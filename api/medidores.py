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
    try:
        medidor = crud_medidores.create_medidor(db, data)
        return medidor
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear medidor: {str(e)}")

#LEER-OBTENER UN MEDIDOR SEGUN SU ID_MEDIDOR
@medidores_api.get("/{id_medidor}", response_model=schemas.MedidorOut)
def get_medidor(id_medidor: int, db: Session = Depends(get_db)):
    medidor = db.get(models.Medidor, id_medidor)
    if not medidor:
        raise HTTPException(status_code=404, detail="Medidor no encontrado")
    return medidor

#LISTAR A TODOS LOS CLIENTES
@medidores_api.get("/", response_model=List[schemas.MedidorOut], status_code=200)
def list_medidores(db: Session = Depends(get_db)):
    medidores = crud_medidores.list_medidores(db)
    return medidores

#ACTUALIZAR UN MEDIDOR SEGUN ID_CLIENTE
@medidores_api.put("/{id_medidor}", response_model=schemas.MedidorOut, status_code=200)
def update_medidor(id_medidor: int, data: schemas.MedidorUpdate, db: Session = Depends(get_db)):
    updated_medidor = crud_medidores.update_medidor(db, id_medidor, data)

    if not updated_medidor:
        raise HTTPException(status_code=404,detail=f"Medidor con id {id_medidor} no encontrado"
        )
    return updated_medidor

#ELIMINAR UN MEDIDOR SEGUN ID_MEDIDOR
@medidores_api.delete("/{id_medidor}", status_code=204)
def delete_medidor(id_medidor: int, db: Session = Depends(get_db)):
    medidor = crud_medidores.get_medidor(db, id_medidor)
    if not medidor:
        raise HTTPException(status_code=404,detail=f"Medidor con id {id_medidor} no encontrado"
        )

    crud_medidores.delete_medidor(db, id_medidor)
    return None