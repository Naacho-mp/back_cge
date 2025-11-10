from typing import List

from sqlalchemy.orm import Session
from app import crud_lecturas
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
    return crud_lecturas.create_lectura(db=db, data=data)


# LISTAR LECTURAS
@lecturas_api.get("/", response_model=List[LecturaOut])
def list_lecturas(db: Session = Depends(get_db), id_medidor: int | None = None, anio: int | None = None, mes: int | None = None
):
    return crud_lecturas.list_lecturas(
        db=db,
        id_medidor=id_medidor,
        anio=anio,
        mes=mes
    )