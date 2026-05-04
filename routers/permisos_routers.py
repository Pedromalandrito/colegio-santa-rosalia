from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos import Permisos
from database.connection import get_session
from schemas import permisos_schemas as ps # ps = permisos_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/permisos/", response_model=ps.PermisoCreate)
def create_permiso(session: sessionDep, permiso_data: ps.PermisoCreate):
    new_permiso = Permisos(descripcion=permiso_data.descripcion)
    session.add(new_permiso)
    session.commit()
    session.refresh(new_permiso)
    return new_permiso

@router.get("/permisos/", response_model=list[ps.PermisoRead])
def read_permisos(session: sessionDep):
    permisos = session.exec(select(Permisos).where(Permisos.is_active == True)).all()
    return permisos

@router.put("/permisos/{permiso_id}", response_model=ps.PermisoUpdate)
def update_permiso(permiso_id: int, session: sessionDep, permiso_data: ps.PermisoUpdate):
    permiso = session.get(Permisos, permiso_id)
    if not permiso or not permiso.is_active:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    permiso.descripcion = permiso_data.descripcion
    session.add(permiso)
    session.commit()
    session.refresh(permiso)
    return permiso

@router.delete("/permisos/{permiso_id}", response_model=ps.PermisoDelete)
def delete_permiso(permiso_id: int, session: sessionDep):
    permiso = session.get(Permisos, permiso_id)
    if not permiso or not permiso.is_active:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    permiso.is_active = False
    session.add(permiso)
    session.commit()
    session.refresh(permiso)
    return {"mensaje": "El permiso ha sido desactivado exitosamente"}