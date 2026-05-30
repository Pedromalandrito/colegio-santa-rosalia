from fastapi import APIRouter, Depends
from schemas import estudiantes_schemas as es # es = estudiantes_schemas

from routers.Services.services_estudiantes import create_estudiante as ce # ce = create_estudiante
from routers.Services.services_estudiantes import read_estudiantes as re # re = read_estudiantes
from routers.Services.services_estudiantes import update_estudiante as ue # ue = update_estudiante
from routers.Services.services_estudiantes import delete_estudiante as de # de = delete_estudiante

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/estudiantes")

@router.post("/", response_model=es.EstudiantesRead)
def create_estudiante(session: sessionDep, payload: es.EstudiantesCreate):
    return ce(session = session, estudiante_data = payload)

@router.get("/", response_model=list[es.EstudiantesRead])
def read_estudiantes(session: sessionDep):
    return re(session = session)

@router.patch("/{cedula_estudiante}", response_model=es.EstudiantesRead)
def update_estudiante(cedula_estudiante: str, session: sessionDep, payload: es.EstudiantesUpdatePartial):
    return ue(cedula_estudiante = cedula_estudiante, session = session, estudiante_data = payload)

@router.delete("/{cedula_estudiante}", response_model=es.EstudiantesDelete)
def delete_estudiante(cedula_estudiante: str, session: sessionDep):
    return de(cedula_estudiante = cedula_estudiante, session = session)