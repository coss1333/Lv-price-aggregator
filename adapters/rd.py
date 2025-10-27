# Черновой адаптер RD Electronics.
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any

BASE = "https://www.rdveikals.lv/search.php"

async def search(query: str, limit: int = 20, timeout: float = 15.0) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=timeout, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }) as client:
        r = await client.get(BASE, params={"search": query})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        items: List[Dict[str, Any]] = []
        cards = soup.select(".product, .products-grid .item, .product-item")
        for c in cards[:limit]:
            title_el = c.select_one(".name a, .product-name a, a[href]")
            price_el = c.select_one(".price, .special-price, .regular-price")
            promo_el = c.select_one(".special-price, .discount, .sale")

            title = title_el.get_text(strip=True) if title_el else ""
            price = price_el.get_text(strip=True) if price_el else None
            promo = bool(promo_el)
            url = title_el.get("href") if title_el and title_el.has_attr("href") else str(r.url)

            items.append({
                "store": "RD Electronics",
                "title": title,
                "price_eur": price,
                "promo": promo,
                "url": url,
            })
        return items
