from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   inline_serializer, OpenApiResponse)
from rest_framework import serializers
from .serializers import TicketRequestSerializer, TicketResponseSerializer

calendar_get = extend_schema(
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

search_ticket_post = extend_schema(description=(
    'Функция для поиска билетов. '
    'Запросы необходимо передавать через RequestBody'),
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
