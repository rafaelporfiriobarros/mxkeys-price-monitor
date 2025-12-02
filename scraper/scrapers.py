import json
import os
import re
import requests
from urllib.parse import urlparse
from .utils import fetch_url, polite_sleep
from .parsers import parse_price_amazon, parse_price_generic
from .config import USER_AGENT
from pathlib import Path

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "pt-BR,pt;q=0.9",
}

# tenta caminhos em ordem: variável de ambiente, arquivo do pacote, cwd, /opt/airflow/dags, Airflow Variable (opcional)
SITES_FILE_ENV = os.environ.get("MXKEYS_SITES_FILE")  # opcional: aponta p/ caminho absoluto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATHS = [
    "/opt/airflow/dags/sites.json",
    "/opt/scraper/sites.json",
    os.path.join(BASE_DIR, "sites.json"),
]

DEFAULT_PATHS = [p for p in DEFAULT_PATHS if p]

def load_sites():
    # 1) tenta carregar de arquivo em vários caminhos
    for path in DEFAULT_PATHS:
        try:
            if Path(path).is_file():
                with open(path, "r", encoding="utf-8") as f:
                    print(f"→ Carregando sites de: {path}")
                    return json.load(f)
        except Exception as e:
            print(f"→ Falha ao tentar abrir {path}: {e}")

    # 2) fallback: tenta Airflow Variable (se estiver rodando no Airflow)
    try:
        from airflow.models import Variable
        sites_json = Variable.get("mxkeys_sites", default_var=None)
        if sites_json:
            print("→ Carregando sites de Airflow Variable `mxkeys_sites`")
            return json.loads(sites_json)
    except Exception:
        pass

    # 3) última alternativa: raise com mensagem útil
    raise FileNotFoundError(
        "Nenhum sites.json encontrado. Verifique: "
        "MXKEYS_SITES_FILE env, ./sites.json no package, /opt/airflow/dags/sites.json ou a Airflow Variable `mxkeys_sites`."
    )


SITES = load_sites()

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

def scrape_site(url: str, site_key: str):
    try:
        print(f"Buscando preço de {site_key}")

        # MERCADO LIVRE — tenta API primeiro
        if site_key == "mercadolivre":
            ml_id = extract_mercadolivre_id(url)
            if ml_id:
                price = mercadolivre_api_price(ml_id)
                if price:
                    print(f"✔ Mercado Livre via API -> {price}")
                    return price

            print("Falhou API - tentando HTML")
            html = fetch_url(url, HEADERS)
            return parse_price_generic(html)

        # AMAZON — usa parser específico sempre
        if site_key == "amazon":
            html = fetch_url(url, HEADERS)
            price = parse_price_amazon(html)
            if price is None:
                print("AMAZON SEM PREÇO — salvando HTML para debug…")
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
        print(f"ERRO no scraping de {site_key}: {e}")
        return None


def scrape_all_sites(sites=SITES):
    results = []
    for site_key, url in sites.items():
        print(f"Coletando {site_key}: {url}")
        price = scrape_site(url, site_key)
        results.append({"site": site_key, "url": url, "price": price})
        polite_sleep(2, 5)

    return results
