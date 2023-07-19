from typing import TypeAlias

Prices: TypeAlias = list[dict[str, str | int]]

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
