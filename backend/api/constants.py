from typing import Final, TypeAlias

Ticket: TypeAlias = dict[str, str | int]
"""
Фрагмент ответа (значение ключа 'data') от
'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'.
Содержит данные списка рейсов (билетов), каждый в виде словаря:
{
    'origin': 'ABA',
    'destination': 'KJA',
    'origin_airport': 'ABA',
    'destination_airport': 'KJA',
    'price': 3013,
    'airline': 'KV',
    'flight_number': '102',
    'departure_at': '2023-08-03T22:25:00+07:00',
    'transfers': 0, 'return_transfers': 0,
    'duration': 65,
    'duration_to': 65,
    'duration_back': 0,
    'link': '/search/ABA0308KJA1?
             t=KV16910763001691080200000065ABAKJA_ \
                370e23d93b043cd4f9b0274783b1dd2f_3013 \
             &search_date=17072023 \
             &expected_price_uuid=1f4a3091-cc70-4fd0-93ee-71ff0489644a \
             &expected_price_source=share&expected_price_currency=rub \
             &expected_price=3013',
}.
"""

AviaSalesData: TypeAlias = dict[str, str | bool | list[Ticket]]
"""
Ответ от 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'
в виде словаря: {'success': True, 'data': [Ticket], 'currency': 'rub'}.
"""

Prices: TypeAlias = list[dict[str, str | int]]

URL_WITH_CITIES: Final[str] = (
    'https://api.travelpayouts.com/data/ru/cities.json?_gl=1'
    '*100i7ih*_ga*MTUzMTY3NDIzNi4xNjg1ODI4ODQx*_ga_1WLL0NEBEH'
    '*MTY4NjA2MDAyMi45LjAuMTY4NjA2MDAyMi42MC4wLjA.'
)
"""Ссылка содержащая список городов с их координатами и IATA кодами."""

URL_CALENDAR: Final[str] = (
    'https://api.travelpayouts.com/aviasales/v3/grouped_prices'
)
"""Ссылка содержащая сгруппированные цены для календаря."""

URL_SEARCH: Final[str] = (
    'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'
)
"""Ссылка содержащая сгруппированные цены по датам."""

URL_AVIASALES: Final[str] = 'https://www.aviasales.ru'
"""Ссылка на сайт aviasales.ru."""

COUNT_TICKET: Final[int] = 1000
"""Количество билетов в ответе."""

CACHE_TTL: Final[int] = 60
"""Время в течении которого кэш валиден (в секундах).
   Для тестирования указана 1 минута. 12 часов = 43200."""

MONTH_SLICE: Final[int] = 7
"""Индекс для среза строки даты, возвращает подстроку в формате YYYY-MM."""

WEEK: Final[int] = 7
"""Количество дней в неделе."""

PERIOD_MAX: Final[int] = 30
"""Максимально допустимая разница между датой вылета и возврата."""

PERIOD: Final[int] = 15
"""Количество дней за которые будут возвращаться цены."""

PERIOD_SLICE: Final[int] = 8
"""Количество дней до/после запрашиваемой даты включительно."""

BLOCK_CITY: Final[set[str]] = {'AAQ', 'EGO', 'BZK', 'VOZ', 'GDZ', 'KRR',
                               'URS', 'LPK', 'URS', 'ROV', 'ESL', 'SIP'}
"""Города закрытые из-за СВО."""

CATEGORIES: Final[set[str]] = {'activity', 'flight', 'hotel'}
"""Допустимые категории активностей."""
