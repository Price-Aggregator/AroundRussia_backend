from rest_framework import filters, viewsets

from tickets.models import City
from .serializers import CitySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
