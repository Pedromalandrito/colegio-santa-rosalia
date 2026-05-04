from pydantic import BaseModel

class CreateMetodoPago(BaseModel):
    descripcion: str

class ReadMetodoPago(BaseModel):
    id: int
    descripcion: str

class UpdateMetodoPago(BaseModel):
    descripcion: str

class DeleteMetodoPago(BaseModel):
    is_active: bool