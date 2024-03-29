import os
from http import HTTPStatus

import requests
from django.core.cache import cache
from django.db.models import Sum
from djoser.views import TokenCreateView as DjTokenCreateView
from djoser.views import TokenDestroyView as DjTokenDestroyView
from rest_framework import filters, mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
# noqa I004
from faq.models import FAQ, FAQ_CACHE_KEY  # noqa: I001
from tickets.models import City
from travel_diary.models import Activity, Travel
from . import openapi  # noqa: I003
from .constants import BLOCK_CITY, COUNT_TICKET, URL_SEARCH
from .exceptions import EmptyResponseError, InvalidDateError, ServiceError
from .filter import sort_by_time, sort_transfer
from .permissions import IsAuthorOrAdmin
from .serializers import (ActivitySerializer, CitySerializer, FAQSerializer,
                          TicketSerializer, TravelListSerializer,
                          TravelSerializer)
from .utils import get_calendar_days, lazy_cycling
from .validators import params_validation

TOKEN = os.getenv('TOKEN')


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet для получения городов."""
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CalendarView(APIView):

    @openapi.calendar_get
    def get(self, request: Request) -> Response:
        """
        Функция для календаря цен.
        """
        cities = [request.query_params.get('origin'),
                  request.query_params.get('destination')]
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
    def post(self, request: Request) -> Response:
        """Функция для поиска билетов."""

        params = request.data
        params['token'] = TOKEN
        params['limit'] = COUNT_TICKET
        if params_validation(params):
            if 'sorting' in params and params['sorting'] == 'time':
                params['sorting'] = 'price'
                response_data = requests.get(URL_SEARCH, params=params,).json()
                sort_by_time(response_data)
            else:
                response_data = requests.get(URL_SEARCH, params=params,).json()
            if 'direct' in params and params['direct'] == 'false':
                sort_transfer(response_data)
            response_data = lazy_cycling(response_data)
            my_serializer = TicketSerializer(data=response_data, many=True)
            return Response(my_serializer.initial_data)
        return Response(HTTPStatus.BAD_REQUEST)


class TokenCreateView(DjTokenCreateView):
    """Исправлена документация."""
    @openapi.token_login
    def post(self, request: Request, **kwargs) -> Response:
        return super().post(request, **kwargs)


class TokenDestroyView(DjTokenDestroyView):
    """Исправлена документация."""
    @openapi.token_destroy
    def post(self, request: Request) -> Response:
        return super().post(request)


class TravelViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet для получения путешествий."""
    permission_classes = (IsAuthorOrAdmin,)

    def get_queryset(self):
        queryset = (Travel.objects.all() if self.request.user.is_staff
                    else Travel.objects.filter(traveler=self.request.user))
        return queryset.annotate(
            total_price=Sum('activities__price')
        ).order_by('-id')

    def get_serializer_class(self) -> Serializer:
        return (TravelListSerializer if self.action == 'list'
                else TravelSerializer)

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(traveler=self.request.user)


class ActivityViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """Базовый ViewSet для карточек."""
    queryset = Activity.objects.all()
    permission_classes = (IsAuthorOrAdmin,)
    serializer_class = ActivitySerializer

    def perform_create(self, serializer: Serializer) -> None:
        """Переопределение метода perform_create."""
        serializer.save(author=self.request.user)


class FAQViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    "ViewSet returns a frequently asked questions list."
    serializer_class = FAQSerializer

    def get_queryset(self):
        return cache.get_or_set(FAQ_CACHE_KEY, FAQ.objects.all, timeout=None)
