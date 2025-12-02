# MX Keys Price Monitor

![Ambiente Virtual](assets/teclado-mxkeys.png)

Monitoramento automático de preços do teclado Logitech MX Keys com Web Scraping, PostgreSQL, Airflow e alertas via Telegram.

Este projeto coleta preços em diferentes sites, salva em um banco de dados PostgreSQL e envia alertas para o Telegram quando o preço cai abaixo de um limite definido.

# Funcionalidades

- Web Scraping automatizado em múltiplos sites

- Armazenamento em banco PostgreSQL

- Envio de alertas via Telegram

- Integração opcional com Airflow para agendamento diário

- Sistema configurado via .env (sem expor credenciais)

# Requisitos
## Python

- Python 3.11.5

- requests

- psycopg2

- python-dotenv

- beautifulsoup4 (se estiver usando parsing HTML)

## Banco de Dados

- PostgreSQL 13+

## Opcional

- Docker / Docker Compose

- Apache Airflow

# Como rodar o projeto 

## Pyenv

- Primeiro de tudo, você deve instalar a versão mais estável do python para trabalhar com airflow no docker, que é a versão 3.11.5.
- Para isso, instale o Pyenv. O Pyenv é uma ferramenta que permite instalar e gerenciar múltiplas versões do Python no mesmo sistema — ideal para projetos diferentes, ambientes isolados e compatibilidade com Airflow, Django, Data Science, etc.
- Acesse o video a seguir da Jornada de Dados para instalar e conhecer melhor sobre o pyenv e ambientes virtuais:

[Como instalar Python em 2024 + Pyenv, PIP, VENV, PIPX e Poetry](https://www.youtube.com/watch?v=9LYqtLuD7z4&t=194s)

- Depois de ter instalado o pyenv e baixado o python 3.11.5, entre na pasta do projeto "mxkeys-price-monitor" e ative a versão do python no terminal utilizando:

```bash
pyenv local 3.11.5

- Verifique no terminal a versão do python utilizando:

```bash
"python3 --version" 

ou tente:

```bash
"python --version" 

dependendo do seu sistema operacional.

## Ambiente virtual

- Agora será preciso criar um ambiente virtual para isolar dependências, garantindo que cada projeto tenha suas próprias bibliotecas e versões — sem conflito com outros projetos ou com o Python do sistema.

- Se você viu o vídeo da "Jornada de Dados" e entendeu como funciona um ambiente virtual, vamos criar um:
    - No diretório do projeto, abra o terminal e digite: 
    - "python -m venv .venv"
    - Será criada uma pasta .venv com as dependências necessárias para o ambiente virtual.
    - Em seguida, ative o ambiente:
    - No Linux / macOS vocẽ utiliza:
    - "source .venv/bin/activate"
    - No Windows vocẽ utiliza:
    - "venv\Scripts\activate"

![Ambiente Virtual](assets/ambiente-virtual-ativo.png)









