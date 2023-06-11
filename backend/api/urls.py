from django.urls import path

from .views import CalendarView

urlpatterns = [
    path('calendar', CalendarView.as_view())
]
