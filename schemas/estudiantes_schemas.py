from pydantic import BaseModel, field_validator, field_serializer, ValidationInfo
from datetime import datetime

class EstudiantesBase(BaseModel):
    cedula_estudiante: str
    nombre: str
    apellido: str
    fecha_nacimiento: datetime
    anio: str
    seccion: str
    representante_cedula: str

    @field_validator("cedula_estudiante", "nombre", "apellido", "fecha_nacimiento", "anio", "seccion", "representante_cedula", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos(cls, valor):
        if valor is None:
            raise ValueError("Este campo no acepta valores nulos (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class EstudiantesCreate(EstudiantesBase):
    @field_serializer('fecha_nacimiento')
    def formatear_fecha(self, fecha: datetime, _info):
        return fecha.strftime("%d-%m-%Y %I:%M %p")

class EstudiantesRead(EstudiantesBase):
    @field_serializer('fecha_nacimiento')
    def formatear_fecha(self, fecha: datetime, _info):
        return fecha.strftime("%d-%m-%Y %I:%M %p")

class EstudiantesUpdatePartial(BaseModel):
    cedula_estudiante: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    fecha_nacimiento: datetime | None = None
    anio: str | None = None
    seccion: str | None = None
    representante_cedula: str | None = None

    @field_validator("cedula_estudiante", "nombre", "apellido", "fecha_nacimiento", "anio", "seccion", "representante_cedula", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos_patch(cls, valor, info: ValidationInfo):
        if valor is None:
            if info.field_name in cls.model_fields and info.field_name not in (info.data or {}):
                return valor
            raise ValueError("Este campo, no puede ser nulo (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

    @field_serializer('fecha_nacimiento')
    def formatear_fecha(self, fecha: datetime | None, _info):
        if fecha is None:
            return None
        return fecha.strftime("%d-%m-%Y %I:%M %p")

class EstudiantesDelete(BaseModel):
    is_active: bool