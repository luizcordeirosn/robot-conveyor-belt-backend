# 🤖 Robot API

API de controle robótico desenvolvida com FastAPI para controle do robô Niryo, incluindo movimentação, manipulação de objetos e transformações de homografia.

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

### 🎮 Controle do Robô
- Movimentação precisa em coordenadas XYZ
- Controle do gripper (agarrar/soltar)
- Posições predefinidas (segura/descarte)
- Orientação automática do gripper

### 🔄 Simulação
- Ambiente containerizado com Docker
- Simulação realista do Niryo
- Controle remoto via API
- Operação em tempo real

### 📐 Homografia
- Geração de matriz de transformação
- Conversão de coordenadas câmera-robô
- Calibração via detecção de retângulos
- Mapeamento preciso do espaço de trabalho

### 🔧 Desenvolvimento
- API REST com FastAPI
- Testes automatizados
- Arquitetura modular
- Documentação interativa

## 🛠️ Tecnologias

- **Backend**
  - FastAPI (framework web)
  - Docker (containerização)
  - pyniryo (controle do robô)
  - OpenCV (visão computacional)
- **Testes**
  - pytest com fixtures
  - unittest.mock
- **Gerenciamento**
  - Poetry (dependências)
  - python-dotenv (configuração)
  - numpy (cálculos)

## 📋 Pré-requisitos

- Docker e Docker Compose
- Python 3.10+
- Poetry (instalado globalmente)
- Conexão com o robô Niryo

## 🚀 Instalação

1. **Configuração do Ambiente**
   ```bash
   # Clone o repositório
   git clone [URL_DO_REPOSITÓRIO]
   cd robot_api

   # Configure o ambiente
   cp .env.example .env
   ```

   Configure o arquivo `.env`:
   ```ini
   NIRYO_ROBOT_IP=169.254.200.200
   ```

2. **Construção do Container**
   ```bash
   # Build da imagem Docker
   ./build_docker.sh
   ```

3. **Inicialização**
   ```bash
   # Inicia a simulação
   ./run_docker.sh
   ```

4. **Calibração**
   ```bash
   # Gera matriz de homografia
   python generate_homography_residents.py
   ```

## 🎯 Uso

### Endpoints da API

Acesse a documentação interativa em `/docs` (Swagger UI)

#### Endpoints Principais:

- **Conexão**
  - `PUT /robots/close-connection`: Encerra conexão

- **Movimento**
  - `PUT /robots/position`: Move para XYZ
  - `PUT /robots/position/safe`: Posição segura
  - `PUT /robots/position/drop`: Posição de descarte

- **Gripper**
  - `PUT /robots/orientation`: Orienta para baixo
  - `PUT /robots/grab`: Agarra objeto
  - `PUT /robots/release`: Solta objeto

- **Visão**
  - `GET /robots/homography`: Transforma coordenadas

## 📁 Estrutura do Projeto

```
robot_api/
├── application/        # Código principal
│   ├── entities/      # Modelos e FSM
│   ├── services/      # Lógica de negócio
│   └── api/           # Endpoints
├── scripts/           # Scripts auxiliares
├── tests/             # Suite de testes
├── worlds/            # Mundos Gazebo
├── main.py           # Entrada da API
```

## 🧪 Testes

```bash
# Executar todos os testes
poetry run pytest
```

A suite de testes cobre:
- Rotas da API
- Camada de serviço
- Comportamentos das entidades
- Gerenciamento de conexão
- Operações de movimento

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📫 Contato

- **Autor**: Luiz Cordeiro da Silva Neto
- **Email**: luizcsneto@outlook.com

