# API de Eventos Acadêmicos — APS 3

API RESTful (FastAPI) para gerenciar eventos, participantes e inscrições. Evolução da APS 2

## Instalação
```bash
python -m venv venv
venv\Scripts\activate        # Windows (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
```

## Execução
```bash
uvicorn main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

## Estrutura
```
projeto/
├── main.py            # cria o app, as tabelas e registra as rotas
├── database.py        # conexão SQLite, sessões (get_db) e função salvar()
├── controller/        # rotas HTTP (evento, participante, relatorio)
├── model/             # tabelas SQLAlchemy (Evento, Participante, Inscricao)
├── schema/            # validação e respostas (Pydantic)
├── service/           # regras de negócio, persistência e relatórios
├── requirements.txt
└── README.md
```

## Banco de dados
- Arquivo `eventos.db`, criado automaticamente na pasta do projeto ao iniciar a aplicação.
- As tabelas são criadas a partir dos models (`Base.metadata.create_all`).
- Cada requisição abre uma sessão (`get_db`) que é fechada ao final.
- `Inscricao` liga `Evento` e `Participante` (chaves estrangeiras + `relationship`) e tem
  `UniqueConstraint(evento_id, participante_id)` contra inscrição duplicada.
- `Participante.email` é único.
- Para zerar os dados, apague o arquivo `eventos.db`.

## Principais rotas
| Método | Rota | Descrição |
|---|---|---|
| POST / GET | `/eventos` | cadastrar / listar eventos |
| GET / PUT / DELETE | `/eventos/{id}` | consultar / atualizar / excluir |
| POST / GET | `/participantes` | cadastrar / listar participantes |
| GET / PUT / DELETE | `/participantes/{id}` | consultar / atualizar / excluir |
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | inscrever participante |
| GET | `/eventos/{evento_id}/inscricoes` | participantes inscritos no evento |
| GET | `/relatorios/eventos/ocupacao` | ocupação por evento |
| GET | `/relatorios/eventos/categorias` | consolidado por categoria |
| GET | `/relatorios/participantes/cursos` | consolidado por curso |

## Regras e erros
- 404: evento ou participante não encontrado.
- 409: e-mail já cadastrado, inscrição duplicada, evento sem vagas.
- 400: capacidade menor que o número de inscritos ao atualizar um evento.
- 422: dados inválidos (título/nome vazio, e-mail inválido, capacidade <= 0, data/hora ou categoria inválidas).
- Excluir um evento ou participante também **exclui suas inscrições**, sem deixar registros órfãos.
- Falhas do banco retornam mensagens genéricas, sem detalhes técnicos.

## Relatórios
Calculados dinamicamente com consultas SQLAlchemy (JOIN, GROUP BY, COUNT, SUM), sem valores fixos.
- **Ocupação**: id, título, capacidade, total de inscritos, vagas disponíveis e percentual
  (eventos sem inscrição aparecem com 0%, sem divisão por zero).
- **Categorias**: total de eventos, capacidade total e total de inscrições por categoria.
- **Cursos**: total de participantes (sem repetir) e total de inscrições por curso.

## Exemplos
```json
POST /eventos
{"titulo": "Workshop de Python", "descricao": "Introdução", "data": "2026-12-01",
 "horario": "14:00:00", "local": "Sala 1", "capacidade": 40, "categoria": "Workshop"}

POST /participantes
{"nome": "Ana", "email": "ana@email.com", "curso": "Engenharia de Software"}

POST /eventos/1/inscricoes/1   ->  201
{"mensagem": "Inscrição realizada com sucesso.", "evento": "Workshop de Python", "participante": "Ana"}

GET /relatorios/eventos/ocupacao
[{"evento_id": 1, "titulo": "Workshop de Python", "capacidade": 40,
  "total_inscritos": 1, "vagas_disponiveis": 39, "percentual_ocupacao": 2.5}]
```

## Como reproduzir os testes (Swagger em /docs)
1. Cadastrar e consultar eventos e participantes.
2. Atualizar e excluir registros.
3. Inscrever um participante; repetir a inscrição (409); usar evento inexistente (404);
   criar evento com capacidade 1 e inscrever dois participantes (409 sem vagas).
4. Parar o servidor, iniciar de novo e chamar `GET /eventos` (dados mantidos).
5. Consultar os três relatórios, fazer novas inscrições/atualizações/exclusões e consultá-los
   de novo para ver os valores mudarem.
