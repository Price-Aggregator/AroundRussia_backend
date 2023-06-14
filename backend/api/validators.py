from datetime import datetime


def params_validation(params):
    if params['origin'] and (len(params['origin']) < 2
                             or len(params['origin']) > 3):
        return False

    if params['destination'] and (len(params['destination']) > 3
                                  or len(params['destination']) < 2):
        return False

    if params['origin'] and params['destination']:
        if params['origin'] == params['destination']:
            return False

    if params['departure_at'] and params['departure_at'] < datetime.today():
        return False

    if params['return_at'] and params['return_at'] < datetime.today():
        return False

    if params['limit'] and params['limit'] > 1000:
        return False

    sorting_variants = ['price', 'route', 'time']
    if params['sorting'] not in sorting_variants:
        return False

    return True
