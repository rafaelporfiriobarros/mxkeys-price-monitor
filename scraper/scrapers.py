import re
import requests
from urllib.parse import urlparse
from .utils import fetch_url, polite_sleep
from .parsers import parse_price_amazon, parse_price_generic
from .config import USER_AGENT

# -------------------------------------------------------
# HEADERS
# -------------------------------------------------------
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "pt-BR,pt;q=0.9",
}


# -------------------------------------------------------
# URLs monitoradas
# Adicione quantas quiser
# -------------------------------------------------------
SITES = {
    "amazon": "https://www.amazon.com.br/dp/B09LYZP1LG",
    "mercadolivre": "https://encurtador.com.br/Wiwd",
    "magalu": "https://www.magazineluiza.com.br/teclado-bluetooth-logitech-master-series-mx-keys-mini-qwerty/p/kkf0k96c15",
    "kabum": "https://www.kabum.com.br/produto/366615/teclado-logitech-mx-keys-mini-cinza-padrao-us-920-010506",
    "iplace":"https://shre.ink/qhmu",
    "terabyte":"https://shre.ink/qhm3",
    "pichau":"https://www.pichau.com.br/teclado-sem-fio-logitech-mx-keys-mini-iluminacao-smart-easy-switch-grafite-920-010505"
}

# -------------------------------------------------------
# Parsers adicionais (para sites que quebram)
# -------------------------------------------------------

def parse_price_kabum(html):
    m = re.search(r'"price"\s*:\s*"?(\\?\d+[.,]\d+)"?', html)
    if m:
        return float(m.group(1).replace(",", "."))
    return None


def parse_price_magalu(html):
    """
    Magalu coloca preço no formato:
    "salesPrice": 899.90
    """
    m = re.search(r'"salesPrice"\s*:\s*(\d+[.,]\d+)', html)
    if m:
        return float(m.group(1).replace(",", "."))
    return None


def mercadolivre_api_price(item_id: str):
    """API REAL do Mercado Livre (muito mais confiável)."""
    try:
        url = f"https://api.mercadolibre.com/items/{item_id}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
        return float(data.get("price", 0)) or None
    except:
        return None


def extract_mercadolivre_id(url: str):
    m = re.search(r"(MLB\d+)", url)
    return m.group(1) if m else None


# -------------------------------------------------------
# Scraper principal
# -------------------------------------------------------
def scrape_site(url: str, site_key: str):
    try:
        print(f"\n🔎 Buscando preço de {site_key}")

        # MERCADO LIVRE — tenta API primeiro
        if site_key == "mercadolivre":
            ml_id = extract_mercadolivre_id(url)
            if ml_id:
                price = mercadolivre_api_price(ml_id)
                if price:
                    print(f"✔ Mercado Livre via API -> {price}")
                    return price

            print("⚠ Falhou API - tentando HTML")
            html = fetch_url(url, HEADERS)
            return parse_price_generic(html)

        # AMAZON — usa parser específico sempre
        if site_key == "amazon":
            html = fetch_url(url, HEADERS)
            price = parse_price_amazon(html)
            if price is None:
                print("⚠ AMAZON SEM PREÇO — salvando HTML para debug…")
                with open("amazon_debug.html", "w", encoding="utf-8") as f:
                    f.write(html)
            return price

        # KABUM
        if site_key == "kabum":
            html = fetch_url(url, HEADERS)
            return parse_price_kabum(html)

        # MAGALU
        if site_key == "magalu":
            html = fetch_url(url, HEADERS)
            return parse_price_magalu(html)

        # fallback genérico para sites novos
        html = fetch_url(url, HEADERS)
        return parse_price_generic(html)

    except Exception as e:
        print(f"❌ ERRO no scraping de {site_key}: {e}")
        return None


# -------------------------------------------------------
# Scraper de todos os sites
# -------------------------------------------------------
def scrape_all_sites(sites=SITES):
    results = []
    for site_key, url in sites.items():
        print(f"\n➡️ Coletando {site_key}: {url}")
        price = scrape_site(url, site_key)
        results.append({"site": site_key, "url": url, "price": price})
        polite_sleep(2, 5)

    return results
