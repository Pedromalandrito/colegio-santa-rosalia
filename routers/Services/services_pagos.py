from sqlmodel import Session, select
from models.modelos import Pagos
from schemas import pagos_schemas as ps # ps = pagos_schemas
from fastapi import HTTPException

def create_pago(session: Session, pago_data: ps.PagosCreate):
    new_pago = Pagos(**pago_data.model_dump())
    session.add(new_pago)
    session.commit()
    session.refresh(new_pago)
    return new_pago

def read_pagos(session: Session):
    return session.exec(select(Pagos).where(Pagos.is_active == True)).all()

def update_pago(pago_id: int, session: Session, pago_data: ps.PagosUpdatePartial):
    pago = session.get(Pagos, pago_id)
    if not pago or not pago.is_active:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    datos_actualizados = pago_data.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(pago, campo, valor)
        
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return pago

def delete_pago(pago_id: int, session: Session):
    pago = session.get(Pagos, pago_id)
    if not pago or not pago.is_active:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    pago.is_active = False
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return pago