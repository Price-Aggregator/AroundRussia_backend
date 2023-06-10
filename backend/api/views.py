import requests

from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import City
from .serializers import CitySerializer, TicketSerializer


URL_2 = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


HEADERS = {
    'origin': 'MOW',
    'destination': 'DXB',
    'departure_at': '2023-07',
    'return_at': '2023-08',
    'market': 'ru',
    'token': 'fc0490ceb2e8db1f3f383adb035ea3e2'
}


class TickerAirline(APIView):
    def get(self, request, format=None):
        response_data = requests.get(URL_2, params=HEADERS,).json()
        my_serializer = TicketSerializer(data=response_data, many=True)
        return Response(data=my_serializer.initial_data)
