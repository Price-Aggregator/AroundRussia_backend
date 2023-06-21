from calendar import monthrange
import datetime as dt
import os
import re

from django.core.cache import cache
from django.utils import timezone
import requests

from .constants import (CACHE_TTL, MONTH_SLICE, PERIOD, PERIOD_SLICE,
                        URL_CALENDAR, URL_AVIASALES, WEEK)
from .exceptions import EmptyResponse, InvalidDate, ServiceError


def get_calendar_prices(origin, destination, date):
    headers = {'X-Access-Token': os.environ.get('TOKEN')}
    request_url = (f'{URL_CALENDAR}?'
                   f'origin={origin}&'
                   f'destination={destination}&'
                   f'departure_at={date[0:MONTH_SLICE]}&'
                   f'group_by=departure_at')
    data_check = get_from_cache(request_url)
    if data_check is not None:
        return data_check
    response = requests.get(
        request_url,
        headers=headers
    )
    if response is None or response.json()['data'] == {}:
        raise EmptyResponse('Данные не получены')
    if 'error' in response.json():
        raise ServiceError(response.json()['error'])
    data = response.json()['data']
    price = []
    for result in data:
        price.append({
            'date': result,
            'price': data[result]['price']
        })
    set_the_cache(response.url, price)
    return price


def get_calendar_days(request):
    date = request.GET.get('departure_at')
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    period = timezone.timedelta(days=PERIOD)
    date_now = timezone.datetime.now().date()
    date_req = timezone.datetime.strptime(date, '%Y-%m-%d').date()
    date_future = date_req + period
    date_previous = date_req - period
    if date_req < date_now:
        raise InvalidDate('Дата не может быть раньше текущего числа')
    current_month = get_calendar_prices(origin, destination, date)
    diff = date_req - date_now
    month_len = monthrange(date_req.year, date_req.month)[1]
    if date_req.month < date_future.month:
        date = str(date_future)
        next_month = get_calendar_prices(origin, destination, date)
        data = current_month + next_month
        if diff.days <= WEEK:
            return data[0:PERIOD]
        day = len(current_month) + date_req.day - (month_len + PERIOD_SLICE)
        return data[day:day + PERIOD]
    elif date_previous.month < date_req.month:
        date = str(date_previous)
        previous_month = get_calendar_prices(origin, destination, date)
        data = previous_month + current_month
        if diff.days <= WEEK:
            return data[0:PERIOD]
        day = len(previous_month) - (PERIOD_SLICE - date_req.day)
        return data[day:day + PERIOD]
    day = date_req.day - PERIOD_SLICE
    return current_month[day: day + PERIOD]


def lazy_cycling(obj):
    for ticket in obj['data']:
        add_arrival_time(ticket)
        add_url(ticket)
        add_id(ticket)
    return obj


def add_arrival_time(ticket):
    departure_time = dt.datetime.fromisoformat(ticket['departure_at'])
    way = dt.timedelta(minutes=ticket['duration_to'])
    arrival_time = departure_time + way
    ticket['arrival_time'] = arrival_time


def add_url(ticket):
    ticket['link'] = URL_AVIASALES + ticket['link']


def add_id(ticket):
    ticket['id'] = re.search('uuid=(.*?)(?=&)', ticket['link']).group(1)


def get_from_cache(url):
    """
    Проверяет url на вхождение в кэш.
    Возвращает json-результат из кэша если найдет.
    Если не найдет - возвращает None.
    """
    return cache.get(url, default=None)


def set_the_cache(url, result):
    """
    Принимает в параметрах url и результат запроса на этот урл - json-строку.
    Записывает результат в кэш по ключу - url.
    TTL значение берется из константы.
    """
    cache.set(url, result, timeout=CACHE_TTL)
