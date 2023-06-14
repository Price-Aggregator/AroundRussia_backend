import requests

from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import City
from .serializers import CitySerializer, TicketSerializer
from .constants import URL_SEARCH, COUNT_TICKET
from .filter import sort_by_time
from .utils import get_calendar_days


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CalendarView(APIView):

    def get(self, request):
        """
        View for price calendar.
        :param origin: The IATA-code for city departure.
        :param destination: The IATA-code for city destination.
        :param departure_at: Date of departure from the
        city departure (in the format YYYY-MM-DD).
        :return: data{date: price} for departure_at +-15 days in advance.
        """
        cities = [request.GET.get('origin'), request.GET.get('destination')]
        for code in cities:
            if not City.objects.filter(code=code):
                return Response(
                    {
                        'InvalidIATA-code': f'Incorrect IATA-code for {code}'
                    }
                )
        response = get_calendar_days(request)
        return Response(response)


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
