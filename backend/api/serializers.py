from rest_framework import serializers
from tickets.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('code', 'name', 'latitude', 'longitude')
