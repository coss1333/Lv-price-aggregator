import re
from typing import Optional

def normalize_price(val) -> Optional[float]:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val)
    s = re.sub(r"[€\s]", "", s)
    s = s.replace(",", ".")
    m = re.search(r"([0-9]+\.?[0-9]*)", s)
    if not m:
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None

def cleanse_text(text: str) -> str:
    text = re.sub("\s+", " ", text or "").strip()
    return text[:300]
