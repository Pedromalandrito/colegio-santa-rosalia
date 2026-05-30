from sqlmodel import Session, select
from models.modelos import CompositoraPermisos
from schemas import compositorapermisos_schemas as cps # cps = compositorapermisos_schemas


def create_compositorapermisos(session: Session, compositorapermisos_data: cps.CompositoraPermisosBase):

    new_compositorapermisos = CompositoraPermisos(**compositorapermisos_data.model_dump())
    session.add(new_compositorapermisos)
    session.commit()
    session.refresh(new_compositorapermisos)
    return new_compositorapermisos


def read_compositorapermisos(session: Session):
    return session.exec(select(CompositoraPermisos)).all()