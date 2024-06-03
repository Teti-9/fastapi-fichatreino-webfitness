from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infra.sqlalchemy.config.database import gerar_db
from src.routers import rotas

# gerar_db()

app = FastAPI()

app.add_middleware(CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],)

app.include_router(rotas.router)