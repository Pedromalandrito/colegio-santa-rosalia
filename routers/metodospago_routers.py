from fastapi import APIRouter, Depends
from schemas import metodospago_schemas as mp # mp = metodospago_schemas

from routers.Services.services_metodospago import create_metodopago as cmp # cmp = create_metodopago
from routers.Services.services_metodospago import read_metodospago as rmp # rmp = read_metodospago
from routers.Services.services_metodospago import update_metodopago as ump # ump = update_metodopago
from routers.Services.services_metodospago import delete_metodopago as dmp # dmp = delete_metodopago

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/metodospago")

@router.post("/", response_model=mp.ReadMetodoPago)
def create_metodopago(session: sessionDep, payload: mp.CreateMetodoPago):
    return cmp(session = session, metodopago_data = payload)

@router.get("/", response_model=list[mp.ReadMetodoPago])
def read_metodospago(session: sessionDep):
    return rmp(session = session)

@router.put("/{metodopago_id}", response_model=mp.ReadMetodoPago)
def update_metodopago(metodopago_id: int, session: sessionDep, payload: mp.UpdateMetodoPago):
    return ump(metodopago_id = metodopago_id, session = session, metodopago_data = payload)

@router.delete("/{metodopago_id}", response_model=mp.DeleteMetodoPago)
def delete_metodopago(metodopago_id: int, session: sessionDep):
    return dmp(metodopago_id = metodopago_id, session = session)