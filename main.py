import importlib
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from models.modelos import *
from sqlmodel import SQLModel
from database.connection import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

routers_dir = "routers"

for nombre_archivo in os.listdir(routers_dir):
    if nombre_archivo.endswith(".py") and nombre_archivo:
        module_name = nombre_archivo[:-3]
        module = importlib.import_module(f"{routers_dir}.{module_name}")
        
        if hasattr(module, "router"):
            tag_name = module_name.replace("_routers", "").replace("_", " ").title()
            app.include_router(module.router, tags=[f"{tag_name}"])