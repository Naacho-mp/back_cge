from typing import List

from sqlalchemy.orm import Session
from app import schemas, crud_clientes, models
from app.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from calculos.verificar_rut import validar_rut


clientes_api = APIRouter(prefix="/api/clientes", tags=["Clientes"]
)

# ENDPOINTS BASICOS PARA EL CRUD DE CLIENTES
# LOGIN DE CLIENTE
@clientes_api.post("/login", response_model=schemas.LoginResponse)
def login_cliente(data: schemas.ClienteLoginSchema, db: Session = Depends(get_db)):

    # Buscar cliente por correo
    cliente = db.query(models.Cliente).filter(models.Cliente.email_contacto == data.email_contacto).first()

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    # Verificar contraseña
    if not crud_clientes.verificar_password(data.password, cliente.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )

    return {
        "message": "Inicio de sesión exitoso",
        "cliente": cliente,
        "primer_login": cliente.primer_login
    }


# CAMBIAR CONTRASEÑA
@clientes_api.post("/cambiar-password")
def cambiar_password(data: schemas.CambiarPasswordSchema, db: Session = Depends(get_db)):

    # Buscar cliente
    cliente = db.query(models.Cliente).filter(models.Cliente.email_contacto == data.email_contacto).first()

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    # Verificar contraseña actual
    if not crud_clientes.verificar_password(data.password_actual, cliente.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La contraseña actual es incorrecta"
        )

    # Verificar que las contraseñas nuevas coincidan
    if data.password_nueva != data.confirmar_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas nuevas no coinciden"
        )


    # Actualizar contraseña
    cliente.password_hash = crud_clientes.crear_password_hash(data.password_nueva)
    cliente.primer_login = False

    db.commit()

    return {
        "message": "Contraseña actualizada exitosamente"
    }


#CREAR CLIENTE
@clientes_api.post("/", response_model=schemas.ClienteOut, status_code=status.HTTP_201_CREATED)
def create_cliente(data: schemas.ClienteCreate, db: Session = Depends(get_db)):
    #Verificar igual aca en el backend que se revise el rut con el script validar_rut segun modulo 11
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