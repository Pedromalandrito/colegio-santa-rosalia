from pydantic import BaseModel

class PersonaCreate(BaseModel):
    cedula: str
    nombre: str
    parentezco: str
    cedula_estudiante: str

class PersonaRead(BaseModel):
    cedula: str
    nombre: str
    parentezco: str
    cedula_estudiante: str

class PersonaUpdatePartial(BaseModel):
    cedula: str | None = None
    nombre: str | None = None
    parentezco: str | None = None
    cedula_estudiante: str | None = None

class PersonaDelete(BaseModel):
    is_active: bool