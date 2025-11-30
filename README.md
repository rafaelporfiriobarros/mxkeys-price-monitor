# MX Keys Price Monitor

Monitoramento automático de preços do teclado Logitech MX Keys com Web Scraping, PostgreSQL, Airflow e alertas via Telegram.

Este projeto coleta preços em diferentes sites, salva em um banco de dados PostgreSQL e envia alertas para o Telegram quando o preço cai abaixo de um limite definido.

# Funcionalidades

- Web Scraping automatizado em múltiplos sites

- Armazenamento em banco PostgreSQL

- Envio de alertas via Telegram

- Integração opcional com Airflow para agendamento diário

- Sistema configurado via .env (sem expor credenciais)