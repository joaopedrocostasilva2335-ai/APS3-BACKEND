from sqlalchemy import func
from model.evento import Evento
from model.inscricao import Inscricao
from model.participante import Participante


def ocupacao_eventos(db):
    linhas = (
        db.query(Evento.id, Evento.titulo, Evento.capacidade, func.count(Inscricao.id))
        .outerjoin(Inscricao, Inscricao.evento_id == Evento.id)
        .group_by(Evento.id)
        .all()
    )
    resultado = []
    for evento_id, titulo, capacidade, inscritos in linhas:
        percentual = round(inscritos / capacidade * 100, 2) if capacidade else 0.0
        resultado.append({
            "evento_id": evento_id,
            "titulo": titulo,
            "capacidade": capacidade,
            "total_inscritos": inscritos,
            "vagas_disponiveis": capacidade - inscritos,
            "percentual_ocupacao": percentual,
        })
    return resultado


def eventos_por_categoria(db):
    por_evento = (
        db.query(Inscricao.evento_id.label("evento_id"), func.count(Inscricao.id).label("total"))
        .group_by(Inscricao.evento_id)
        .subquery()
    )
    linhas = (
        db.query(
            Evento.categoria,
            func.count(Evento.id),
            func.sum(Evento.capacidade),
            func.sum(func.coalesce(por_evento.c.total, 0)),
        )
        .outerjoin(por_evento, por_evento.c.evento_id == Evento.id)
        .group_by(Evento.categoria)
        .all()
    )
    return [
        {
            "categoria": categoria,
            "total_eventos": total_eventos,
            "capacidade_total": capacidade or 0,
            "total_inscricoes": inscricoes or 0,
        }
        for categoria, total_eventos, capacidade, inscricoes in linhas
    ]


def participacao_por_curso(db):
    linhas = (
        db.query(
            Participante.curso,
            func.count(func.distinct(Participante.id)),  
            func.count(Inscricao.id),
        )
        .outerjoin(Inscricao, Inscricao.participante_id == Participante.id)
        .group_by(Participante.curso)
        .all()
    )
    return [
        {"curso": curso, "total_participantes": participantes, "total_inscricoes": inscricoes}
        for curso, participantes, inscricoes in linhas
    ]
