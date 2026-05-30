from pydantic import BaseModel, field_validator, ValidationInfo

class RepresentanteBase(BaseModel):
    cedula_representante: str
    nombre: str
    apellido: str
    telefono: str
    correo: str
    direccion: str
    cedula_estudiante: str

    @field_validator("cedula_representante", "nombre", "apellido", "telefono", "correo", "direccion", "cedula_estudiante", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos(cls, valor):
        if valor is None:
            raise ValueError("Este campo no acepta valores nulos (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class RepresentanteCreate(RepresentanteBase):
    pass

class RepresentanteRead(RepresentanteBase):
    pass

class RepresentanteUpdatePartial(BaseModel):
    cedula_representante: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None
    correo: str | None = None
    direccion: str | None = None
    cedula_estudiante: str | None = None

    @field_validator("cedula_representante", "nombre", "apellido", "telefono", "correo", "direccion", "cedula_estudiante", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos_patch(cls, valor, info: ValidationInfo):
        if valor is None:
            if info.field_name in cls.model_fields and info.field_name not in (info.data or {}):
                return valor
            raise ValueError("Este campo, no puede ser nulo (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class RepresentanteDelete(BaseModel):
    is_active: bool