from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .models import LecturaConsumo

#FUNCIONES TIPO CRUD PARA COMUNICARSE CON LA BD VIA SQLALCHEMY ORM
def create_lectura(db: Session, data: schemas.LecturaConsumoCreate) -> models.LecturaConsumo:
    medidor = db.get(models.Medidor, data.id_medidor)

    if not medidor:
        raise HTTPException(status_code=404, detail=f"El medidor con id {data.id_medidor} no existe")

    lectura_existente = (
        db.query(models.LecturaConsumo)
        .filter_by(id_medidor=data.id_medidor, anio=data.anio, mes=data.mes)
        .first()
    )
    if lectura_existente:
        raise HTTPException(status_code=400, detail="Ya existe una lectura para ese medidor, año y mes")

    obj = models.LecturaConsumo(
        id_medidor=data.id_medidor,
        anio=data.anio,
        mes=data.mes,
        lectura_kwh=data.lectura_kwh,
        observacion=data.observacion,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_lecturas(db: Session, id_medidor: int | None = None, anio: int | None = None, mes: int | None = None) -> List[LecturaConsumo]:
    query = db.query(LecturaConsumo)

    if id_medidor is not None:
        query = query.filter(LecturaConsumo.id_medidor == id_medidor)
    if anio is not None:
        query = query.filter(LecturaConsumo.anio == anio)
    if mes is not None:
        query = query.filter(LecturaConsumo.mes == mes)

    return query.all()