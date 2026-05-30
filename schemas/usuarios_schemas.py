from pydantic import BaseModel, field_validator, field_serializer, ValidationInfo
from datetime import datetime

class UsuarioBase(BaseModel):
    nickname: str
    clave: str
    pregunta1: str
    respuesta1: str
    pregunta2: str
    respuesta2: str

    @field_validator("nickname", "clave", "pregunta1", "respuesta1", "pregunta2", "respuesta2", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos(cls, valor):
        if valor is None:
            raise ValueError("Este campo no acepta valores nulos (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioRead(UsuarioBase):
    id: int
    fecha_creacion: datetime

    @field_serializer('fecha_creacion')
    def formatear_fecha(self, fecha: datetime, _info):
        return fecha.strftime("%d-%m-%Y %I:%M %p")

class UsuarioUpdatePartial(BaseModel):
    nickname: str | None = None
    clave: str | None = None
    pregunta1: str | None = None
    respuesta1: str | None = None
    pregunta2: str | None = None
    respuesta2: str | None = None

    @field_validator("nickname", "clave", "pregunta1", "respuesta1", "pregunta2", "respuesta2", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos_patch(cls, valor, info: ValidationInfo):
        if valor is None:
            if info.field_name in cls.model_fields and info.field_name not in (info.data or {}):
                return valor
            raise ValueError("Este campo, no puede ser nulo (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class UsuarioDelete(BaseModel):
    is_active: bool