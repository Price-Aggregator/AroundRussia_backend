from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CalendarView, CityViewSet, SearchTicketView,
                    TokenCreateView, TokenDestroyView, TravelViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('cities', CityViewSet)
router.register('travels', TravelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('calendar', CalendarView.as_view()),
    path('airline', SearchTicketView.as_view()),
    path(r"^auth/token/login/?$", TokenCreateView.as_view(), name='login'),
    path(r"^auth/token/logout/?$", TokenDestroyView.as_view(), name="logout"),
    path('', include('djoser.urls'))
]
