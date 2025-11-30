# MX Keys Price Monitor

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

- Python 3.9+

- requests

- psycopg2

- python-dotenv

- beautifulsoup4 (se estiver usando parsing HTML)

## Banco de Dados

- PostgreSQL 13+

## Opcional

- Docker / Docker Compose

- Apache Airflow

# Configuração do .env

## Crie um arquivo .env na raiz do projeto:

# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=precos
DB_USER=airflow
DB_PASSWORD=airflow

# Telegram
TG_BOT_TOKEN=SEU_BOT_TOKEN
TG_CHAT_ID=SEU_CHAT_ID

# Alerts
PRICE_ALERT_THRESHOLD=600.00

# Scraping
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36

# Como obter o Token e Chat ID do Telegram

- Abra o Telegram e fale com o BotFather → @BotFather

- Crie um bot:
/newbot

- Copie o TOKEN fornecido

- Descubra seu Chat ID usando:

    - o bot @userinfobot, ou

    - acessando:

    https://api.telegram.org/botSEU_TOKEN/getUpdates
    

# Como executar o scraper
## Rodando diretamente com Python

No diretório raiz:

python -m scraper.main

# Rodando com Docker (se configurado)

docker compose up --build

# Estrutura da Tabela no Banco

## A tabela utilizada é:

CREATE TABLE IF NOT EXISTS precos (
    id SERIAL PRIMARY KEY,
    produto TEXT NOT NULL,
    site TEXT NOT NULL,
    url TEXT NOT NULL,
    preco NUMERIC(10,2),
    data_coleta TIMESTAMP
);

# Alertas de Preço

## O sistema envia alerta quando:

preco <= PRICE_ALERT_THRESHOLD

Exemplo de alerta enviado:

ALERTA: Logitech MX Keys em Amazon por R$ 580.00
https://amazon.com/...

