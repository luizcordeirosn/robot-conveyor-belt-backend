# 💾 Database API

API de banco de dados desenvolvida com FastAPI para gerenciar usuários, logs de operações e dashboards de classificação de peças. Utiliza MySQL como banco de dados, SQLAlchemy para ORM, Alembic para migrações e bcrypt para segurança.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Testes](#-testes)
- [Licença](#-licença)
- [Contato](#-contato)

## ⭐ Funcionalidades

### 🔐 Autenticação e Usuários
- Login seguro com bcrypt
- Registro de novos usuários
- Gerenciamento de sessões
- Proteção de rotas

### 📝 Gerenciamento de Logs
- Registro de operações por usuário
- Categorização por tipo e status
- Filtros por cor e categoria
- Histórico de execuções

### 📊 Dashboards
- Armazenamento de resultados
- Imagens classificadas
- Níveis de confiança
- Filtros por label

### 🔄 Banco de Dados
- Migrações com Alembic
- Relacionamentos otimizados
- Backup e restauração
- Controle de versão do schema

## 🛠️ Tecnologias

- **Backend**
  - FastAPI (framework web)
  - SQLAlchemy (ORM)
  - BetterProto (serialização)
  - bcrypt (segurança)
- **Banco de Dados**
  - MySQL
  - Alembic (migrações)
  - Docker (containerização)
- **Testes**
  - pytest com fixtures
  - unittest.mock
- **Gerenciamento**
  - Poetry (dependências)
  - python-dotenv (configuração)
  - uvicorn (servidor ASGI)

## 📋 Pré-requisitos

- Python 3.10.11+
- Docker e Docker Compose
- Poetry (instalado globalmente)
- MySQL Server

## 🚀 Instalação

1. **Configuração do Ambiente**
   ```bash
   # Clone o repositório
   git clone [URL_DO_REPOSITÓRIO]
   cd database_api

   # Configure o ambiente
   cp .env.example .env
   ```

   Configure o arquivo `.env`:
   ```ini
   MYSQL_ROOT_USER=root
   MYSQL_ROOT_PASSWORD=senha123
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_DATABASE=database_api_db
   ```

2. **Instalação de Dependências**
   ```bash
   # Instale as dependências
   poetry install
   ```

3. **Inicialização do Banco**
   ```bash
   # Execute as migrações
   poetry run alembic upgrade head
   ```

## 🎯 Uso

### Endpoints da API

Acesse a documentação interativa em `/docs` (Swagger UI)

#### Endpoints Principais:

- **Autenticação**
  - `POST /login/`: Login de usuário

- **Usuários**
  - `POST /users/`: Registro de usuário

- **Logs**
  - `POST /logs/`: Cria novo log
  - `GET /logs/user/{user_id}`: Lista logs
  - `GET /logs/user/{user_id}/last-execution/`: Último log
  - Filtros:
    - `GET /logs/user/category/{user_id}/{category}`
    - `GET /logs/user/color/{user_id}/{color}`
    - `GET /logs/user/status/{user_id}/{status}`

- **Dashboards**
  - `POST /dashboards/`: Cria dashboard
  - `GET /dashboards/user/{user_id}`: Lista dashboards
  - `GET /dashboards/label/{user_id}/{label}`: Filtra por label


## 📁 Estrutura do Projeto

```
database_api/
├── database/           # Código principal
│   ├── connection/    # Conexão com banco
│   ├── dao/          # Data Access Objects
│   ├── model/        # Modelos SQLAlchemy
│   ├── proto/        # Definições BetterProto
│   └── services/     # Lógica de negócio
├── routes/            # Endpoints FastAPI
├── alembic/           # Migrações
├── tests/             # Suite de testes
└── main.py           # Entrada da API
```

## 🧪 Testes

```bash
# Executar todos os testes
poetry run pytest
```

Cobertura inclui:
- Modelos (User, Log, Dashboard)
- DAOs e Serviços
- Rotas e endpoints
- Migrações e conexões
- Cenários de erro

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📫 Contato

- **Autor**: Tamyres Silva
- **Email**: tamyressilvazz@outlook.com

