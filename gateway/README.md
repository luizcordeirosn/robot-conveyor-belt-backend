# 🌐 Gateway API

API Gateway desenvolvida com FastAPI que atua como ponto central de integração para um sistema de classificação de peças, gerenciando usuários, autenticação, logs, dashboards e controle de dispositivos (robô, câmera e esteira transportadora).

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

### 👥 Autenticação e Usuários
- Login e registro de usuários
- Armazenamento local em JSON
- Gerenciamento de sessões
- Controle de acesso

### 📊 Gerenciamento de Dados
- Logs de operação (categoria, cor, status)
- Dashboards com métricas
- Histórico de execuções
- Imagens e resultados de classificação

### 🎛️ Controle de Dispositivos
- Integração com robô para manipulação
- Controle de câmera para detecção
- Gerenciamento da esteira transportadora
- Modos real e virtual de operação

### 🔄 Máquina de Estados
- FSM para orquestração do sistema
- Estados: idle, detecting, grabbing
- Transições automáticas
- Controle de ciclo operacional

## 🛠️ Tecnologias

- **Backend**
  - FastAPI (framework web)
  - BetterProto (serialização)
  - Transitions (FSM)
  - pyserial (comunicação)
- **Integração**
  - requests (chamadas HTTP)
  - threading (operações assíncronas)
- **Gerenciamento**
  - Poetry (dependências)
  - python-dotenv (configuração)
  - uvicorn (servidor ASGI)

## 📋 Pré-requisitos

- Python 3.10+
- Poetry (instalado globalmente)
- Serviços externos configurados (database, vision, robot)
- ESP conectado (para modo real)

## 🚀 Instalação

1. **Configuração do Ambiente**
   ```bash
   # Clone o repositório
   git clone [URL_DO_REPOSITÓRIO]
   cd gateway

   # Configure o ambiente
   cp .env.example .env
   ```

   Configure o arquivo `.env`:
   ```ini
   # Para execução local (testes, desenvolvimento)
   DATABASE_URL="http://localhost:8003"
   VISION_URL="http://localhost:8001"
   ROBOT_URL="http://localhost:8002"
   ```


**Testes**  
Para rodar os testes automatizados, é necessário configurar corretamente o ambiente e as variáveis do arquivo `.env`.

1. **Configuração do .env**  
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   Para executar os testes (e também para rodar a aplicação localmente com `uvicorn` ou executar o `alembic`), as URLs no `.env` devem apontar para `localhost`, pois os scripts são executados diretamente na sua máquina (host).

   Crie ou verifique seu arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   ```bash
   # .env para execução LOCAL (testes, alembic, etc.)
   DATABASE_URL="http://localhost:8003"
   VISION_URL="http://localhost:8001"
   ROBOT_URL="http://localhost:8002"
   ```

   Nota: Lembre-se que esta configuração é para execução local. Para rodar a aplicação principal dentro de um contêiner via docker-compose, os valores de host deverão ser alterados para `host.docker.internal`.

## 🎯 Uso

### Endpoints da API

Acesse a documentação interativa em `/docs` (Swagger UI)

#### Endpoints Principais:

- **Autenticação**
  - `POST /login/`: Login de usuário

- **Usuários**
  - `POST /users/`: Registro de usuário

- **Dados**
  - `GET /dashboards/user/{user_id}`: Dashboards
  - `GET /logs/user/{user_id}`: Histórico
  - `GET /logs/user/{user_id}/last-exec`: Última execução

- **Esteira**
  - `PUT /conveyor-belt/start`: Inicia operação
  - `PUT /conveyor-belt/stop`: Para operação

- **Dispositivos**
  - `GET /cameras/label`: Detecção de objetos
  - `PUT /robots/position`: Controle de movimento
  - `PUT /robots/grab`: Manipulação de objetos

## 📁 Estrutura do Projeto

```
gateway/
├── application/
│   ├── api/
│   │   └── routes/    # Endpoints FastAPI
│   ├── entities/      # Modelos e FSM
│   ├── services/      # Lógica de negócio
│   ├── proto/         # Definições BetterProto
│   └── utils/         # Utilitários
├── data/             # Armazenamento local
├── tests/            # Suite de testes
└── main.py          # Entrada da API
```

## 🧪 Testes

```bash
# Executar todos os testes
poetry run pytest
```

Cobertura inclui:
- Rotas da API
- Serviços e integrações
- Máquina de estados
- Comunicação com dispositivos
- Persistência de dados

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📫 Contato

- **Autor**: Luiz Cordeiro da Silva Neto
- **Email**: luizcsneto@outlook.com
