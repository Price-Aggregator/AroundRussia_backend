from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import datetime as dt
from .utils import get_calendar_prices


class CalendarViewSet(ViewSet):

    def get(self, request):
        date = request.GET.get('departure_at')
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        period = dt.timedelta(days=28)
        date_req = dt.datetime.strptime(date, '%Y-%m-%d').date()
        date_future = date_req + period
        current_month = get_calendar_prices(origin, destination, date)
        if date_req.month != date_future.month:
            date = str(date_future)
            next_month = get_calendar_prices(origin, destination, date)
            data = current_month + next_month
            if date_req.day > 15:
                day = date_req.day - 15
                return Response(data[day:day + 30])
            return Response(data[0:30])
        return Response(current_month)
