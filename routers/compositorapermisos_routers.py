from fastapi import APIRouter, Depends
from schemas import compositorapermisos_schemas as cps # cps = compositorapermisos_schemas

from routers.Services.services_compositorapermisos import create_compositorapermisos as ccp # ccp = Create_compositorapermisos
from routers.Services.services_compositorapermisos import read_compositorapermisos as rcp # rcp = read_compositorapermisos

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter(prefix="/compositorapermisos")

@router.post("/", response_model=cps.CompositoraPermisosBase)
def create_compositorapermisos(session: sessionDep, payload: cps.CompositoraPermisosBase):
    return ccp(session = session, compositorapermisos_data = payload)

@router.get("/", response_model=list[cps.CompositoraPermisosBase])
def read_compositorapermisos(session: sessionDep):
    return rcp(session = session)