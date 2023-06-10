import os
import requests
from .constants import URL_CALENDAR

from dotenv import load_dotenv

load_dotenv()


def get_calendar_prices(origin, destination, date):
    HEADERS = {'X-Access-Token': os.environ.get('TOKEN')}
    payload = {
        'origin': origin,
        'destination': destination,
        'departure_at': date[0:7],
        'group_by': 'departure_at'}
    response = requests.get(
        URL_CALENDAR,
        headers=HEADERS,
        params=payload
    ).json()
    data = response['data']
    price = []
    for res in data:
        price.append({
            'date': res,
            'price': data[res]['price']
        },)
    return price
