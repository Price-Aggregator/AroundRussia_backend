
from django.urls import path

from .views import CalendarViewSet


urlpatterns = [
    path('calendar', CalendarViewSet.as_view({'get': 'get'}))
]
