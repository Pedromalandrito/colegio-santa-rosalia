from pydantic import BaseModel
from datetime import datetime

class EstudiantesCreate(BaseModel):
    cedula_estudiante: str
    nombre: str
    apellido: str
    fecha_nacimiento: datetime
    anio: str
    seccion: str
    representante_cedula: str

class EstudiantesRead(BaseModel):
    cedula_estudiante: str
    nombre: str
    apellido: str
    fecha_nacimiento: datetime
    anio: str
    seccion: str
    representante_cedula: str

class EstudiantesUpdatePartial(BaseModel):
    cedula_estudiante: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    fecha_nacimiento: datetime | None = None
    anio: str | None = None
    seccion: str | None = None
    representante_cedula: str | None = None

class EstudiantesDelete(BaseModel):
    is_active: bool