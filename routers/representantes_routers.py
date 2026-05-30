from fastapi import APIRouter, Depends
from schemas import representantes_schemas as rs # rs = representantes_schemas

from routers.Services.services_representantes import create_representante as cr # cr = create_representante
from routers.Services.services_representantes import read_representantes as rr # rr = read_representantes
from routers.Services.services_representantes import update_representante as ur # ur = update_representante
from routers.Services.services_representantes import delete_representante as dr # dr = delete_representante

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/representantes")

@router.post("/", response_model=rs.RepresentanteRead)
def create_representante(session: sessionDep, payload: rs.RepresentanteCreate):
    return cr(session = session, representante_data = payload)

@router.get("/", response_model=list[rs.RepresentanteRead])
def read_representantes(session: sessionDep):
    return rr(session = session)

@router.patch("/{representante_id}", response_model=rs.RepresentanteRead)
def update_representante(representante_id: int, session: sessionDep, payload: rs.RepresentanteUpdatePartial):
    return ur(representante_id = representante_id, session = session, representante_data = payload)

@router.delete("/{representante_id}", response_model=rs.RepresentanteDelete)
def delete_representante(representante_id: int, session: sessionDep):
    return dr(representante_id = representante_id, session = session)