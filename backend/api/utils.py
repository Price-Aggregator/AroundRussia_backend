import datetime as dt
import os
import re
from calendar import monthrange

import requests
from django.core.cache import cache
from django.utils import timezone
from rest_framework.request import Request

from .constants import (CACHE_TTL, MONTH_SLICE, PERIOD, PERIOD_MAX,
                        PERIOD_SLICE, URL_AVIASALES, URL_CALENDAR, WEEK,
                        AviaSalesData, Prices, Ticket)
from .exceptions import EmptyResponseError, InvalidDateError, ServiceError


def get_calendar_prices(
    origin: str, destination: str, date: str, return_at: str = ''
) -> Prices:
    """Утилита для получения цен для календаря."""
    headers = {'X-Access-Token': os.environ.get('TOKEN')}
    request_url = (f'{URL_CALENDAR}?'
                   f'origin={origin}&'
                   f'destination={destination}&'
                   f'departure_at={date}&'
                   f'return_at={return_at}&'
                   f'group_by=departure_at')
    data_check = get_from_cache(request_url)
    if data_check is not None:
        return data_check
    response = requests.get(
        request_url,
        headers=headers
    )
    output = response.json()
    if response is None:
        raise EmptyResponseError('Данные не получены')
    if 'error' in output:
        raise ServiceError(output['error'])
    data = output['data']
    price = []
    for result in data:
        price.append({
            'date': result,
            'price': data[result]['price']
        })
    set_the_cache(response.url, price)
    return price


def get_calendar_days(request: Request) -> Prices | None:
    """Утилита для получения дней для календаря."""
    date = request.query_params.get('departure_at')
    date_now = timezone.datetime.now().date()
    date_req = timezone.datetime.strptime(date, '%Y-%m-%d').date()
    return_at = request.query_params.get('return_at', default='')
    if date_req < date_now:
        raise InvalidDateError('Дата не может быть раньше текущего числа')
    if return_at:
        date_return = timezone.datetime.strptime(
            return_at, '%Y-%m-%d').date()
        if date_return < date_req:
            raise InvalidDateError(
                'Дата возвращения не может быть раньше даты отправления'
            )
        diff_return = date_return - date_req
        if diff_return.days > PERIOD_MAX:
            raise InvalidDateError(
                'Превышена максимально допустимая разница в 30 дней '
                'между датой отправления и датой возвращения'
            )
        return calendar_dry(request, date_now, date_req, return_at)
    return calendar_dry(request, date_now, date_req)


def calendar_dry(
    request: Request, date_now: dt.date, date_req: dt.date, return_at: str = ''
) -> Prices:
    """Утилита для обработки месяцев в календаре."""
    date = request.query_params.get('departure_at')
    origin = request.query_params.get('origin')
    destination = request.query_params.get('destination')
    period = timezone.timedelta(days=PERIOD)
    date_future = date_req + period
    date_previous = date_req - period
    current_month = get_current_month(origin, destination,
                                      date, return_at)
    diff = date_req - date_now
    month_len = monthrange(date_req.year, date_req.month)[1]
    if date_req.month < date_future.month:
        date = str(date_future)[0:MONTH_SLICE]
        if return_at:
            next_month = get_calendar_prices(origin, destination, date, date)
        else:
            next_month = get_calendar_prices(origin, destination, date)
        data = current_month + next_month
        if diff.days <= WEEK:
            return data[0:PERIOD]
        day = len(current_month) + date_req.day - (month_len + PERIOD_SLICE)
        return data[day:day + PERIOD]
    if date_previous.month < date_req.month:
        date = str(date_previous)[0:MONTH_SLICE]
        if return_at:
            previous_month = get_calendar_prices(origin, destination,
                                                 date, date)
        else:
            previous_month = get_calendar_prices(origin, destination, date)
        data = previous_month + current_month
        if diff.days <= WEEK:
            return data[0:PERIOD]
        day = len(previous_month) - (PERIOD_SLICE - date_req.day)
        return data[day:day + PERIOD]
    day = date_req.day - PERIOD_SLICE
    return current_month[day: day + PERIOD]


def get_current_month(
        origin: str, destination: str, date: str, return_at: str) -> Prices:
    """Утилита для обработки месяца даты отправления."""
    date_month = date[0:MONTH_SLICE]
    if return_at:
        data = get_calendar_prices(origin, destination, date_month, date_month)
        day_req = get_calendar_prices(origin, destination, date, return_at)
        for day in range(0, len(data) - 1):
            if data[day]['date'] == date:
                if day_req:
                    data[day]['price'] = day_req[0]['price']
                else:
                    data.pop(day)
        return data
    data = get_calendar_prices(origin, destination, date_month)
    return data


def lazy_cycling(obj: AviaSalesData) -> AviaSalesData:
    """Утилита ленивого цикла для получения билетов."""
    for ticket in obj['data']:
        add_arrival_time(ticket)
        add_url(ticket)
        add_id(ticket)
    return obj


def add_arrival_time(ticket: Ticket) -> None:
    """Утилита для добавления времени прибытия."""
    departure_time = dt.datetime.fromisoformat(ticket['departure_at'])
    way = dt.timedelta(minutes=ticket['duration_to'])
    arrival_time = departure_time + way
    ticket['arrival_time'] = arrival_time


def add_url(ticket: Ticket) -> None:
    """Утилита для добавления ссылки к билету."""
    ticket['link'] = URL_AVIASALES + ticket['link']


def add_id(ticket: Ticket) -> None:
    """Утилита длоя добавления id к билету."""
    ticket['id'] = re.search('uuid=(.*?)(?=&)', ticket['link']).group(1)


def get_from_cache(url: str) -> Prices | None:
    """
    Проверяет url на вхождение в кэш.
    Возвращает json-результат из кэша если найдет.
    Если не найдет - возвращает None.
    """
    return cache.get(url, default=None)


def set_the_cache(url: str, result: Prices) -> None:
    """
    Принимает в параметрах url и результат запроса на этот урл - json-строку.
    Записывает результат в кэш по ключу - url.
    TTL значение берется из константы.
    """
    cache.set(url, result, timeout=CACHE_TTL)
