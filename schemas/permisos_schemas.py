from pydantic import BaseModel

class PermisoCreate(BaseModel):
    descripcion: str

class PermisoRead(BaseModel):
    id: int
    descripcion: str

class PermisoUpdate(BaseModel):
    descripcion: str

class PermisoDelete(BaseModel):
    is_active: bool