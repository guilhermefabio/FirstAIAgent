# app/tools/web/scraper_playwright.py
from typing import Dict, Any
from playwright.sync_api import sync_playwright
import re

def extract_contacts_from_url(url: str, timeout_ms: int = 15000) -> Dict[str, Any]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=timeout_ms)
        page.wait_for_timeout(1500)
        text = page.inner_text("body")
        browser.close()

    emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))
    phones = sorted(set(re.findall(r"\+?\d[\d\s().-]{8,}\d", text)))
    wa_links = sorted(set(re.findall(r"(https?://wa\.me/\S+|https?://api\.whatsapp\.com/send\?phone=\S+)", text)))

    return {
        "emails": emails[:10],
        "phones": phones[:10],
        "whatsapp_links": wa_links[:10],
        "source_url": url,
    }
