from requests import get

from django.core.management import BaseCommand

from api.constants import URL_WITH_CITIES
from tickets.models import City


class Command(BaseCommand):
    help = 'Filling the database with cities'

    def handle(self, *args, **kwargs):
        response = get(URL_WITH_CITIES).json()
        cities = []
        for city in response:
            if city['country_code'] == 'RU' and city.get('name') is not None:
                cities.append(city)
        City.objects.bulk_create(
            City(
                code=city['code'],
                name=city['name'],
                latitude=city['coordinates']['lat'],
                longitude=city['coordinates']['lon']
            ) for city in cities
        )
