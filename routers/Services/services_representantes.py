from sqlmodel import Session, select
from models.modelos import Representantes
from schemas import representantes_schemas as rs # rs = representantes_schemas
from fastapi import HTTPException

def create_representante(session: Session, representante_data: rs.RepresentanteCreate):
    new_representante = Representantes(**representante_data.model_dump())
    session.add(new_representante)
    session.commit()
    session.refresh(new_representante)
    return new_representante

def read_representantes(session: Session):
    return session.exec(select(Representantes).where(Representantes.is_active == True)).all()

def update_representante(representante_id: int, session: Session, representante_data: rs.RepresentanteUpdatePartial):
    representante = session.get(Representantes, representante_id)
    if not representante or not representante.is_active:
        raise HTTPException(status_code=404, detail="Representante no encontrado")
    
    datos_actualizados = representante_data.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(representante, campo, valor)
        
    session.add(representante)
    session.commit()
    session.refresh(representante)
    return representante

def delete_representante(representante_id: int, session: Session):
    representante = session.get(Representantes, representante_id)
    if not representante or not representante.is_active:
        raise HTTPException(status_code=404, detail="Representante no encontrado")
    representante.is_active = False
    session.add(representante)
    session.commit()
    session.refresh(representante)
    return representante