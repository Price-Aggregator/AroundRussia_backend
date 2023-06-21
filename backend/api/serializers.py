from rest_framework import serializers
from tickets.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('code', 'name', 'latitude', 'longitude')


class TicketSerializer(serializers.Serializer):
    """Сериализатор для вывода билетов."""

    id = serializers.CharField()
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
    arrival_time = serializers.DateField()


class TicketDataserializer(serializers.Serializer):
    origin = serializers.CharField()
    destination = serializers.CharField()
    origin_airport = serializers.CharField()
    destination_airport = serializers.CharField()
    price = serializers.IntegerField()
    airline = serializers.CharField()
    flight_number = serializers.CharField()
    departure_at = serializers.DateTimeField()
    transfers = serializers.IntegerField()
    return_transfers = serializers.IntegerField()
    duration = serializers.IntegerField()
    duration_to = serializers.IntegerField()
    duration_back = serializers.IntegerField()
    link = serializers.CharField()


class TicketResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    data = TicketDataserializer(many=True)
    currency = serializers.CharField()


class TicketRequestSerializer(serializers.Serializer):
    origin = serializers.CharField(help_text='Город отправления')
    destination = serializers.CharField(help_text='Город назначения')
    sorting = serializers.CharField(help_text='Сортировка')
    departure_at = serializers.CharField(help_text='Время отправления')
