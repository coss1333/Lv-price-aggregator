# Минимальный парсер результатов salidzini.lv
# Селекторы могут меняться — проверяйте и обновляйте при необходимости.
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any

BASE = "https://www.salidzini.lv/cena"

async def search(query: str, limit: int = 20, timeout: float = 15.0) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=timeout, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }) as client:
        r = await client.get(BASE, params={"q": query})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        items: List[Dict[str, Any]] = []
        cards = soup.select(".product-list .item, .product-item, .search-result-item, .cena-list .item")
        for c in cards[:limit]:
            title_el = c.select_one(".title, .product-title, a[href]")
            price_el = c.select_one(".price, .product-price, .cena")
            shop_el = c.select_one(".shop, .store, .vendor, .veikals")
            link_el = c.select_one("a[href]")

            title = title_el.get_text(strip=True) if title_el else ""
            price = price_el.get_text(strip=True) if price_el else None
            store = shop_el.get_text(strip=True) if shop_el else "salidzini-merchant"
            url = link_el.get("href") if link_el else str(r.url)

            items.append({
                "store": store,
                "title": title,
                "price_eur": price,
                "promo": False,
                "url": url,
            })
        return items
