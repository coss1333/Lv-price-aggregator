# Базовый парсер Barbora.lv страниц поиска (черновой).
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any

BASE = "https://www.barbora.lv/paiesana"

async def search(query: str, limit: int = 20, timeout: float = 15.0) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=timeout, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }) as client:
        r = await client.get(BASE, params={"search": query})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        items: List[Dict[str, Any]] = []
        cards = soup.select("[data-product-id], .b-product--wrap, .product-grid__item")
        for c in cards[:limit]:
            title_el = c.select_one(".b-product-title, .product__name, a[href]")
            price_el = c.select_one(".price, .b-product-price-current, .product__price")
            old_el = c.select_one(".old-price, .b-product-price-old")
            badge = c.select_one(".badge, .discount, .promotion")

            title = title_el.get_text(strip=True) if title_el else ""
            price = price_el.get_text(strip=True) if price_el else None
            old_price = old_el.get_text(strip=True) if old_el else None
            promo = bool(badge or old_price)
            url = title_el.get("href") if title_el and title_el.has_attr("href") else str(r.url)

            items.append({
                "store": "Barbora",
                "title": title,
                "price_eur": price,
                "old_price_eur": old_price,
                "promo": promo,
                "url": url,
            })
        return items
