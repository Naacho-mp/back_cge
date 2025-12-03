from typing import List

from sqlalchemy.orm import Session

from app import schemas, crud_medidores, models
from app.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter

medidores_api = APIRouter(prefix="/api/medidores", tags=["Medidores"]
)

# ENDPOINTS BASICOS PARA EL CRUD DE MEDIDORES

#CREAR MEDIDOR
@medidores_api.post("/", response_model=schemas.MedidorOut, status_code=status.HTTP_201_CREATED)
def create_medidor(data: schemas.MedidorCreate, db: Session = Depends(get_db)):
    medidor = crud_medidores.create_medidor(db, data)

    # traer el cliente para obtener el rut
    cliente = db.get(models.Cliente, medidor.id_cliente)

    return {
        "id_medidor": medidor.id_medidor,
        "codigo_medidor": medidor.codigo_medidor,
        "id_cliente": medidor.id_cliente,
        "rut": cliente.rut,
        "direccion_suministro": medidor.direccion_suministro,
        "latitud": medidor.latitud,
        "longitud": medidor.longitud,
        "estado": medidor.estado,
        "created_at": medidor.created_at,
        "updated_at": medidor.updated_at,
    }


#LEER-OBTENER UN MEDIDOR SEGUN SU ID_MEDIDOR
@medidores_api.get("/{id_medidor}", response_model=schemas.MedidorOut)
def get_medidor(id_medidor: int, db: Session = Depends(get_db)):
    medidor = db.get(models.Medidor, id_medidor)
    if not medidor:
        raise HTTPException(status_code=404, detail="Medidor no encontrado")
    return medidor

#LISTAR A TODOS LOS MEDIDORES}
@medidores_api.get("/", response_model=List[schemas.MedidorOut], status_code=200)
def list_medidores(db: Session = Depends(get_db)):
    medidores = crud_medidores.list_medidores(db)

    resultado = []
    for m in medidores:
        cliente = db.get(models.Cliente, m.id_cliente)

        resultado.append({
            "id_medidor": m.id_medidor,
            "codigo_medidor": m.codigo_medidor,
            "id_cliente": m.id_cliente,
            "rut": cliente.rut if cliente else None,
            "direccion_suministro": m.direccion_suministro,
            "latitud": m.latitud,
            "longitud": m.longitud,
            "estado": m.estado,
            "created_at": m.created_at,
            "updated_at": m.updated_at,
        })

    return resultado


#ACTUALIZAR UN MEDIDOR SEGUN ID_MEDIDOR
@medidores_api.put("/{id_medidor}", response_model=schemas.MedidorOut, status_code=200)
def update_medidor(id_medidor: int, data: schemas.MedidorUpdate, db: Session = Depends(get_db)):
    updated_medidor = crud_medidores.update_medidor(db, id_medidor, data)

    if not updated_medidor:
        raise HTTPException(
            status_code=404,
            detail=f"Medidor con id {id_medidor} no encontrado"
        )

    # Obtener cliente para obtener el rut
    cliente = db.get(models.Cliente, updated_medidor.id_cliente)

    return {
        "id_medidor": updated_medidor.id_medidor,
        "codigo_medidor": updated_medidor.codigo_medidor,
        "id_cliente": updated_medidor.id_cliente,
        "rut": cliente.rut if cliente else None,
        "direccion_suministro": updated_medidor.direccion_suministro,
        "latitud": updated_medidor.latitud,
        "longitud": updated_medidor.longitud,
        "estado": updated_medidor.estado,
        "created_at": updated_medidor.created_at,
        "updated_at": updated_medidor.updated_at,
    }


#ELIMINAR UN MEDIDOR SEGUN ID_MEDIDOR
@medidores_api.delete("/{id_medidor}", status_code=204)
def delete_medidor(id_medidor: int, db: Session = Depends(get_db)):
    medidor = crud_medidores.get_medidor(db, id_medidor)
    if not medidor:
        raise HTTPException(status_code=404,detail=f"Medidor con id {id_medidor} no encontrado"
        )

    crud_medidores.delete_medidor(db, id_medidor)
    return None


# OBTENER MEDIDORES POR CLIENTE
@medidores_api.get("/cliente/{id_cliente}", response_model=List[schemas.MedidorOut], status_code=200)
def get_medidores_by_cliente(id_cliente: str, db: Session = Depends(get_db)):

    # Verificar que el cliente existe
    cliente = db.get(models.Cliente, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Obtener medidores del cliente
    medidores = db.query(models.Medidor).filter(
        models.Medidor.id_cliente == id_cliente
    ).all()

    resultado = []
    for m in medidores:
        resultado.append({
            "id_medidor": m.id_medidor,
            "codigo_medidor": m.codigo_medidor,
            "id_cliente": m.id_cliente,
            "rut": cliente.rut,
            "direccion_suministro": m.direccion_suministro,
            "latitud": m.latitud,
            "longitud": m.longitud,
            "estado": m.estado,
            "created_at": m.created_at,
            "updated_at": m.updated_at,
        })

    return resultado