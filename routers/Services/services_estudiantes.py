from sqlmodel import Session, select
from models.modelos import Estudiantes
from schemas import estudiantes_schemas as es # es = estudiantes_schemas
from fastapi import HTTPException

def create_estudiante(session: Session, estudiante_data: es.EstudiantesCreate):
    new_estudiante = Estudiantes(**estudiante_data.model_dump())
    session.add(new_estudiante)
    session.commit()
    session.refresh(new_estudiante)
    return new_estudiante

def read_estudiantes(session: Session):
    return session.exec(select(Estudiantes).where(Estudiantes.is_active == True)).all()

def update_estudiante(cedula_estudiante: str, session: Session, estudiante_data: es.EstudiantesUpdatePartial):
    estudiante = session.get(Estudiantes, cedula_estudiante)
    if not estudiante or not estudiante.is_active:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    datos_actualizados = estudiante_data.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(estudiante, campo, valor)
    
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

def delete_estudiante(cedula_estudiante: str, session: Session):
    estudiante = session.get(Estudiantes, cedula_estudiante)
    if not estudiante or not estudiante.is_active:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.is_active = False
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante