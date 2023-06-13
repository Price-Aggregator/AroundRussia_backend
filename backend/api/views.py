import requests

from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from tickets.models import City
from .serializers import CitySerializer, TicketSerializer


URL_2 = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


@api_view(['POST'])
def get_ticket(request, format=None):
    """Функция для поиска билетов."""

    if request.method == 'POST':
        HEADERS = request.data
        HEADERS['token'] = 'fc0490ceb2e8db1f3f383adb035ea3e2'
        response_data = requests.get(URL_2, params=HEADERS,).json()
        my_serializer = TicketSerializer(data=response_data, many=True)
        return Response(data=my_serializer.initial_data)
