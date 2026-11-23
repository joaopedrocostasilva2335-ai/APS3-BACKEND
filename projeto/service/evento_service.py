from fastapi import HTTPException
from database import salvar
from model.evento import Evento
from model.inscricao import Inscricao
from schema.evento_schema import EventoCreate
from service import participante_service


def listar(db):
    return db.query(Evento).all()


def buscar(db, evento_id: int) -> Evento:
    evento = db.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    return evento


def _total_inscritos(db, evento_id: int) -> int:
    return db.query(Inscricao).filter(Inscricao.evento_id == evento_id).count()


def criar(db, dados: EventoCreate) -> Evento:
    novo = Evento(**dados.model_dump())
    db.add(novo)
    salvar(db)
    db.refresh(novo)
    return novo


def atualizar(db, evento_id: int, dados: EventoCreate) -> Evento:
    existente = buscar(db, evento_id)
    if dados.capacidade < _total_inscritos(db, evento_id):
        raise HTTPException(
            status_code=400,
            detail="A capacidade não pode ser menor que o número de inscritos.",
        )
    for campo, valor in dados.model_dump().items():
        setattr(existente, campo, valor)
    salvar(db)
    db.refresh(existente)
    return existente


def excluir(db, evento_id: int):
    evento = buscar(db, evento_id)
    db.query(Inscricao).filter(Inscricao.evento_id == evento_id).delete()
    db.delete(evento)
    salvar(db)


def remover_inscricoes_do_participante(db, participante_id: int):
    db.query(Inscricao).filter(Inscricao.participante_id == participante_id).delete()


MSG_DUPLICADA = "Participante já está inscrito neste evento."


def inscrever(db, evento_id: int, participante_id: int):
    evento = buscar(db, evento_id)                                       # 1. evento existe?
    participante = participante_service.buscar(db, participante_id)      # 2. participante existe?

    ja_inscrito = db.query(Inscricao).filter(
        Inscricao.evento_id == evento_id,
        Inscricao.participante_id == participante_id,
    ).first()
    if ja_inscrito:                                                      # 3. já inscrito?
        raise HTTPException(status_code=409, detail=MSG_DUPLICADA)

    if _total_inscritos(db, evento_id) >= evento.capacidade:             # 4. há vagas?
        raise HTTPException(
            status_code=409, detail="Não existem vagas disponíveis para este evento."
        )

    db.add(Inscricao(evento_id=evento_id, participante_id=participante_id))
    salvar(db, MSG_DUPLICADA)
    return {
        "mensagem": "Inscrição realizada com sucesso.",
        "evento": evento.titulo,
        "participante": participante.nome,
    }


def listar_inscritos(db, evento_id: int):
    evento = buscar(db, evento_id)
    return [i.participante for i in evento.inscricoes]
