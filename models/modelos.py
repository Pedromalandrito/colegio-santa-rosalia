from sqlmodel import SQLModel, Field, Relationship, Column, Numeric
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

class CompositoraPermisos(SQLModel, table=True):
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuarios.id", primary_key=True)
    permiso_id: Optional[int] = Field(default=None, foreign_key="permisos.id", primary_key=True)

class Usuarios(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str
    clave: str
    pregunta1: str
    respuesta1: str
    pregunta2: str
    respuesta2: str
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    permisos: List["Permisos"] = Relationship(back_populates="usuarios", link_model=CompositoraPermisos)

class Permisos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    is_active: bool = Field(default=True)

    usuarios: List["Usuarios"] = Relationship(back_populates="permisos", link_model=CompositoraPermisos)

class MetodosPago(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    is_active: bool = Field(default=True)

    pagos: List["Pagos"] = Relationship(back_populates="metodo")

class Estudiantes(SQLModel, table=True):
    cedula_estudiante: str = Field(primary_key=True)
    nombre: str
    apellido: str
    fecha_nacimiento: datetime
    anio: str
    seccion: str
    representante_cedula: str = Field(foreign_key="representantes.cedula_representante")
    is_active: bool = Field(default=True)

    representantes: List["Representantes"] = Relationship(
        back_populates="estudiante", 
        sa_relationship_kwargs={"foreign_keys": "[Representantes.cedula_estudiante]"}
    )
    personas_autorizadas: List["Personas"] = Relationship(back_populates="estudiante")
    pagos: List["Pagos"] = Relationship(back_populates="estudiante")

class Representantes(SQLModel, table=True):
    cedula_representante: str = Field(primary_key=True)
    nombre: str
    apellido: str
    telefono: str
    correo: str
    direccion: str
    cedula_estudiante: str = Field(foreign_key="estudiantes.cedula_estudiante")
    is_active: bool = Field(default=True)

    estudiante: "Estudiantes" = Relationship(
        back_populates="representantes", 
        sa_relationship_kwargs={"foreign_keys": "[Representantes.cedula_estudiante]"}
    )

class Personas(SQLModel, table=True):
    cedula: str = Field(primary_key=True)
    nombre: str
    parentezco: str
    cedula_estudiante: str = Field(foreign_key="estudiantes.cedula_estudiante")
    is_active: bool = Field(default=True)

    estudiante: "Estudiantes" = Relationship(back_populates="personas_autorizadas")

class Pagos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cedula_estudiante: str = Field(foreign_key="estudiantes.cedula_estudiante")
    monto: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    mes_correspondiente: str
    anio_correspondiente: int
    fecha_pago: datetime = Field(default_factory=datetime.now)
    metodo_pago: int = Field(foreign_key="metodospago.id")
    referencia_pago: str
    is_active: bool = Field(default=True)

    estudiante: "Estudiantes" = Relationship(back_populates="pagos")
    metodo: "MetodosPago" = Relationship(back_populates="pagos")