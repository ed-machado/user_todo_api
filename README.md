# User Todo API

## Descrição do Projeto

Aplicação construída com FastAPI com funcionalidades de gerenciamento de tarefas (To-Do) e autenticação de usuários.

- **Branch `main`:** Utiliza PostgreSQL via Docker.
- **Branch `develop`:** Utiliza SQLite para desenvolvimento local.

O projeto inclui testes unitários e já vem com o banco de dados configurado, eliminando a necessidade de migrações iniciais manuais.

## Funcionalidades

- **Gerenciamento de Tarefas (To-Do)**
  - Criar tarefas (somente usuários autenticados)
  - Listar tarefas do próprio usuário
  - Atualizar tarefas do próprio usuário
  - Deletar tarefas do próprio usuário

- **Gerenciamento de Usuários**
  - Registro de novos usuários
  - Login de usuários
  - Alteração dos dados pessoais
  - Deleção de contas de usuário

## Tecnologias Utilizadas

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Migrações de Banco de Dados**: Alembic
- **Banco de Dados**: PostgreSQL (produção na `main`) / SQLite (desenvolvimento na `develop`)
- **Gerenciador de Dependências**: Poetry
- **Servidor ASGI**: Uvicorn
- **Testes**: Pytest
- **Deploy**: Docker

## Documentação da API

A **User Todo API** utiliza a documentação automática do **FastAPI**, que pode ser acessada no navegador em:

- **[Swagger UI](http://localhost:8000/docs)**: Para testar e explorar os endpoints da API de forma interativa em http://localhost:8000/docs.
- **[Redoc](http://localhost:8000/redoc)**: Documentação alternativa gerada automaticamente em http://localhost:8000/redoc.

## Instalação

### Pré-requisitos

- **Python 3.12+**
- **Poetry**
- **Docker**


### Como Executar a `main`.

Esse comando cria o banco de dados, aplica as migrações e inicia a aplicação.
- docker-compose up --build

### Como Executar a `develop`.
- poetry install
- poetry shell
- task run ou uvicorn user_todo_api.main:app --reload

### Como Executar os testes.
- poetry shell
- task test ou poetry run pytest


## Acesse a API:

Acesse http://localhost:8000 para utilizar a API.


## Autenticação
A API utiliza autenticação baseada em token. No campo username no formulário de login, utilize o e-mail registrado na criação da conta.
