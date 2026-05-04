from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos import Pagos
from database.connection import get_session
from schemas import pagos_schemas as ps # ps = pagos_schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/pagos/", response_model=ps.PagosCreate)
def create_pago(session: sessionDep, pago_data: ps.PagosCreate):
    new_pago = Pagos(
        cedula_estudiante=pago_data.cedula_estudiante,
        monto=pago_data.monto,
        mes_correspondiente=pago_data.mes_correspondiente,
        anio_correspondiente=pago_data.anio_correspondiente,
        metodo_pago=pago_data.metodo_pago,
        referencia_pago=pago_data.referencia_pago
    )
    session.add(new_pago)
    session.commit()
    session.refresh(new_pago)
    return new_pago

@router.get("/pagos/", response_model=list[ps.PagosRead])
def read_pagos(session: sessionDep):
    pagos = session.exec(select(Pagos).where(Pagos.is_active == True)).all()
    return pagos

@router.patch("/pagos/{pago_id}", response_model=ps.PagosUpdatePartial)
def update_pago(pago_id: int, session: sessionDep, pago_data: ps.PagosUpdatePartial):
    pago = session.get(Pagos, pago_id)
    if not pago or not pago.is_active:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    if pago_data.mes_correspondiente is not None:
        pago.mes_correspondiente = pago_data.mes_correspondiente
    if pago_data.anio_correspondiente is not None:
        pago.anio_correspondiente = pago_data.anio_correspondiente
    if pago_data.metodo_pago is not None:
        pago.metodo_pago = pago_data.metodo_pago
    if pago_data.referencia_pago is not None:
        pago.referencia_pago = pago_data.referencia_pago
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return pago

@router.delete("/pagos/{pago_id}", response_model=ps.PagosDelete)
def delete_pago(pago_id: int, session: sessionDep):
    pago = session.get(Pagos, pago_id)
    if not pago or not pago.is_active:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    pago.is_active = False
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return {"mensaje": "El pago ha sido desactivado exitosamente"}