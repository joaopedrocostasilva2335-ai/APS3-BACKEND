from fastapi import HTTPException
from database import salvar
from model.participante import Participante
from schema.participante_schema import ParticipanteCreate

MSG_EMAIL = "Já existe um participante cadastrado com este e-mail."


def listar(db):
    return db.query(Participante).all()


def buscar(db, participante_id: int) -> Participante:
    participante = db.get(Participante, participante_id)
    if not participante:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    return participante


def _verificar_email(db, email: str, ignorar_id: int = None):
    consulta = db.query(Participante).filter(Participante.email == email)
    if ignorar_id:
        consulta = consulta.filter(Participante.id != ignorar_id)
    if consulta.first():
        raise HTTPException(status_code=409, detail=MSG_EMAIL)


def criar(db, dados: ParticipanteCreate) -> Participante:
    _verificar_email(db, dados.email)
    novo = Participante(**dados.model_dump())
    db.add(novo)
    salvar(db, MSG_EMAIL)
    db.refresh(novo)
    return novo


def atualizar(db, participante_id: int, dados: ParticipanteCreate) -> Participante:
    existente = buscar(db, participante_id)
    _verificar_email(db, dados.email, participante_id)
    for campo, valor in dados.model_dump().items():
        setattr(existente, campo, valor)
    salvar(db, MSG_EMAIL)
    db.refresh(existente)
    return existente


def excluir(db, participante_id: int):
    from service import evento_service
    participante = buscar(db, participante_id)
    evento_service.remover_inscricoes_do_participante(db, participante_id)
    db.delete(participante)
    salvar(db)
