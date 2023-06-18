import os
from http import HTTPStatus

from dotenv import load_dotenv
import requests
from rest_framework import filters, status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from tickets.models import City
from drf_spectacular.utils import (extend_schema, inline_serializer,
                                   OpenApiParameter, OpenApiResponse,)
from .constants import COUNT_TICKET, URL_SEARCH
from .filter import sort_by_time, sort_transfer
from .serializers import (CitySerializer, TicketSerializer,
                          TicketRequestSerializer,
                          TicketResponseSerializer)
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
    @extend_schema(
        parameters=[
            OpenApiParameter(
                'origin',
                description='IATA-code for origin city'
            ),
            OpenApiParameter(
                'destination',
                description='IATA-code for destination city'
            ),
            OpenApiParameter(
                'departure_at',
                description=('Date of departure from the city departure'
                             '(in the format YYYY-MM-DD)')
            )
        ],
        responses={
            200: inline_serializer(
                'Getting_date_prices',
                fields={
                    'date': serializers.CharField(),
                    'price': serializers.IntegerField()
                }
            ),
            400: inline_serializer(
                'Bad_request',
                fields={
                    'InvalidDate': serializers.CharField()
                }
            ),
            404: inline_serializer(
                'Not_found',
                fields={
                    'Invalid IATA-code': serializers.CharField()
                }
            )
        }
    )
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
                        'InvalidIATA-code': f'Incorrect IATA-code for {code}',
                    }, status=status.HTTP_404_NOT_FOUND
                )
        response = get_calendar_days(request)
        if 'InvalidDate' in response:
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
                    '(optional if destination set) IATA-code for origin city')
            ),
            OpenApiParameter(
                'destination',
                description=(
                    '(optional if origin set) IATA-code for destination city')
            ),
            OpenApiParameter(
                'departure_at',
                description=(
                    '(optional) Date of departure from the city departure'
                    '(in the format YYYY-MM-DD)')
            ),
            OpenApiParameter(
                'return_at',
                description=(
                    '(optional) Date of return from the city departure'
                    '(in the format YYYY-MM-DD)')
            ),
            OpenApiParameter(
                'one_way',
                description=(
                    '(optional) One way ticket. true or false true by default')
            ),
            OpenApiParameter(
                'direct',
                description=(
                    '(optional) Only direct flights.'
                    'true or false. false by default')
            ),
            OpenApiParameter(
                'limit',
                description=(
                    '(optional) Number of records in answer.'
                    'max=1000. 30 by default')
            ),
            OpenApiParameter(
                'page',
                description='(optional) Page number.'
            ),
            OpenApiParameter(
                'sorting',
                description=(
                    '(optional) Sorting type.'
                    'Available sorting: time, price, route.')
            ),

            OpenApiParameter(
                'token',
                description='(required if not in .env) travelpayout API token'
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
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                params['sorting'] = 'price'
                response_data = requests.get(URL_SEARCH, params=params,).json()
                response_data = sort_by_time(response_data)
            else:
                response_data = requests.get(URL_SEARCH, params=params,).json()
            if 'direct' in params and params['direct'] == 'true':
                response_data = sort_transfer(response_data)
            response_data = add_arrival_time(response_data)
            my_serializer = TicketSerializer(data=response_data, many=True)
            return Response(my_serializer.initial_data)
        return Response(HTTPStatus.BAD_REQUEST)
