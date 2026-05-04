import importlib
import os
from fastapi import FastAPI
from models.modelos import *
from sqlmodel import SQLModel
from database.connection import engine

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

routers_dir = "routers"

for nombre_archivo in os.listdir(routers_dir):
    if nombre_archivo.endswith(".py") and nombre_archivo != "__init__.py":
        module_name = nombre_archivo[:-3]
        module = importlib.import_module(f"{routers_dir}.{module_name}")
        
        if hasattr(module, "router"):
            tag_name = module_name.replace("_routers", "").replace("_", " ").title()
            app.include_router(module.router, tags=[f"Endpoints {tag_name}"])