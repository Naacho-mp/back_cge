from sqlalchemy.orm import Session
from . import models, schemas

#FUNCIONES TIPO CRUD PARA COMUNICARSE CON LA BD VIA SQLALCHEMY ORM

def create_cliente(db:Session, data: schemas.ClienteCreate)->models.Cliente:
    obj = models.Cliente(
        rut=data.rut,
        nombre_razon = data.nombre_razon,
        email_contacto = data.email_contacto,
        telefono = data.telefono,
        direccion_facturacion = data.direccion_facturacion,
        estado = data.estado,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_cliente(db:Session, id_cliente: str)-> models.Cliente | None:
    return db.get(models.Cliente, id_cliente)

def list_clientes(db:Session) -> list[models.Cliente]:
    return db.query(models.Cliente).all()


def update_cliente(db: Session, id_cliente: str, data: schemas.ClienteUpdate) -> models.Cliente | None:
    obj = db.get(models.Cliente, id_cliente)
    if not obj:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj



def delete_cliente(db:Session, id_cliente: str)-> bool:
    obj = db.get(models.Cliente, id_cliente)

    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

