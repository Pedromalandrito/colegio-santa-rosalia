from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos import MetodosPago
from database.connection import get_session
from schemas import metodospago_schemas as mp # mp = metodospago_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/metodospago/", response_model=mp.CreateMetodoPago)
def create_metodopago(session: sessionDep, metodopago_data: mp.CreateMetodoPago):
    new_metodopago = MetodosPago(descripcion=metodopago_data.descripcion)
    session.add(new_metodopago)
    session.commit()
    session.refresh(new_metodopago)
    return new_metodopago

@router.get("/metodospago/", response_model=list[mp.ReadMetodoPago])
def read_metodospago(session: sessionDep):
    metodospago = session.exec(select(MetodosPago).where(MetodosPago.is_active == True)).all()
    return metodospago

@router.put("/metodospago/{metodopago_id}", response_model=mp.UpdateMetodoPago)
def update_metodopago(metodopago_id: int, session: sessionDep, metodopago_data: mp.UpdateMetodoPago):
    metodopago = session.get(MetodosPago, metodopago_id)
    if not metodopago or not metodopago.is_active:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    metodopago.descripcion = metodopago_data.descripcion
    session.add(metodopago)
    session.commit()
    session.refresh(metodopago)
    return metodopago

@router.delete("/metodospago/{metodopago_id}", response_model=mp.DeleteMetodoPago)
def delete_metodopago(metodopago_id: int, session: sessionDep):
    metodopago = session.get(MetodosPago, metodopago_id)
    if not metodopago or not metodopago.is_active:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    metodopago.is_active = False
    session.add(metodopago)
    session.commit()
    session.refresh(metodopago)
    return {"mensaje": "El método de pago ha sido desactivado exitosamente"}