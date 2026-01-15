# app/tools/web/price_lookup.py
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import re

import httpx

PRICE_PATTERN = re.compile(r"(R\$\s?\d+(?:\.\d{3})*(?:,\d{2})?|\$\s?\d+(?:,\d{3})*(?:\.\d{2})?)")
RESULT_LINK_PATTERN = re.compile(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>')
RESULT_SNIPPET_PATTERN = re.compile(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>')

def fetch_price_signals(query: str, limit: int = 5) -> List[Dict[str, Optional[str]]]:
    search_url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (buyer-agent price lookup)"}

    with httpx.Client(timeout=15.0) as client:
        response = client.get(search_url, headers=headers)
        response.raise_for_status()
        html = response.text

    links = RESULT_LINK_PATTERN.findall(html)
    snippets = RESULT_SNIPPET_PATTERN.findall(html)

    results = []
    for idx, (url, title_html) in enumerate(links[:limit]):
        snippet = snippets[idx] if idx < len(snippets) else ""
        text = re.sub(r"<[^>]+>", "", f"{title_html} {snippet}")
        price_match = PRICE_PATTERN.search(text)
        results.append({
            "title": re.sub(r"<[^>]+>", "", title_html).strip(),
            "url": url,
            "price": price_match.group(1) if price_match else None,
        })

    return results
