import requests
from django.core.management import BaseCommand  # noqa: I001
# noqa: I004
from api.constants import URL_WITH_CITIES
from tickets.models import City


class Command(BaseCommand):
    help = 'Filling the database with cities'

    def handle(self, *args, **kwargs) -> None:
        try:
            City.objects.bulk_create(
                City(
                    code=city['code'],
                    name=city['name'],
                    latitude=city['coordinates']['lat'],
                    longitude=city['coordinates']['lon'],
                ) for city in requests.get(URL_WITH_CITIES).json()
                if city['country_code'] == 'RU'
                and city.get('name') is not None
            )
        except (AttributeError, KeyError, TypeError):
            raise ValueError(
                'Неверный формат данных для загрузки таблицы городов'
            )
