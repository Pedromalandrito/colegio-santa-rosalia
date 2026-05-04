from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, col, func, Integer, or_
from db_models.models import Paciente
from database.connection import get_session
from schemas import pacientes_schema as ps # ps = pacientes schemas

from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter()

@router.post("/pacientes")
def create_pacientes(session: sessionDep, paciente_data: ps.PacienteCreate):
    for nombre_campo, valor in paciente_data.model_dump().items():
        if not valor or str(valor).strip() == "":
            raise HTTPException(status_code=400, detail=f"El campo {nombre_campo} no puede estar vacío")
        
    new_paciente = Paciente(
            cedula = paciente_data.cedula,
            nombre = paciente_data.nombre,
            celular = paciente_data.celular,
            tipo_sangre = paciente_data.tipo_sangre
            )
    existe_cedula = session.exec(select(Paciente).where(Paciente.cedula == paciente_data.cedula)).first()
    if existe_cedula:
            raise HTTPException(status_code=400, detail="Esta cedula ya esta siendo utilizada por otro Paciente")

    session.add(new_paciente)
    session.commit()
    session.refresh(new_paciente)
    return new_paciente

@router.get("/pacientes", response_model=list[ps.PacienteGet])
def get_pacientes_filtrado(session: sessionDep, busqueda: str | None = None, tipo_sangre: str | None = None):
     estado = select(Paciente).where(Paciente.is_active == True)
     if busqueda:
        patron = f"%{busqueda}%"
        estado = estado.where(
            or_(
                col(Paciente.cedula).ilike(patron),
                col(Paciente.nombre).ilike(patron),
                col(Paciente.celular).ilike(patron),
                col(Paciente.tipo_sangre).ilike(patron)
            )
        )
    
     estado = estado.order_by(func.cast(col(Paciente.cedula), Integer).asc())

     pacientes = session.exec(estado).all()
     return pacientes

@router.put("/pacientes/{cedula}")
def update_pacientes(session: sessionDep, cedula: str, paciente_data: ps.PacienteUpdate):
    paciente = session.get(Paciente, cedula)

    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    campos_editables = {
        "cedula": paciente_data.cedula,
        "nombre": paciente_data.nombre,
        "celular": paciente_data.celular,
        "tipo_sangre": paciente_data.tipo_sangre
    }

    for nombre_campo, valor in campos_editables.items():
        if not valor or str(valor).strip() == "":
            raise HTTPException(status_code=400, detail=f"El campo {nombre_campo} no puede estar vacío")
        
        if nombre_campo == "cedula" and valor != cedula:
            existe = session.exec(select(Paciente).where(Paciente.cedula == valor)).first()
            if existe:
                raise HTTPException(status_code=400, detail=f"La cedula {valor} ya está en uso")
        
        setattr(paciente, nombre_campo, valor)

    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


@router.patch("/pacientes/{cedula}")
def updatePartial_pacientes(session: sessionDep, cedula: str, paciente_data: ps.PacienteUpdatePartial):
    paciente = session.get(Paciente, cedula)

    if paciente is None:
          raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    campos_editables = {"cedula" : paciente_data.cedula,
                        "nombre": paciente_data.nombre,
                        "celular": paciente_data.celular,
                        "tipo_sangre": paciente_data.tipo_sangre}
    
    for nombre_campo, valor in campos_editables.items():
         if valor is not None:
              if str(valor).strip() == "":
                   raise HTTPException(status_code=400, detail=f"El Campo {nombre_campo} No puede estar vacío")
              
              if nombre_campo == "cedula" and valor != cedula:
                   existe = session.exec(select(Paciente).where(Paciente.cedula == valor)).first()
                   if existe:
                        raise HTTPException(status_code=400, detail= f"La Cedula {valor} Ya esta siendo usada por otro Paciente")
              
              setattr(paciente, nombre_campo, valor)

    session.commit()
    session.refresh(paciente)
    return paciente

@router.delete("/paciente/{cedula}")
def delete_paciente(session: sessionDep, cedula: str, tipo_delete: bool):
    paciente = session.get(Paciente, cedula)

    if not paciente:
         raise HTTPException(status_code=404, detail="Que va a borrar si no hay nada bobo?")
    
    if tipo_delete == False:
         paciente.is_active = False
         session.add(paciente)
         session.commit()
         session.refresh(paciente)
         return{"mensaje":"borrado de forma logica"}
    else:
         session.delete(paciente)
         session.commit()
         return{"mensaje":"borrado de forma fisica"}