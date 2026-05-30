from sqlmodel import Session, select
from models.modelos import Personas
from schemas import personas_schemas as p # p = personas_schemas
from fastapi import HTTPException

def create_persona(session: Session, persona_data: p.PersonaCreate):
    if session.exec(select(Personas).where(Personas.cedula == persona_data.cedula)).first():
        raise HTTPException(status_code=400, detail="Ya existe una persona con esta cédula")

    new_persona = Personas(**persona_data.model_dump())
    session.add(new_persona)
    session.commit()
    session.refresh(new_persona)
    return new_persona

def read_personas(session: Session):
    return session.exec(select(Personas).where(Personas.is_active == True)).all()

def update_persona(persona_id: int, session: Session, persona_data: p.PersonaUpdatePartial):
    persona = session.get(Personas, persona_id)
    if not persona or not persona.is_active:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    datos_actualizados = persona_data.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(persona, campo, valor)
        
    session.add(persona)
    session.commit()
    session.refresh(persona)
    return persona

def delete_persona(persona_id: int, session: Session):
    persona = session.get(Personas, persona_id)
    if not persona or not persona.is_active:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    persona.is_active = False
    session.add(persona)
    session.commit()
    session.refresh(persona)
    return persona