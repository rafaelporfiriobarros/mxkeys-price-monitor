# scraper/main.py

import psycopg2
import requests
from datetime import datetime

from scraper.scrapers import scrape_all_sites
from scraper.utils import normalize_price
from scraper.config import (
    DB,
    TG_BOT_TOKEN,
    TG_CHAT_ID,
    PRICE_ALERT_THRESHOLD,
)

def save_price_db(conn, produto, site, url, price):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO precos (produto, site, url, preco, data_coleta)
        VALUES (%s, %s, %s, %s, %s)
    """, (produto, site, url, price, datetime.utcnow()))
    conn.commit()
    cur.close()


def send_telegram(msg):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        print("Telegram não configurado.")
        return

    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TG_CHAT_ID, "text": msg}, timeout=10)
    except Exception as e:
        print("Erro ao enviar Telegram:", e)


def main():
    produto = "Logitech MX Keys"

    results = scrape_all_sites()

    # conecta ao banco usando config.DB
    conn = psycopg2.connect(
        host=DB["host"],
        port=DB["port"],
        dbname=DB["name"],
        user=DB["user"],
        password=DB["password"]
    )

    for r in results:
        price = r["price"]
        site = r["site"]
        url = r["url"]

        print(f"{site}: {price}")

        if price is None:
            print(f"Aviso: preço não encontrado para {site} — pulando.")
            continue

        save_price_db(conn, produto, site, url, price)

        if price <= PRICE_ALERT_THRESHOLD:
            msg = f"ALERTA: {produto} em {site} por R$ {price:.2f}\n{url}"
            send_telegram(msg)

    conn.close()


if __name__ == "__main__":
    main()
