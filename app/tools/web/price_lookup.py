import re
import asyncio
from typing import List, Dict, Optional
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _ml_search(query: str, limit: int = 5) -> List[Dict[str, Optional[str]]]:
    """
    Mercado Livre (httpx + bs4). Retorna no MESMO formato:
      {"title": str, "price": Optional[str], "url": str}
    """
    url = f"https://lista.mercadolivre.com.br/{quote_plus(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }

    try:
        r = httpx.get(url, headers=headers, timeout=30, follow_redirects=True)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "lxml")
        results: List[Dict[str, Optional[str]]] = []

        for li in soup.select("li.ui-search-layout__item")[: limit * 3]:
            a = li.select_one("h3 a.poly-component__title")
            if not a:
                continue

            title = _clean_text(a.get_text(strip=True))
            link = a.get("href") or "mercadolivre.com.br"

            # preço atual
            price_span = li.select_one("span.poly-price__current span.andes-money-amount")
            if not price_span:
                price_span = li.select_one("span.andes-money-amount")

            if not price_span:
                results.append({"title": title[:100], "price": None, "url": link})
                if len(results) >= limit:
                    break
                continue

            frac = price_span.select_one("span.andes-money-amount__fraction")
            cents = price_span.select_one("span.andes-money-amount__cents")

            if not frac:
                price = None
            else:
                if cents:
                    price = f"R$ {frac.get_text(strip=True)},{cents.get_text(strip=True)}"
                else:
                    price = f"R$ {frac.get_text(strip=True)}"

            results.append({"title": title[:100], "price": price, "url": link})
            if len(results) >= limit:
                break

        return results

    except Exception:
        return []


async def google_udm28_prices(query: str, limit: int = 5) -> List[Dict[str, Optional[str]]]:
    """
    Mantido o mesmo nome/assinatura.
    Como Google cai em captcha, aqui vira um wrapper que retorna [] (pra cair no fallback).
    """
    # Se quiser insistir no Google, coloca tua lógica Playwright aqui.
    # Por padrão, retorna vazio pra evitar travar o fluxo.
    return []


def fetch_price_signals(query: str, limit: int = 5) -> List[Dict[str, Optional[str]]]:
    """
    MESMA assinatura e mesmo formato de saída.
    1) tenta google_udm28_prices (atualmente retorna [])
    2) fallback Mercado Livre (funcional)
    3) último fallback padrão
    """
    try:
        results = asyncio.run(google_udm28_prices(query, limit))
        if results and any(r.get("price") for r in results):
            return results
    except Exception:
        pass

    ml = _ml_search(query, limit)
    if ml and any(r.get("price") for r in ml):
        return ml
    if ml:
        return ml

    return [{"title": f"Buscar '{query}' no Mercado Livre", "url": "mercadolivre.com.br", "price": None}]
