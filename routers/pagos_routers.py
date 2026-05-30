from fastapi import APIRouter, Depends
from schemas import pagos_schemas as ps # ps = pagos_schemas

from routers.Services.services_pagos import create_pago as cp # cp = create_pago
from routers.Services.services_pagos import read_pagos as rp # rp = read_pagos
from routers.Services.services_pagos import update_pago as up # up = update_pago
from routers.Services.services_pagos import delete_pago as dp # dp = delete_pago

from sqlmodel import Session
from database.connection import get_session
from typing import Annotated
sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/pagos")

@router.post("/", response_model=ps.PagosRead)
def create_pago(session: sessionDep, payload: ps.PagosCreate):
    return cp(session = session, pago_data = payload)

@router.get("/", response_model=list[ps.PagosRead])
def read_pagos(session: sessionDep):
    return rp(session = session)

@router.patch("/{pago_id}", response_model=ps.PagosRead)
def update_pago(pago_id: int, session: sessionDep, payload: ps.PagosUpdatePartial):
    return up(pago_id = pago_id, session = session, pago_data = payload)

@router.delete("/{pago_id}", response_model=ps.PagosDelete)
def delete_pago(pago_id: int, session: sessionDep):
    return dp(pago_id = pago_id, session = session)