# TrabalhoPY
# Helpdesk API

API REST desenvolvida em Python utilizando Flask, SQLAlchemy e SQLite.

O projeto foi desenvolvido utilizando arquitetura em camadas, separando as responsabilidades entre Controllers, Services, Repositories e Models.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite

## Estrutura do projeto

```text
helpdesk/
│
├── controllers/
│   ├── __init__.py
│   ├── usuario_controller.py
│   └── chamado_controller.py
│
├── services/
│   ├── __init__.py
│   ├── usuario_service.py
│   └── chamado_service.py
│
├── repositories/
│   ├── __init__.py
│   ├── usuario_repository.py
│   └── chamado_repository.py
│
├── models/
│   ├── __init__.py
│   ├── usuario.py
│   └── chamado.py
│
├── database.py
├── app.py
├── requirements.txt
├── README.md
└── helpdesk.db
