import os
from datetime import date
from datetime import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import serializers


def params_validation(params) -> bool:  # noqa
    """Валидация вводимых пользователем данных."""

    if 'origin' not in params and 'destination' not in params:
        return False

    if 'origin' in params and (len(params['origin']) < 2
                               or len(params['origin']) > 3):
        return False

    if 'destination' in params and (len(params['destination']) > 3
                                    or len(params['destination']) < 2):
        return False

    if 'origin' in params and 'destination' in params:
        if params['origin'] == params['destination']:
            return False

    if 'departure_at' in params:
        if len(params['departure_at'].split('-')) == 3:
            departure_at = dt.strptime(
                params['departure_at'], '%Y-%m-%d')
        else:
            departure_at = dt.strptime(params['departure_at'], '%Y-%m')
        if departure_at < dt.today():
            return False

    if 'return_at' in params:
        if len(params['return_at'].split('-')) == 3:
            return_at = dt.strptime(params['return_at'], '%Y-%m-%d')
        else:
            return_at = dt.strptime(params['return_at'], '%Y-%m')
        if return_at < dt.today():
            return False

    if 'sorting' in params:
        sorting_variants = ['price', 'route', 'time']
        if params['sorting'] not in sorting_variants:
            return False

    return True


def validate_file_extension(value) -> None:  # noqa
    """Валидация типа файла."""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемый тип файла.')


def travel_dates_validator(start: date, end: date) -> None:
    """Валидация дат начала и окончания путешествия."""
    if end < start:
        raise serializers.ValidationError(
            'Дата окончания путешествия не может '
            'быть раньше даты начала!'
        )
    if start < dt.today().date():
        raise serializers.ValidationError(
            'Дата начала не может быть раньше чем сегодня!'
        )
