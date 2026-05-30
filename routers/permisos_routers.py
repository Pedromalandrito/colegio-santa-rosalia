from fastapi import APIRouter, Depends
from schemas import permisos_schemas as ps # ps = permisos_schemas

from routers.Services.services_permisos import create_permiso as cp # cp = create_permiso
from routers.Services.services_permisos import read_permisos as rp # rp = read_permisos
from routers.Services.services_permisos import update_permiso as up # up = update_permiso
from routers.Services.services_permisos import delete_permiso as dp # dp = delete_permiso

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/permisos")

@router.post("/", response_model=ps.PermisoRead)
def create_permiso(session: sessionDep, payload: ps.PermisoCreate):
    return cp(session = session, permiso_data = payload)

@router.get("/", response_model=list[ps.PermisoRead])
def read_permisos(session: sessionDep):
    return rp(session = session)

@router.put("/{permiso_id}", response_model=ps.PermisoRead)
def update_permiso(permiso_id: int, session: sessionDep, payload: ps.PermisoUpdate):
    return up(permiso_id = permiso_id, session = session, permiso_data = payload)

@router.delete("/{permiso_id}", response_model=ps.PermisoDelete)
def delete_permiso(permiso_id: int, session: sessionDep):
    return dp(permiso_id = permiso_id, session = session)