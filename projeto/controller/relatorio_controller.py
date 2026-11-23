from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from service import relatorio_service

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/eventos/ocupacao")
def relatorio_ocupacao(db: Session = Depends(get_db)):
    return relatorio_service.ocupacao_eventos(db)


@router.get("/eventos/categorias")
def relatorio_categorias(db: Session = Depends(get_db)):
    return relatorio_service.eventos_por_categoria(db)


@router.get("/participantes/cursos")
def relatorio_cursos(db: Session = Depends(get_db)):
    return relatorio_service.participacao_por_curso(db)
