from rest_framework.response import Response
from rest_framework.views import APIView
from tickets.models import City

from .utils import get_calendar_days


class CalendarView(APIView):

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
            if not City.objects.filter(code=code):
                return Response(
                    {
                        'InvalidIATA-code': f'Incorrect IATA-code for {code}'
                    }
                )
        response = get_calendar_days(request)
        return Response(response)
