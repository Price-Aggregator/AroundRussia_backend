import os
from http import HTTPStatus

import requests
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import openapi
from .constants import BLOCK_CITY, COUNT_TICKET, URL_SEARCH
from .exceptions import EmptyResponseError, InvalidDateError, ServiceError
from .filter import sort_by_time, sort_transfer
from .serializers import (CitySerializer, TicketSerializer,
                          TravelListSerializer, TravelSerializer)
# noqa: I004, I001
from tickets.models import City  # noqa: I001
from travel_diary.models import Travel  # noqa: I001
from .utils import get_calendar_days, lazy_cycling
from .validators import params_validation

TOKEN = os.getenv('TOKEN')


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения городов."""
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CalendarView(APIView):

    @openapi.calendar_get
    def get(self, request):
        """
        Функция для календаря цен.
        """
        cities = [request.GET.get('origin'), request.GET.get('destination')]
        for code in cities:
            if not City.objects.filter(code=code).exists():
                return Response(
                    {
                        'InvalidIATA-code': f'Некорректный IATA-код {code}',
                    }, status=status.HTTP_404_NOT_FOUND
                )
            if code in BLOCK_CITY:
                return Response(
                    {
                        'Error': 'Извините, в данный момент аэропорт закрыт',
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        try:
            response = get_calendar_days(request)
            return Response(response, status=status.HTTP_200_OK)
        except ServiceError as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidDateError as e:
            return Response(
                {'InvalidDate': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except EmptyResponseError as e:
            return Response(
                {'EmptyResponse': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


class SearchTicketView(APIView):
    @openapi.search_ticket_post
    def post(self, request):
        """Функция для поиска билетов."""

        params = request.data
        params['token'] = TOKEN
        params['limit'] = COUNT_TICKET
        if params_validation(params):
            if 'sorting' in params and params['sorting'] == 'time':
                params['sorting'] = 'price'
                response_data = requests.get(URL_SEARCH, params=params,).json()
                response_data = sort_by_time(response_data)
            else:
                response_data = requests.get(URL_SEARCH, params=params,).json()
            if 'direct' in params and params['direct'] == 'false':
                response_data = sort_transfer(response_data)
            response_data = lazy_cycling(response_data)
            my_serializer = TicketSerializer(data=response_data, many=True)
            return Response(my_serializer.initial_data)
        return Response(HTTPStatus.BAD_REQUEST)


class TravelViewSet(viewsets.ModelViewSet):
    """ViewSet для получения путешествий."""
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TravelListSerializer
        return TravelSerializer

    def perform_create(self, serializer):
        serializer.save(traveller=self.request.user)
