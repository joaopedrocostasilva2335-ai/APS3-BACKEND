from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from database import get_db
from schema.evento_schema import Evento, EventoCreate
from schema.participante_schema import Participante
from service import evento_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("", response_model=Evento, status_code=status.HTTP_201_CREATED)
def cadastrar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    return evento_service.criar(db, evento)


@router.get("", response_model=list[Evento])
def listar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar(db)


@router.get("/{evento_id}", response_model=Evento)
def consultar_evento(evento_id: int, db: Session = Depends(get_db)):
    return evento_service.buscar(db, evento_id)


@router.put("/{evento_id}", response_model=Evento)
def atualizar_evento(evento_id: int, evento: EventoCreate, db: Session = Depends(get_db)):
    return evento_service.atualizar(db, evento_id, evento)


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(evento_id: int, db: Session = Depends(get_db)):
    evento_service.excluir(db, evento_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{evento_id}/inscricoes/{participante_id}", status_code=status.HTTP_201_CREATED)
def inscrever_participante(evento_id: int, participante_id: int, db: Session = Depends(get_db)):
    return evento_service.inscrever(db, evento_id, participante_id)


@router.get("/{evento_id}/inscricoes", response_model=list[Participante])
def listar_inscritos(evento_id: int, db: Session = Depends(get_db)):
    return evento_service.listar_inscritos(db, evento_id)
