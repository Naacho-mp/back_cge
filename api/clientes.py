from enum import Enum
from typing import List

from sqlalchemy.orm import Session
from app import schemas, crud_clientes
from app.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from calculos.verificar_rut import validar_rut


clientes_api = APIRouter(prefix="/api/clientes", tags=["Clientes"]
)

# ENDPOINTS BASICOS PARA EL CRUD DE CLIENTES

#CREAR CLIENTE
@clientes_api.post("/", response_model=schemas.ClienteOut, status_code=status.HTTP_201_CREATED)
def create_cliente(data: schemas.ClienteCreate, db: Session = Depends(get_db)):
    if not validar_rut(data.rut):
        raise HTTPException(status_code=400, detail="RUT inválido")

    try:
        cliente = crud_clientes.create_cliente(db, data)
        return cliente
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear cliente: {str(e)}")

#LEER-OBTENER CLIENTE
@clientes_api.get("/{id_cliente}", response_model=schemas.ClienteOut, status_code=status.HTTP_200_OK)
def get_cliente(id_cliente: str, db: Session = Depends(get_db)):
    cliente = crud_clientes.get_cliente(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente con id {id_cliente} no encontrado")
    return cliente

#LISTAR A TODOS LOS CLIENTES
@clientes_api.get("/", response_model=List[schemas.ClienteOut], status_code=200)
def list_clientes(db: Session = Depends(get_db)):
    clientes = crud_clientes.list_clientes(db)
    return clientes

#ACTUALIZAR A UN CLIENTE SEGUN ID_CLIENTE
@clientes_api.put("/{id_cliente}", response_model=schemas.ClienteOut, status_code=200)
def update_cliente(id_cliente: str, data: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    updated_cliente = crud_clientes.update_cliente(db, id_cliente, data)

    if not updated_cliente:
        raise HTTPException(status_code=404,detail=f"Cliente con id {id_cliente} no encontrado"
        )
    return updated_cliente

#ELIMINAR A UN CLIENTE SEGUN ID_CLIENTE
@clientes_api.delete("/{id_cliente}", status_code=204)
def delete_cliente(id_cliente: str, db: Session = Depends(get_db)):
    cliente = crud_clientes.get_cliente(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404,detail=f"Cliente con id {id_cliente} no encontrado"
        )

    crud_clientes.delete_cliente(db, id_cliente)
    return None