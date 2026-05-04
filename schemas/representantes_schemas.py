from pydantic import BaseModel

class RepresentanteCreate(BaseModel):
    cedula_representante: str
    nombre: str
    apellido: str
    telefono: str
    correo: str
    direccion: str
    cedula_estudiante: str

class RepresentanteRead(BaseModel):
    cedula_representante: str
    nombre: str
    apellido: str
    telefono: str
    correo: str
    direccion: str
    cedula_estudiante: str

class RepresentanteUpdatePartial(BaseModel):
    cedula_representante: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None
    correo: str | None = None
    direccion: str | None = None
    cedula_estudiante: str | None = None

class RepresentanteDelete(BaseModel):
    is_active: bool