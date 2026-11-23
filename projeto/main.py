from fastapi import FastAPI
from database import Base, engine
from model import evento, participante, inscricao  # noqa: F401 (registra as tabelas)
from controller import evento_controller, participante_controller, relatorio_controller

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Eventos Acadêmicos")

app.include_router(evento_controller.router)
app.include_router(participante_controller.router)
app.include_router(relatorio_controller.router)
