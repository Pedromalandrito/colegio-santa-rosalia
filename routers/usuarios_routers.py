from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos import Usuarios
from database.connection import get_session
from schemas import usuarios_schemas as u # u = usuarios_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/usuarios/", response_model=u.UsuarioCreate)
def create_usuario(session: sessionDep, usuario_data: u.UsuarioCreate):

    if session.exec(select(Usuarios).where(Usuarios.nickname == usuario_data.nickname)).first():
        raise HTTPException(status_code=400, detail="El nickname ya está en uso")

    new_usuario = Usuarios(
        nickname=usuario_data.nickname,
        clave=usuario_data.clave,
        pregunta1=usuario_data.pregunta1,
        respuesta1=usuario_data.respuesta1,
        pregunta2=usuario_data.pregunta2,
        respuesta2=usuario_data.respuesta2
    )
    session.add(new_usuario)
    session.commit()
    session.refresh(new_usuario)
    return new_usuario

@router.get("/usuarios/", response_model=list[u.UsuarioRead])
def read_usuarios(session: sessionDep):
    usuarios = session.exec(select(Usuarios).where(Usuarios.is_active == True)).all()
    return usuarios

@router.patch("/usuarios/{usuario_id}", response_model=u.UsuarioUpdatePartial)
def update_usuario(usuario_id: int, session: sessionDep, usuario_data: u.UsuarioUpdatePartial):
    usuario = session.get(Usuarios, usuario_id)
    if not usuario or not usuario.is_active:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario_data.nickname is not None:
        if session.exec(select(Usuarios).where(Usuarios.nickname == usuario_data.nickname, Usuarios.id != usuario_id)).first():
            raise HTTPException(status_code=400, detail="El nickname ya está en uso por otro usuario")
        usuario.nickname = usuario_data.nickname
    if usuario_data.clave is not None:
        usuario.clave = usuario_data.clave
    if usuario_data.pregunta1 is not None:
        usuario.pregunta1 = usuario_data.pregunta1
    if usuario_data.respuesta1 is not None:
        usuario.respuesta1 = usuario_data.respuesta1
    if usuario_data.pregunta2 is not None:
        usuario.pregunta2 = usuario_data.pregunta2
    if usuario_data.respuesta2 is not None:
        usuario.respuesta2 = usuario_data.respuesta2
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.delete("/usuarios/{usuario_id}", response_model=u.UsuarioDelete)
def delete_usuario(usuario_id: int, session: sessionDep):
    usuario = session.get(Usuarios, usuario_id)
    if not usuario or not usuario.is_active:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.is_active = False
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return {"mensaje": "El usuario ha sido desactivado exitosamente"}