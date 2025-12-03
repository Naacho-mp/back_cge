import io
from sqlalchemy.orm import Session
from app import schemas, crud_boletas
from app.crud_boletas import generar_boleta_pdf
from app.database import get_db
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models import Boleta

boletas_api = APIRouter(prefix="/api/boletas", tags=["Boletas"]
)

# ENDPOINTS BASICOS PARA EL CRUD DE BOLETAS

#LISTAR BOLETAS POR RUT AÑO Y MES
@boletas_api.get("/", response_model=list[schemas.BoletaOut])
def listar_boletas(rut: str | None = None, anio: int | None = None,mes: int | None = None,
    db: Session = Depends(get_db)
):
    return crud_boletas.listar_boletas(db, rut, anio, mes)


#GENERAR BOLETA
@boletas_api.post("/", response_model=schemas.BoletaOut)
def generar_boleta(data: schemas.BoletaCreate,db: Session = Depends(get_db)
) -> schemas.BoletaOut:

    boleta = crud_boletas.generar_boleta(db=db,rut=data.rut,anio=data.anio,mes=data.mes,estado=data.estado
    )
    return boleta

#DESCARGAR BOLETA
@boletas_api.get("/boleta/{id_cliente}/{anio}/{mes}/pdf")
def descargar_boleta_pdf(id_cliente: str, anio: int, mes: int, db: Session = Depends(get_db)):
    boleta = db.query(Boleta).filter_by(id_cliente=id_cliente, anio=anio, mes=mes).first()
    if not boleta:
        raise HTTPException(status_code=404, detail="Boleta no encontrada")

    pdf_bytes = generar_boleta_pdf(boleta)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={
        "Content-Disposition": f"inline; filename=boleta_{id_cliente}_{anio}_{mes}.pdf"

    })

