from sqlmodel import Session, select
from models.modelos import MetodosPago
from schemas import metodospago_schemas as mp # mp = metodospago_schemas
from fastapi import HTTPException

def create_metodopago(session: Session, metodopago_data: mp.CreateMetodoPago):
    new_metodopago = MetodosPago(descripcion=metodopago_data.descripcion)
    session.add(new_metodopago)
    session.commit()
    session.refresh(new_metodopago)
    return new_metodopago

def read_metodospago(session: Session):
    return session.exec(select(MetodosPago).where(MetodosPago.is_active == True)).all()

def update_metodopago(metodopago_id: int, session: Session, metodopago_data: mp.UpdateMetodoPago):
    metodopago = session.get(MetodosPago, metodopago_id)
    if not metodopago or not metodopago.is_active:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    
    if metodopago_data.descripcion is not None:
        metodopago.descripcion = metodopago_data.descripcion
        
    session.add(metodopago)
    session.commit()
    session.refresh(metodopago)
    return metodopago

def delete_metodopago(metodopago_id: int, session: Session):
    metodopago = session.get(MetodosPago, metodopago_id)
    if not metodopago or not metodopago.is_active:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    metodopago.is_active = False
    session.add(metodopago)
    session.commit()
    session.refresh(metodopago)
    return metodopago