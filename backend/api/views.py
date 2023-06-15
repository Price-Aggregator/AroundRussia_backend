import os
from http import HTTPStatus

from dotenv import load_dotenv
import requests
from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import City
from .constants import COUNT_TICKET, URL_SEARCH
from .filter import sort_by_time, sort_transfer
from .serializers import CitySerializer, TicketSerializer
from .utils import add_arrival_time, get_calendar_days
from .validators import params_validation

load_dotenv()

TOKEN = os.getenv('TOKEN')


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
            if not City.objects.filter(code=code).exists():
                return Response(
                    {
                        'InvalidIATA-code': f'Incorrect IATA-code for {code}'
                    }
                )
        response = get_calendar_days(request)
        return Response(response)


class SearchTicketView(APIView):
    def post(self, request):
        """Функция для поиска билетов."""

        params = request.data
        params['token'] = TOKEN
        params['limit'] = COUNT_TICKET
        if params_validation(params):
            if params['sorting'] == 'time':
                params['sorting'] = 'price'
                response_data = requests.get(URL_SEARCH, params=params,).json()
                response_data = sort_by_time(response_data)
            else:
                response_data = requests.get(URL_SEARCH, params=params,).json()
            if params['direct'] == 'true':
                response_data = sort_transfer(response_data)
            response_data = add_arrival_time(response_data)
            my_serializer = TicketSerializer(data=response_data, many=True)
            return Response(my_serializer.initial_data)
        return Response(HTTPStatus.BAD_REQUEST)
