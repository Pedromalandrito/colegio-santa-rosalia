from pydantic import BaseModel, field_validator, ValidationInfo

class PermisoBase(BaseModel):
    descripcion: str

    @field_validator("descripcion", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos(cls, valor):
        if valor is None:
            raise ValueError("Este campo no acepta valores nulos (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class PermisoCreate(PermisoBase):
    pass

class PermisoRead(PermisoBase):
    id: int

class PermisoUpdate(BaseModel):
    descripcion: str | None = None

    @field_validator("descripcion", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos_patch(cls, valor, info: ValidationInfo):
        if valor is None:
            if info.field_name in cls.model_fields and info.field_name not in (info.data or {}):
                return valor
            raise ValueError("Este campo, no puede ser nulo (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class PermisoDelete(BaseModel):
    is_active: bool