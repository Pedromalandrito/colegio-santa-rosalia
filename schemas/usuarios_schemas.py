from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nickname: str
    clave: str
    pregunta1: str
    respuesta1: str
    pregunta2: str
    respuesta2: str

class UsuarioRead(BaseModel):
    id: int
    nickname: str
    pregunta1: str
    respuesta1: str
    pregunta2: str
    respuesta2: str
    fecha_creacion: str

class UsuarioUpdatePartial(BaseModel):
    nickname: str | None = None
    clave: str | None = None
    pregunta1: str | None = None
    respuesta1: str | None = None
    pregunta2: str | None = None
    respuesta2: str | None = None

class UsuarioDelete(BaseModel):
    is_active: bool