from pydantic import BaseModel, field_validator, field_serializer, ValidationInfo
from decimal import Decimal
from datetime import datetime

class PagosBase(BaseModel):
    cedula_estudiante: str
    monto: Decimal
    mes_correspondiente: str
    anio_correspondiente: int
    metodo_pago: int
    referencia_pago: str

    @field_validator("cedula_estudiante", "monto", "mes_correspondiente", "anio_correspondiente", "metodo_pago", "referencia_pago", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos(cls, valor):
        if valor is None:
            raise ValueError("Este campo no acepta valores nulos (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class PagosCreate(PagosBase):
    pass

class PagosRead(PagosBase):
    id: int
    fecha_pago: datetime

    @field_serializer('fecha_pago')
    def formatear_fecha(self, fecha: datetime, _info):
        return fecha.strftime("%d-%m-%Y %I:%M %p")

class PagosUpdatePartial(BaseModel):
    mes_correspondiente: str | None = None
    anio_correspondiente: int | None = None
    metodo_pago: int | None = None
    referencia_pago: str | None = None

    @field_validator("mes_correspondiente", "anio_correspondiente", "metodo_pago", "referencia_pago", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos_patch(cls, valor, info: ValidationInfo):
        if valor is None:
            if info.field_name in cls.model_fields and info.field_name not in (info.data or {}):
                return valor
            raise ValueError("Este campo, no puede ser nulo (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class PagosDelete(BaseModel):
    is_active: bool