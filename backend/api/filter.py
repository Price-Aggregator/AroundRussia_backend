def sort_by_time(sorted_obj):
    sorted_obj['data'].sort(key=lambda x: x.get('departure_at'))
    return sorted_obj


def sort_transfer(sorted_obj):
    result = []
    data = sorted_obj['data']
    for ticket in data:
        if ticket['transfers'] == '1':
            result.append(data[ticket]['transfers'])
    sorted_obj['data'] = result
    return sorted_obj
