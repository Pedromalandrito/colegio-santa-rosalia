from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos import Estudiantes
from database.connection import get_session
from schemas import estudiantes_schemas as es # es = estudiantes_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/estudiantes", response_model=es.EstudiantesCreate)
def create_estudiante(session: sessionDep, estudiante_data: es.EstudiantesCreate):
    new_estudiante = Estudiantes(
        cedula_estudiante=estudiante_data.cedula_estudiante,
        nombre=estudiante_data.nombre,
        apellido=estudiante_data.apellido,
        fecha_nacimiento=estudiante_data.fecha_nacimiento,
        anio=estudiante_data.anio,
        seccion=estudiante_data.seccion,
        representante_cedula=estudiante_data.representante_cedula
    )
    session.add(new_estudiante)
    session.commit()
    session.refresh(new_estudiante)
    return new_estudiante

@router.get("/estudiantes", response_model=list[es.EstudiantesRead])
def read_estudiantes(session: sessionDep):
    estudiantes = session.exec(select(Estudiantes).where(Estudiantes.is_active == True)).all()
    return estudiantes

@router.patch("/estudiantes/{cedula_estudiante}", response_model=es.EstudiantesUpdatePartial)
def update_estudiante(session: sessionDep, cedula_estudiante: str, estudiante_data: es.EstudiantesUpdatePartial):
    estudiante = session.get(Estudiantes, cedula_estudiante)
    if not estudiante or not estudiante.is_active:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    campos_editables = {
        "cedula_estudiante": estudiante_data.cedula_estudiante,
        "nombre": estudiante_data.nombre,
        "apellido": estudiante_data.apellido,
        "fecha_nacimiento": estudiante_data.fecha_nacimiento,
        "anio": estudiante_data.anio,
        "seccion": estudiante_data.seccion,
        "representante_cedula": estudiante_data.representante_cedula
    }

    for nombre_campo, valor in campos_editables.items():
        setattr(estudiante, nombre_campo, valor)
    
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.delete("/estudiantes/{cedula_estudiante}", response_model=es.EstudiantesDelete)
def delete_estudiante(session: sessionDep, cedula_estudiante: str):
    estudiante = session.get(Estudiantes, cedula_estudiante)
    if not estudiante or not estudiante.is_active:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.is_active = False
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return {"is_active": estudiante.is_active}