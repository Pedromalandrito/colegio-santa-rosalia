from sqlmodel import Session, select
from models.modelos import Usuarios
from schemas import usuarios_schemas as u # u = usuarios_schemas
from fastapi import HTTPException

def create_usuario(session: Session, usuario_data: u.UsuarioCreate):
    if session.exec(select(Usuarios).where(Usuarios.nickname == usuario_data.nickname)).first():
        raise HTTPException(status_code=400, detail="El nickname ya está en uso")
    
    new_usuario = Usuarios(**usuario_data.model_dump())
    session.add(new_usuario)
    session.commit()
    session.refresh(new_usuario)
    return new_usuario

def read_usuarios(session: Session):
    return session.exec(select(Usuarios).where(Usuarios.is_active == True)).all()

def update_usuario(usuario_id: int, session: Session, usuario_data: u.UsuarioUpdatePartial):
    usuario = session.get(Usuarios, usuario_id)
    if not usuario or not usuario.is_active:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if usuario_data.nickname is not None:
        if session.exec(select(Usuarios).where(Usuarios.nickname == usuario_data.nickname, Usuarios.id != usuario_id)).first():
            raise HTTPException(status_code=400, detail="El nickname ya está en uso por otro usuario")

    datos_actualizados = usuario_data.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(usuario, campo, valor)
        
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def delete_usuario(usuario_id: int, session: Session):
    usuario = session.get(Usuarios, usuario_id)
    if not usuario or usuario.is_active == False:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.is_active = False
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario