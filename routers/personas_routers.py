from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos import Personas
from database.connection import get_session
from schemas import personas_schemas as p # p = personas_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/personas/", response_model=p.PersonaCreate)
def create_persona(session: sessionDep, persona_data: p.PersonaCreate):
    if session.exec(select(Personas).where(Personas.cedula == persona_data.cedula)).first():
        raise HTTPException(status_code=400, detail="Ya existe una persona con esta cédula")

    new_persona = Personas(
        cedula=persona_data.cedula,
        nombre=persona_data.nombre,
        parentezco=persona_data.parentezco,
        cedula_estudiante=persona_data.cedula_estudiante
    )
    session.add(new_persona)
    session.commit()
    session.refresh(new_persona)
    return new_persona

@router.get("/personas/", response_model=list[p.PersonaRead])
def read_personas(session: sessionDep):
    personas = session.exec(select(Personas).where(Personas.is_active == True)).all()
    return personas

@router.patch("/personas/{persona_id}", response_model=p.PersonaUpdatePartial)
def update_persona(persona_id: int, session: sessionDep, persona_data: p.PersonaUpdatePartial):
    persona = session.get(Personas, persona_id)
    if not persona or not persona.is_active:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if persona_data.nombre is not None:
        persona.nombre = persona_data.nombre
    if persona_data.parentezco is not None:
        persona.parentezco = persona_data.parentezco
    if persona_data.cedula_estudiante is not None:
        persona.cedula_estudiante = persona_data.cedula_estudiante
    session.add(persona)
    session.commit()
    session.refresh(persona)
    return persona

@router.delete("/personas/{persona_id}", response_model=p.PersonaDelete)
def delete_persona(persona_id: int, session: sessionDep):
    persona = session.get(Personas, persona_id)
    if not persona or not persona.is_active:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    persona.is_active = False
    session.add(persona)
    session.commit()
    session.refresh(persona)
    return {"mensaje": "La persona ha sido desactivada exitosamente"}