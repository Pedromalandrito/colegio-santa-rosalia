from pydantic import BaseModel, field_validator

class PersonaBase(BaseModel):
    cedula: str
    nombre: str
    parentezco: str
    cedula_estudiante: str
    
    @field_validator("cedula", "nombre", "parentezco", "cedula_estudiante", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos(cls, valor):
        if valor is None:
            raise ValueError("Este campo no acepta valores nulos (null)")
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
        return valor

class PersonaCreate(PersonaBase):
    pass

class PersonaRead(PersonaBase):
    pass

class PersonaUpdatePartial(BaseModel):
    cedula: str | None = None
    nombre: str | None = None
    parentezco: str | None = None
    cedula_estudiante: str | None = None

    @field_validator("cedula", "nombre", "parentezco", "cedula_estudiante", mode="before")
    @classmethod
    def bloquear_vacios_y_nulos_patch(cls, valor):

        if valor is None:
            raise ValueError("Este campo, no puede ser nulo (null)")
            
        if isinstance(valor, str) and valor.strip() == "":
            raise ValueError("Este campo no puede estar vacío ni contener solo espacios")
            
        return valor

class PersonaDelete(BaseModel):
    is_active: bool