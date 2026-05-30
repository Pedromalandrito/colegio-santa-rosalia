from pydantic import BaseModel, field_validator

class CompositoraPermisosBase(BaseModel):
    usuario_id: int
    permiso_id: int

    @field_validator("usuario_id", "permiso_id", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos(cls, valor):
        if valor is None:
            raise ValueError("Este campo no acepta valores nulos (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor