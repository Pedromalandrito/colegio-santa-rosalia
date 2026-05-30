from sqlmodel import Session, select
from models.modelos import Permisos
from schemas import permisos_schemas as ps # ps = permisos_schemas
from fastapi import HTTPException

def create_permiso(session: Session, permiso_data: ps.PermisoCreate):
    new_permiso = Permisos(descripcion=permiso_data.descripcion)
    session.add(new_permiso)
    session.commit()
    session.refresh(new_permiso)
    return new_permiso

def read_permisos(session: Session):
    return session.exec(select(Permisos).where(Permisos.is_active == True)).all()

def update_permiso(permiso_id: int, session: Session, permiso_data: ps.PermisoUpdate):
    permiso = session.get(Permisos, permiso_id)
    if not permiso or not permiso.is_active:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    
    if permiso_data.descripcion is not None:
        permiso.descripcion = permiso_data.descripcion
        
    session.add(permiso)
    session.commit()
    session.refresh(permiso)
    return permiso

def delete_permiso(permiso_id: int, session: Session):
    permiso = session.get(Permisos, permiso_id)
    if not permiso or not permiso.is_active:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    permiso.is_active = False
    session.add(permiso)
    session.commit()
    session.refresh(permiso)
    return permiso