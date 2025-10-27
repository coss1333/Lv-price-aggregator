import asyncio
import importlib
import pkgutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import typer
from utils.normalize import normalize_price, cleanse_text
from utils.output import print_table, write_csv

app = typer.Typer(add_completion=False)

def load_adapters(include: Optional[List[str]] = None):
    adapters_pkg = "adapters"
    pkg_path = Path(__file__).parent / adapters_pkg
    mods = []
    for info in pkgutil.iter_modules([str(pkg_path)]):
        name = info.name
        if name.startswith("_"):
            continue
        if include and name not in include:
            continue
        module = importlib.import_module(f"{adapters_pkg}.{name}")
        if hasattr(module, "search"):
            mods.append((name, module))
    return mods

async def run_query(query: str, sources: Optional[List[str]], limit: int, timeout: float):
    adapters = load_adapters(include=sources)
    tasks = []
    for name, module in adapters:
        tasks.append(module.search(query=query, limit=limit, timeout=timeout))
    results = await asyncio.gather(*tasks, return_exceptions=True)

    items: List[Dict[str, Any]] = []
    for (name, _), res in zip(adapters, results):
        if isinstance(res, Exception):
            items.append({
                "store": name,
                "title": f"[ERROR] {name}",
                "price_eur": None,
                "promo": False,
                "url": "",
                "source": name,
                "error": str(res),
            })
            continue
        for it in res:
            it["title"] = cleanse_text(it.get("title",""))
            it["price_eur"] = normalize_price(it.get("price_eur"))
            it["promo"] = bool(it.get("promo", False))
            it["source"] = name
            items.append(it)

    dedup = {}
    for it in items:
        key = (it.get("store","").lower(), it.get("title","").lower(), it.get("url",""))
        cur = dedup.get(key)
        if cur is None:
            dedup[key] = it
        else:
            p_new = it.get("price_eur")
            p_old = cur.get("price_eur")
            if p_new is not None and (p_old is None or p_new < p_old):
                dedup[key] = it

    sorted_items = sorted(dedup.values(), key=lambda x: (x["price_eur"] is None, x["price_eur"] or 0))
    return sorted_items

@app.command()
def cli(
    query: str = typer.Argument(..., help="Название/ключевые слова товара"),
    sources: Optional[str] = typer.Option(None, "--sources", help="Через запятую: salidzini,barbora,rimi,rd,maxima,one_a,euronics,drogas"),
    limit: int = typer.Option(20, "--limit", help="Ограничение результатов на источник"),
    timeout: float = typer.Option(15.0, "--timeout", help="Таймаут запроса к источнику (сек)"),
    csv: Optional[str] = typer.Option(None, "--csv", help="Путь для сохранения CSV"),
):
    src_list = [s.strip() for s in sources.split(",")] if sources else None
    items = asyncio.run(run_query(query=query, sources=src_list, limit=limit, timeout=timeout))
    print_table(items, top=50)
    if csv:
        write_csv(items, csv)
        typer.echo(f"CSV saved: {csv}")

if __name__ == "__main__":
    app()
