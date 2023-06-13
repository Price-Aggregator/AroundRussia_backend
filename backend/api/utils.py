import datetime as dt
import os

import requests
#from dotenv import load_dotenv

from .constants import URL_CALENDAR

#load_dotenv()


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
        })
    return price


def get_calendar_days(request):
    date = request.GET.get('departure_at')
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    period = dt.timedelta(days=15)
    date_now = dt.datetime.now().date()
    date_req = dt.datetime.strptime(date, '%Y-%m-%d').date()
    date_future = date_req + period
    date_previous = date_req - period
    current_month = get_calendar_prices(origin, destination, date)
    diff = date_req - date_now
    if date_req < date_now:
        return {'InvalidDate': 'Entered past date'}
    if date_req.month < date_future.month:
        date = str(date_future)
        next_month = get_calendar_prices(origin, destination, date)
        data = current_month + next_month
        if diff.days <= 15:
            return data[0: diff.days + 15]
        day = len(current_month) + date_req.day - 45
        return data[day:day + 30]
    elif date_previous.month < date_req.month:
        date = str(date_previous)
        previous_month = get_calendar_prices(origin, destination, date)
        data = previous_month + current_month
        if diff.days <= 15:
            return data[0: diff.days + 15]
        day = len(previous_month) - (15 - date_req.day)
        return data[day:day + 30]
    return current_month
