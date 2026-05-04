from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos import Representantes
from database.connection import get_session
from schemas import representantes_schemas as rs # rs = representantes_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/representantes/", response_model=rs.RepresentanteCreate)
def create_representante(session: sessionDep, representante_data: rs.RepresentanteCreate):

    new_representante = Representantes(
        cedula_representante=representante_data.cedula_representante,
        nombre=representante_data.nombre,
        apellido=representante_data.apellido,
        telefono=representante_data.telefono,
        correo=representante_data.correo,
        direccion=representante_data.direccion,
        cedula_estudiante=representante_data.cedula_estudiante
    )
    session.add(new_representante)
    session.commit()
    session.refresh(new_representante)
    return new_representante

@router.get("/representantes/", response_model=list[rs.RepresentanteRead])
def read_representantes(session: sessionDep):
    representantes = session.exec(select(Representantes).where(Representantes.is_active == True)).all()
    return representantes

@router.patch("/representantes/{representante_id}", response_model=rs.RepresentanteUpdatePartial)
def update_representante(representante_id: int, session: sessionDep, representante_data: rs.RepresentanteUpdatePartial):
    representante = session.get(Representantes, representante_id)
    if not representante or not representante.is_active:
        raise HTTPException(status_code=404, detail="Representante no encontrado")
    if representante_data.nombre is not None:
        representante.nombre = representante_data.nombre
    if representante_data.apellido is not None:
        representante.apellido = representante_data.apellido
    if representante_data.telefono is not None:
        representante.telefono = representante_data.telefono
    if representante_data.correo is not None:
        representante.correo = representante_data.correo
    if representante_data.direccion is not None:
        representante.direccion = representante_data.direccion
    if representante_data.cedula_estudiante is not None:
        representante.cedula_estudiante = representante_data.cedula_estudiante
    session.add(representante)
    session.commit()
    session.refresh(representante)
    return representante

@router.delete("/representantes/{representante_id}", response_model=rs.RepresentanteDelete)
def delete_representante(representante_id: int, session: sessionDep):
    representante = session.get(Representantes, representante_id)
    if not representante or not representante.is_active:
        raise HTTPException(status_code=404, detail="Representante no encontrado")
    representante.is_active = False
    session.add(representante)
    session.commit()
    session.refresh(representante)
    return {"mensaje": "El representante ha sido desactivado exitosamente"}