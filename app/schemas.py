from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, conint, confloat

# SCHEMAS NECESARIOS PARA DEFINIR LA ESTRUCTURA DE LOS DATOS QUE VAN O SALEN DE LA API

class EstadoMedidorEnum(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"


#----------------------  CLIENTE ---------------------------
class ClienteSchema(BaseModel):
    rut: str
    nombre_razon: str
    email_contacto: EmailStr
    telefono: Optional[str]
    direccion_facturacion: str
    estado: str

class ClienteCreate(ClienteSchema):
    pass

class ClienteRead(ClienteSchema):
    id_cliente: str
    rut: str
    nombre_razon: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ClienteUpdate(BaseModel):
    email_contacto: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion_facturacion: Optional[str] = None
    estado: Optional[str] = None

class ClienteOut(ClienteSchema):
    id_cliente: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

#--------------------------- MEDIDOR ------------------------------------------
class MedidorSchema(BaseModel):
    codigo_medidor: str
    id_cliente: str
    direccion_suministro: str
    estado: EstadoMedidorEnum = Field(default=EstadoMedidorEnum.ACTIVO)

class MedidorCreate(MedidorSchema):
    pass

class MedidorRead(MedidorSchema):
    id_medidor: int
    codigo_medidor: str
    id_cliente: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes  = True

class MedidorUpdate(BaseModel):
    direccion_suministro: Optional[str] = None
    estado: Optional[EstadoMedidorEnum] = None

class MedidorOut(MedidorSchema):
    id_medidor: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


#----------------------- LECTURA_CONSUMO-----------------------------
class LecturaConsumoSchema(BaseModel):
    id_medidor: int
    anio: int
    mes: int = Field(..., ge=1, le=12)
    lectura_kwh: conint(ge=0)
    observacion: Optional[str]

class LecturaConsumoCreate(LecturaConsumoSchema):
    pass

class LecturaConsumoRead(LecturaConsumoSchema):
    id_lectura: int
    created_at: datetime

    class Config:
        from_attributes  = True


class LecturaConsumoUpdate(BaseModel):
    lectura_kwh: Optional[conint(ge=0)]= None
    observacion: Optional[str] = None

class LecturaOut(LecturaConsumoSchema):
    id_lectura: int
    created_at: datetime

    class Config:
        from_attributes = True

#------------------------  BOLETA -----------------------------
class BoletaSchema(BaseModel):
    id_cliente: str
    anio: int
    mes: int = Field(ge=1, le=12)

class BoletaCreate(BoletaSchema):
    pass

class BoletaOut(BaseModel):
    id_boleta: int
    id_cliente: str
    anio: int
    mes: int
    kwh_total: float
    tarifa_base: float
    cargos: float
    iva: float
    total_pagar: float
    estado: str

    class Config:
        from_attributes = True
