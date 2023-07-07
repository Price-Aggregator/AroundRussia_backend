from datetime import datetime
import os

from django.core.exceptions import ValidationError


def params_validation(params):  # noqa
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
            departure_at = datetime.strptime(
                params['departure_at'], '%Y-%m-%d')
        else:
            departure_at = datetime.strptime(params['departure_at'], '%Y-%m')
        if departure_at < datetime.today():
            return False

    if 'return_at' in params:
        if len(params['return_at'].split('-')) == 3:
            return_at = datetime.strptime(params['return_at'], '%Y-%m-%d')
        else:
            return_at = datetime.strptime(params['return_at'], '%Y-%m')
        if return_at < datetime.today():
            return False

    if 'sorting' in params:
        sorting_variants = ['price', 'route', 'time']
        if params['sorting'] not in sorting_variants:
            return False

    return True


def validate_file_extension(value):  # noqa
    """Валидация типа файла."""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемый тип файла.')
