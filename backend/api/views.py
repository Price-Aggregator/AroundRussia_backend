import requests

from rest_framework import filters, viewsets
from rest_framework.response import Response

from tickets.models import City
from .serializers import CitySerializer, TicketSerializer
from .constants import URL_SEARCH, COUNT_TICKET
from .filter import sort_by_time


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


def find_ticket(request, format=None):
    """Функция для поиска билетов."""

    HEADERS = request.data
    HEADERS['token'] = 'fc0490ceb2e8db1f3f383adb035ea3e2'
    HEADERS['limit'] = COUNT_TICKET
    if HEADERS['sorting'] == 'time':
        HEADERS['sorting'] = 'price'
        response_data = requests.get(URL_SEARCH, params=HEADERS,).json()
        response_data = sort_by_time(response_data)
        my_serializer = TicketSerializer(data=response_data, many=True)
        return Response(data=my_serializer.initial_data)
    else:
        response_data = requests.get(URL_SEARCH, params=HEADERS,).json()
        my_serializer = TicketSerializer(data=response_data, many=True)
        return Response(data=my_serializer.initial_data)
