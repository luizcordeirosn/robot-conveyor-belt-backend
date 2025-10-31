# Robot Conveyor Backend

Sistema de backend para controle e monitoramento de esteira robótica, integrando visão computacional, controle de robô e gerenciamento de dados.

## 📋 Índice

- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
  - [Clonagem do Repositório](#clonagem-do-repositório)
  - [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
  - [Execução das APIs](#execução-das-apis)
- [Testes](#-testes)
- [Estrutura do Projeto](#-estrutura-do-projeto)

## 🔧 Pré-requisitos

- Docker e Docker Compose
- Python 3.8 ou superior
- Poetry (gerenciador de dependências Python)
- Git

## 🚀 Instalação e Configuração

### Clonagem do Repositório

```bash
git clone git@github.com:luizcordeirosn/robot-conveyor-belt-backend.git
cd robot-conveyor-belt-backend
```

### Configuração do Banco de Dados

1. **Preparação do Ambiente**
   - Crie e configure os arquivos `.env` para todas as aplicações (backend, banco de dados)
   - Certifique-se de que as variáveis de ambiente estão configuradas corretamente

2. **Iniciando o Banco de Dados**
   ```bash
   docker-compose up -d
   ```

3. **Configuração das Migrações**
   > **⚠️ Importante:** O Alembic será executado localmente e precisa se conectar ao banco no Docker
   
   Configure o arquivo `.env` para o Alembic:
   ```ini
   DB_HOST=localhost
   DB_PORT=3306  # Porta exposta no docker-compose
   ```

4. **Executando as Migrações**
   ```bash
   alembic upgrade head
   ```

### Execução das APIs

#### Opção 1: Desenvolvimento Local

Ideal para desenvolvimento e debug:

1. **Instalação das Dependências**
   ```bash
   poetry install
   poetry shell
   ```

2. **Iniciando o Servidor**
   ```bash
   uvicorn main:app --reload --port 8010
   ```

   📝 Acesse a API em: `http://localhost:8010/docs`

#### Opção 2: Via Docker Compose

Para ambiente de produção ou teste integrado:

1. Execute o ambiente completo:
   ```bash
   docker-compose up -d
   ```

2. Acesse a documentação da API:
   ```
   http://localhost:8000/docs
   ```

   > 📌 Se a porta 8000 não estiver disponível, verifique a porta configurada no `docker-compose.yml`

## 🧪 Testes

Execute os testes usando o pytest:

```bash
# Executar todos os testes
poetry run pytest

# Executar um teste específico
poetry run pytest model/test_log_model.py::test_log_model_creation
```
