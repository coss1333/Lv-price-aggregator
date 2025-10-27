from typing import List, Dict, Any
from tabulate import tabulate
import pandas as pd

def print_table(items: List[Dict[str, Any]], top: int = 50):
    headers = ["price_eur","promo","store","title","source","url"]
    rows = []
    for it in items[:top]:
        rows.append([it.get("price_eur"), "YES" if it.get("promo") else "", it.get("store"), it.get("title"), it.get("source"), it.get("url")])
    print(tabulate(rows, headers=headers, tablefmt="github", floatfmt=".2f"))

def write_csv(items: List[Dict[str, Any]], path: str):
    df = pd.DataFrame(items)
    df.to_csv(path, index=False, encoding="utf-8")
