import os
from http import HTTPStatus

from drf_spectacular.utils import (extend_schema, inline_serializer,
                                   OpenApiParameter, OpenApiResponse)
import requests
from rest_framework import filters, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import COUNT_TICKET, URL_SEARCH
from .filter import sort_by_time, sort_transfer
from .serializers import (CitySerializer, TicketSerializer,
                          TicketRequestSerializer,
                          TicketResponseSerializer)
from .utils import get_calendar_days, lazy_cycling
from .validators import params_validation
from tickets.models import City

TOKEN = os.getenv('TOKEN')


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CalendarView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                'origin',
                description='IATA-код города отправления'
            ),
            OpenApiParameter(
                'destination',
                description='IATA-код города назначения'
            ),
            OpenApiParameter(
                'departure_at',
                description="""Дата отправления из города отправления
                                 (в формате YYYY-MM-DD)"""
            )
        ],
        responses={
            200: inline_serializer(
                'Получение дат цен',
                fields={
                    'date': serializers.CharField(),
                    'price': serializers.IntegerField()
                }
            ),
            400: inline_serializer(
                'Bad request',
                fields={
                    'ERROR': serializers.CharField()
                }
            )
        }
    )
    def get(self, request):
        """
        View для календаря цен.
        """
        cities = [request.GET.get('origin'), request.GET.get('destination')]
        for code in cities:
            if not City.objects.filter(code=code).exists():
                return Response(
                    {
                        'InvalidIATA-code': f'Некорректный IATA-код {code}',
                    }, status=status.HTTP_404_NOT_FOUND
                )
        response = get_calendar_days(request)
        if 'InvalidDate' in response or 'error' in response:
            stat = status.HTTP_400_BAD_REQUEST
        else:
            stat = status.HTTP_200_OK
        return Response(response, status=stat)


class SearchTicketView(APIView):
    @extend_schema(description=(
        'Функция для поиска билетов. '
        ' Запросы необходимо передавать через RequestBody'),
        parameters=[
            OpenApiParameter(
                'origin',
                description=(
                    '(Опционально если указан destination)'
                    'IATA-код города отправления')
            ),
            OpenApiParameter(
                'destination',
                description=(
                    '(Опционально если указан origin)'
                    'IATA-код города назначения')
            ),
            OpenApiParameter(
                'departure_at',
                description=(
                    '(Опционально) Дата отправления из города отправления'
                    '(в формате YYYY-MM-DD)')
            ),
            OpenApiParameter(
                'return_at',
                description=(
                    '(Опционально) Дата возвращения'
                    '(в формате YYYY-MM-DD)')
            ),
            OpenApiParameter(
                'one_way',
                description=(
                    '(Опционально) Билет в один конец.'
                    'true или false, true по умолчанию.')
            ),
            OpenApiParameter(
                'direct',
                description=(
                    '(Опционально) Только рейсы без пересадок.'
                    'true или false. false по умолчанию.')
            ),
            OpenApiParameter(
                'limit',
                description=(
                    '(Опционально) Количество записей в ответе.'
                    'max=1000. 30 по умолчанию')
            ),
            OpenApiParameter(
                'page',
                description='(Опционально) Номер страницы.'
            ),
            OpenApiParameter(
                'sorting',
                description=(
                    'Тип сортировки.'
                    'Допустимые значения: time, price, route.')
            )
    ],
        request=TicketRequestSerializer(),
        responses={
            200: OpenApiResponse(response=TicketResponseSerializer()),
            400: inline_serializer(
                'Bad_Request',
                fields={
                    'InvalidData': serializers.CharField()
                }
            ),
            404: inline_serializer(
                'Not_Found',
                fields={
                    'Invalid IATA-code': serializers.CharField()
                }
            )
    }
    )
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
            if 'direct' in params and params['direct'] == 'true':
                response_data = sort_transfer(response_data)
            response_data = lazy_cycling(response_data)
            my_serializer = TicketSerializer(data=response_data, many=True)
            return Response(my_serializer.initial_data)
        return Response(HTTPStatus.BAD_REQUEST)
