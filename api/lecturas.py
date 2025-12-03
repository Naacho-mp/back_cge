from typing import List

from sqlalchemy.orm import Session
from app import crud_lecturas
from app import models
from app.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter

from app.schemas import LecturaOut, LecturaConsumoCreate

lecturas_api = APIRouter(prefix="/api/lecturas", tags=["Lecturas"]
)

# ENDPOINTS BASICOS PARA EL CRUD DE LECTURAS

# CREAR UNA LECTURA
@lecturas_api.post("/", response_model=LecturaOut)
def create_lectura(data: LecturaConsumoCreate, db: Session = Depends(get_db)
):
    medidor = db.get(models.Medidor, data.id_medidor)

    if not medidor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medidor no Encontrado")

    lectura = crud_lecturas.create_lectura(db=db, data=data)

    return {
        "id_lectura":lectura.id_lectura,
        "id_medidor":lectura.id_medidor,
        "anio":lectura.anio,
        "mes":lectura.mes,
        "lectura_kwh":lectura.lectura_kwh,
        "observacion":lectura.observacion,
        "created_at":lectura.created_at,
        "codigo_medidor":medidor.codigo_medidor
    }


# LISTAR LECTURAS POR CODIGO DE MEDIDOR
@lecturas_api.get("/", response_model=List[LecturaOut])
def get_lecturas(db: Session = Depends(get_db)):
    lecturas = db.query(models.LecturaConsumo).all()

    # dar respuesta con código de medidor
    resultado = []
    for lectura in lecturas:
        medidor = db.get(models.Medidor, lectura.id_medidor)

        resultado.append({
            "id_lectura": lectura.id_lectura,
            "id_medidor": lectura.id_medidor,
            "codigo_medidor": medidor.codigo_medidor if medidor else None,
            "anio": lectura.anio,
            "mes": lectura.mes,
            "lectura_kwh": lectura.lectura_kwh,
            "observacion": lectura.observacion,
            "created_at": lectura.created_at,
        })

    return resultado