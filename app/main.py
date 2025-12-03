
from starlette.middleware.cors import CORSMiddleware

from .database import engine, Base
from fastapi import FastAPI
from api import clientes, medidores, lecturas, boletas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CGE", description="API para gestionar clientes, medidores, lecturas, boletas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8100"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.clientes_api)
app.include_router(medidores.medidores_api)
app.include_router(lecturas.lecturas_api)
app.include_router(boletas.boletas_api)