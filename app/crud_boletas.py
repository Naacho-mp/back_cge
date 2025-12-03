import io
from decimal import Decimal
from fastapi import HTTPException
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from app.models import Cliente, Boleta, LecturaConsumo
from calculos.total_a_pagar import calcular_montos

#FUNCIONES TIPO CRUD PARA COMUNICARSE CON LA BD VIA SQLALCHEMY ORM

def listar_boletas(db: Session, rut: str | None = None, anio: int | None = None, mes: int | None = None):

    query = db.query(Boleta)

    if rut:
        cliente = db.query(Cliente).filter(Cliente.rut == rut).first()
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente con RUT {rut} no existe"
            )
        query = query.filter(Boleta.id_cliente == cliente.id_cliente)

    if anio:
        query = query.filter(Boleta.anio == anio)
    if mes:
        query = query.filter(Boleta.mes == mes)

    return query.order_by(Boleta.anio.desc(), Boleta.mes.desc()).all()


def generar_boleta(db: Session, rut: str, anio: int, mes: int, estado: str) -> Boleta:
    cliente = db.query(Cliente).filter(Cliente.rut == rut).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente con Rut {rut} no existe")

    # Evitar duplicados
    boleta_existente = db.query(Boleta).filter_by(
        id_cliente=cliente.id_cliente,
        anio=anio,
        mes=mes
    ).first()

    if boleta_existente:
        raise HTTPException(status_code=400, detail="La boleta para este cliente en este año y mes ya existe.")

    kwh_total = 0
    tiene_lecturas = False

    # Sumar lecturas del mismo mes de todos los medidores del cliente
    for medidor in cliente.medidores:
        lectura_actual = (
            db.query(LecturaConsumo)
            .filter_by(id_medidor=medidor.id_medidor, anio=anio, mes=mes)
            .first()
        )

        if lectura_actual is None:
            continue

        tiene_lecturas = True

    #Se suma la lectura del mes
        kwh_total += lectura_actual.lectura_kwh

    if not tiene_lecturas:
        raise HTTPException(
            status_code=400,
            detail=f"No existen lecturas registradas para el cliente {rut} en {mes}/{anio}."
        )

    montos = calcular_montos(Decimal(kwh_total))

    boleta = Boleta(
        id_cliente=cliente.id_cliente,
        anio=anio,
        mes=mes,
        kwh_total=kwh_total,
        tarifa_base=montos["tarifa_base"],
        cargos=montos["cargos"],
        iva=montos["iva"],
        total_pagar=montos["total"],
        estado=estado
    )

    db.add(boleta)
    db.commit()
    db.refresh(boleta)

    return boleta



def generar_boleta_pdf(boleta) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    nombre_mes = meses.get(boleta.mes, str(boleta.mes))

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, h - 90, f"Boleta de Consumo Electricidad (CGE)")

    #Subtitulo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, h - 140, f"Detalle de mi Cuenta:")
    c.drawString(50, h - 170, f"______________________________________________________________")

    # Datos del cliente y montos
    c.setFont("Helvetica", 12)

    c.drawString(450, 800, f"ID Boleta: {boleta.id_boleta}")
    c.drawString(50, 640, f"ID Cliente: {boleta.id_cliente}")

    c.drawString(50, 610, f"Periodo (Año): {boleta.anio}")
    c.drawString(50, 580, f"Periodo (Mes): {nombre_mes}")

    c.drawString(50, 550, f"Kwh Total: {boleta.kwh_total}")

    c.drawString(50, 340, f"________________________________________________________________________")
    c.drawString(50, 310, f"Tarifa Base: ")
    c.drawString(450, 310, f"$ {boleta.tarifa_base}")

    c.drawString(50, 280, f"Cargos: ")
    c.drawString(450, 280, f"$ {boleta.cargos}")

    c.drawString(50, 250, f"IVA: ")
    c.drawString(450, 250, f"$ {boleta.iva}")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 180, f"Total a Pagar: ")
    c.drawString(450, 180, f"$ {boleta.total_pagar} ")



    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
