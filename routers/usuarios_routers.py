from fastapi import APIRouter, Depends
from schemas import usuarios_schemas as u # u = usuarios_schemas

from routers.Services.services_usuarios import create_usuario as cu # cu = create_usuario
from routers.Services.services_usuarios import read_usuarios as ru # ru = read_usuarios
from routers.Services.services_usuarios import update_usuario as uu # uu = update_usuario
from routers.Services.services_usuarios import delete_usuario as du # du = delete_usuario

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/usuarios")

@router.post("/", response_model=u.UsuarioRead)
def create_usuario(session: sessionDep, payload: u.UsuarioCreate):
    return cu(session = session, usuario_data = payload)

@router.get("/", response_model=list[u.UsuarioRead])
def read_usuarios(session: sessionDep):
    return ru(session = session)

@router.patch("/{usuario_id}", response_model=u.UsuarioRead)
def update_usuario(usuario_id: int, session: sessionDep, payload: u.UsuarioUpdatePartial):
    return uu(usuario_id = usuario_id, session = session, usuario_data = payload)

@router.delete("/{usuario_id}", response_model=u.UsuarioDelete)
def delete_usuario(usuario_id: int, session: sessionDep):
    return du(usuario_id = usuario_id, session = session)