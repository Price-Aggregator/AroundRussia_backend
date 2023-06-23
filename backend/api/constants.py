from typing import Final

URL_WITH_CITIES: Final[str] = (
    'https://api.travelpayouts.com/data/ru/cities.json?_gl=1'
    '*100i7ih*_ga*MTUzMTY3NDIzNi4xNjg1ODI4ODQx*_ga_1WLL0NEBEH'
    '*MTY4NjA2MDAyMi45LjAuMTY4NjA2MDAyMi42MC4wLjA.'
)

URL_CALENDAR: Final[str] = (
    'https://api.travelpayouts.com/aviasales/v3/grouped_prices'
)

URL_SEARCH: Final[str] = (
    'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'
)

URL_AVIASALES: Final[str] = 'https://www.aviasales.ru'

COUNT_TICKET: Final[int] = 1000

CACHE_TTL: Final[int] = 60  # That's one minute for testing, 12 hours is 43200

MONTH_SLICE: Final[int] = 7
"""Индекс для среза строки даты, возвращает подстроку в формате YYYY-MM"""

WEEK: Final[int] = 7

PERIOD: Final[int] = 15
"""Количество дней за которые будут возвращаться цены"""

PERIOD_SLICE: Final[int] = 8
"""Количество дней до/после запрашиваемой даты включительно"""
