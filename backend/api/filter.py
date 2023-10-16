from .types import AviaSalesData


def sort_by_time(sorted_obj: AviaSalesData) -> AviaSalesData:
    """Сортировка билетов по времени."""
    sorted_obj['data'].sort(key=lambda x: x.get('departure_at'))


def sort_transfer(sorted_obj: AviaSalesData) -> AviaSalesData:
    """Сортировка билетов по наличию пересадок."""
    sorted_obj['data'] = [ticket for ticket in sorted_obj['data']
                          if ticket['transfers'] == 1]
