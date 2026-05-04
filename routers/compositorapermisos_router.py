from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models.modelos import CompositoraPermisos
from database.connection import get_session
from schemas import compositorapermisos_schemas as cps # cps = compositorapermisos_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/compositorapermisos", response_model=cps.CompositorapermisosCreate)
def create_compositorapermisos(session: sessionDep, compositorapermisos_data: cps.CompositorapermisosCreate):
    new_compositorapermisos = CompositoraPermisos(
        usuario_id=compositorapermisos_data.usuario_id,
        permiso_id=compositorapermisos_data.permiso_id
    )
    session.add(new_compositorapermisos)
    session.commit()
    session.refresh(new_compositorapermisos)
    return new_compositorapermisos

@router.get("/compositorapermisos", response_model=list[cps.CompositorapermisosRead])
def read_compositorapermisos(session: sessionDep):
    compositorapermisos = session.exec(select(CompositoraPermisos)).all()
    return compositorapermisos