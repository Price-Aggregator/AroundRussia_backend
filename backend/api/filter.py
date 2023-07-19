from .types import AviaSalesData


def sort_by_time(sorted_obj: AviaSalesData) -> AviaSalesData:
    """Сортировка билетов по времени."""
    sorted_obj['data'].sort(key=lambda x: x.get('departure_at'))
    return sorted_obj


def sort_transfer(sorted_obj: AviaSalesData) -> AviaSalesData:
    """Сортировка билетов по наличию пересадок."""
    result = []
    data = sorted_obj['data']
    for ticket in data:
        if ticket['transfers'] == 1:
            result.append(ticket)
    sorted_obj['data'] = result
    return sorted_obj
