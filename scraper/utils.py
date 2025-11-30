import re
import time
import requests
from bs4 import BeautifulSoup
from decimal import Decimal, InvalidOperation

def normalize_price(text):
    """
    Recebe uma string contendo R$ e retorna float (ex: "R$ 1.234,56" -> 1234.56)
    """
    if not text:
        return None
    # extrai substring com R$ ou dígitos e vírgulas
    m = re.search(r'R\$\s*[\d\.\,]+|[\d\.\,]+\s*R\$', text)
    txt = m.group(0) if m else text
    # remove R$ e espaços
    txt = txt.replace("R$", "").replace(" ", "")
    # normaliza pontos e vírgulas
    txt = txt.replace(".", "").replace(",", ".")
    try:
        return float(Decimal(txt))
    except (InvalidOperation, ValueError):
        return None

def fetch_url(url, headers=None, timeout=15):
    headers = headers or {}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"Erro ao buscar {url}: {e}")
        return None

def soup_from_html(html):
    return BeautifulSoup(html, "html.parser")

def find_price_in_text(html_text):
    # procura o primeiro padrão R$ X
    import re
    m = re.search(r'R\$\s*[\d\.\,]+', html_text)
    return m.group(0) if m else None

def polite_sleep(min_seconds=2, max_seconds=6):
    import random
    time.sleep(random.uniform(min_seconds, max_seconds))
