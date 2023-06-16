from datetime import datetime


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
        departure_at = datetime.strptime(params['departure_at'], '%Y-%m-%d')
        if departure_at < datetime.today():
            return False

    if 'return_at' in params:
        return_at = datetime.strptime(params['return_at'], '%Y-%m-%d')
        if return_at < datetime.today():
            return False

    if 'sorting' in params:
        sorting_variants = ['price', 'route', 'time']
        if params['sorting'] not in sorting_variants:
            return False

    return True
