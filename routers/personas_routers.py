from fastapi import APIRouter, Depends
from schemas import personas_schemas as p # p = personas_schemas

from routers.Services.services_personas import create_persona as cp # cp = create_persona
from routers.Services.services_personas import read_personas as rp # rp = read_personas
from routers.Services.services_personas import update_persona as up # up = update_persona
from routers.Services.services_personas import delete_persona as dp # dp = delete_persona

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/personas")

@router.post("/", response_model=p.PersonaRead)
def create_persona(session: sessionDep, payload: p.PersonaCreate):
    return cp(session = session, persona_data = payload)

@router.get("/", response_model=list[p.PersonaRead])
def read_personas(session: sessionDep):
    return rp(session = session)

@router.patch("/{persona_id}", response_model=p.PersonaRead)
def update_persona(persona_id: int, session: sessionDep, payload: p.PersonaUpdatePartial):
    return up(persona_id = persona_id, session = session, persona_data = payload)

@router.delete("/{persona_id}", response_model=p.PersonaDelete)
def delete_persona(persona_id: int, session: sessionDep):
    return dp(persona_id = persona_id, session = session)