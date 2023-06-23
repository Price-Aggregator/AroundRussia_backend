from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   inline_serializer)
from rest_framework import serializers

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
