from rest_framework import serializers

from tickets.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class TicketSerializer(serializers.Serializer):

    origin = serializers.CharField(max_length=10)
    destination = serializers.CharField(max_length=10)
    origin_airport = serializers.CharField(max_length=10)
    destination_airport = serializers.CharField(max_length=10)
    price = serializers.IntegerField()
    airline = serializers.CharField(max_length=10)
    flight_number = serializers.CharField(max_length=10)
    departure_at = serializers.DateField()
    return_at = serializers.DateField()
    transfers = serializers.IntegerField()
    return_transfers = serializers.IntegerField()
    duration = serializers.IntegerField()
    link = serializers.URLField()
    currency = serializers.CharField(max_length=10)
