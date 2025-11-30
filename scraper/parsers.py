# scraper/parsers.py
from bs4 import BeautifulSoup
import re
from .utils import normalize_price, find_price_in_text

def parse_price_amazon(html: str):
    """
    Tenta extrair o preço da Amazon Brasil com vários seletores e fallback por regex.
    Retorna float ou None.
    """
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    selectors = [
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#priceblock_saleprice",
        "span.a-price > span.a-offscreen",           # novo padrão comum
        "span.a-price .a-offscreen",
        ".a-offscreen",                               # genérico Amazon
        ".priceBlockBuyingPriceString",
        ".priceToPay .a-offscreen",
        ".product-price span"                         # fallback genérico
    ]

    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            txt = el.get_text(" ", strip=True)
            v = normalize_price(txt)
            if v is not None:
                return v

    # Tentar combinar partes (ex: whole + fraction)
    whole = soup.select_one("span.a-price-whole")
    frac = soup.select_one("span.a-price-fraction")
    if whole:
        txt = whole.get_text(strip=True)
        if frac:
            txt = f"{txt},{frac.get_text(strip=True)}"
        v = normalize_price(txt)
        if v is not None:
            return v

    # fallback: procurar por qualquer ocorrência "R$ ..." no texto
    raw = find_price_in_text(soup.get_text(" ", strip=True))
    if raw:
        return normalize_price(raw)

    return None


def parse_price_generic(html: str):
    """
    Parser genérico usado para sites com preço em HTML estático.
    """
    if not html:
        return None
    # tenta seletores comuns
    soup = BeautifulSoup(html, "html.parser")
    selectors = [
        ".product-price", ".price", ".preco", ".valor", ".price-value", ".price_number", ".productCardPrice"
    ]
    for sel in selectors:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            p = normalize_price(el.get_text(strip=True))
            if p is not None:
                return p

    raw = find_price_in_text(soup.get_text(" ", strip=True))
    if raw:
        return normalize_price(raw)

    return None
