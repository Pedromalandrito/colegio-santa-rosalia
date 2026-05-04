from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class PagosCreate(BaseModel):
    cedula_estudiante: str
    monto: Decimal
    mes_correspondiente: str
    anio_correspondiente: int
    metodo_pago: int
    referencia_pago: str

class PagosRead(BaseModel):
    id: int
    cedula_estudiante: str
    monto: Decimal
    mes_correspondiente: str
    anio_correspondiente: int
    fecha_pago: datetime
    metodo_pago: int
    referencia_pago: str

class PagosUpdatePartial(BaseModel):
    mes_correspondiente: str | None = None
    anio_correspondiente: int | None = None
    metodo_pago: int | None = None
    referencia_pago: str | None = None

class PagosDelete(BaseModel):
    is_active: bool