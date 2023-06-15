from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CalendarView, CityViewSet, SearchTicketView

app_name = 'api'

router = DefaultRouter()

router.register('cities', CityViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('calendar', CalendarView.as_view()),
    path('airline', SearchTicketView.as_view()),
]

