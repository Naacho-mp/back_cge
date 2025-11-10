from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload
from . import models, schemas

#FUNCIONES TIPO CRUD PARA COMUNICARSE CON LA BD VIA SQLALCHEMY ORM
def create_medidor(db: Session, data: schemas.MedidorCreate) -> models.Medidor:
    cliente = db.get(models.Cliente, data.id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail=f"El Cliente con id {data.id_cliente} no se ha encontrado")

    existe = db.query(models.Medidor).filter_by(codigo_medidor=data.codigo_medidor).first()
    if existe:
        raise HTTPException(status_code=400, detail="El código de medidor ya está registrado")

    obj = models.Medidor(
        codigo_medidor=data.codigo_medidor,
        id_cliente=data.id_cliente,
        direccion_suministro=data.direccion_suministro,
        estado=data.estado
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_medidor(db: Session, id_medidor: int) -> models.Medidor | None:
    return db.query(models.Medidor).options( selectinload(models.Medidor.cliente),
        selectinload(models.Medidor.lecturas)
    ).filter(models.Medidor.id_medidor == id_medidor).first()

def list_medidores(db:Session) -> list[models.Medidor]:
    return db.query(models.Medidor).all()

def update_medidor(db: Session, id_medidor: str, data: schemas.MedidorUpdate) -> models.Medidor | None:
    obj = db.get(models.Medidor, id_medidor)
    if not obj:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_medidor(db:Session, id_medidor: int)-> bool:
    obj = db.get(models.Medidor, id_medidor)

    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
