# 👁️ Vision API

API de visão computacional desenvolvida com FastAPI para detecção e classificação de objetos em tempo real usando câmera, YOLO e detecção de retângulos vermelhos.

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

### 📸 Captura de Vídeo
- Controle de câmera via OpenCV
- Limpeza de buffer e captura de frames
- Suporte a ROI (Region of Interest)

### 🔍 Detecção de Retângulos Vermelhos
- Identificação de centroides usando LAB color space
- Aprimoramento com CLAHE e morfologia
- Detecção parcial com estimativa de pontos faltantes

### 🤖 Classificação com YOLO
- Predição de objetos (semisphere, cuboid, etc.)
- Salvamento de imagens anotadas
- Cálculo de confiança

### 📊 Processamento
- Mapeamento de coordenadas globais (1280x720)
- Cálculo preciso de centroides
- Identificação em tempo real

## 🛠️ Tecnologias

- **Backend**
  - FastAPI (framework web)
  - OpenCV (visão computacional)
  - Ultralytics YOLO (detecção)
- **Testes**
  - pytest com fixtures
  - unittest.mock
- **Gerenciamento**
  - Poetry (dependências)
  - python-dotenv (configuração)
  - numpy (cálculos)

## 📋 Pré-requisitos

- Python 3.10.11 ou superior
- Poetry instalado globalmente
- Câmera conectada (ex.: /dev/video0)

## 🚀 Instalação

1. **Configuração do Ambiente**
   ```bash
   # Clone o repositório
   git clone [URL_DO_REPOSITÓRIO]
   cd vision_api

   # Instale as dependências
   poetry install
   ```

2. **Configuração das Variáveis de Ambiente**
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   ```
   
   Configure o arquivo `.env`:
   ```ini
   WEIGHTS_PATH=best_with_brightness.pt
   NUM_CAM=0
   ```

3. **Scripts Auxiliares**
   - Captura de imagens:
     ```bash
     python scripts/taking-picture.py
     ```
     - Pressione 'q' para salvar
     - Pressione 'e' para próxima pasta
   
   - Teste de centroides:
     ```bash
     python scripts/get_centroid.py
     ```

## 🎯 Uso

### API Endpoints

Acesse a documentação interativa em `/docs` (Swagger UI)

#### Endpoints Principais:

- **Câmera**
  - `GET /cameras/label`: 
    - Retorna: centroid (x, y), label, classe, confiança e filename
  - `PUT /cameras/release-video`: 
    - Libera a captura de vídeo

## 📁 Estrutura do Projeto

```
vision_api/
├── application/
│   ├── entities/     # Modelos (Camera, Yolo)
│   ├── services/     # Lógica (CameraService)
│   ├── api/routes/   # Endpoints FastAPI
│   └── utils/        # Utilitários
├── scripts/          # Scripts auxiliares
├── tests/            # Testes automatizados
└── main.py          # Ponto de entrada
```

## 🧪 Testes

```bash
# Executar todos os testes
poetry run pytest
```

A cobertura inclui:
- Testes de rotas (sucesso/resposta vazia)
- Serviços mockados
- Validação de componentes

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📫 Contato

- **Autor**: Luiz Neto
- **Email**: luizcsneto@outlook.com
