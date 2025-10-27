# LV Price Aggregator (MVP)

Сборщик выгодных цен и акций по магазинам Латвии. Архитектура плагинов:
каждый магазин — отдельный adapter в `adapters/`. Скрипт асинхронно
обращается к адаптерам, нормализует цены, помечает акции, и выводит
самые выгодные предложения на момент запроса.

ВАЖНО: Уважайте robots.txt и условия использования сайтов. Где доступно —
используйте официальные API/feeds. Селекторы/маршруты страниц у магазинов
меняются — адаптеры могут потребовать правок.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Простой поиск
python main.py "kafija" --limit 10

# Сохранить в CSV
python main.py "piens 2.5%" --csv data/output.csv

# Включить только некоторые источники
python main.py "olīveļļa" --sources salidzini,barbora,rimi
```
