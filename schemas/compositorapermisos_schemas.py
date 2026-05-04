from pydantic import BaseModel

class CompositorapermisosCreate(BaseModel):
    usuario_id: int
    permiso_id: int

class CompositorapermisosRead(BaseModel):
    usuario_id: int
    permiso_id: int