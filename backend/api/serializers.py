import base64
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer as DjUserCreateSerializer
from djoser.serializers import UserSerializer as DjUserSerializer
from rest_framework import serializers  # noqa: I004
from tickets.models import City
from travel_diary.models import Activity, Travel

from .constants import BLOCK_CITY, CATEGORIES

User = get_user_model()


class AirportField(serializers.Field):
    """Поле для сериализатора.
       Проверяет что все города сейчас доступны."""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if data in BLOCK_CITY:
            raise serializers.ValidationError(
                'Извините, в данный момент аэропорт закрыт'
            )
        return data


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для вывода городов."""
    class Meta:
        model = City
        fields = ('code', 'name', 'latitude', 'longitude')


class TicketSerializer(serializers.Serializer):
    """Сериализатор для вывода билетов."""

    id = serializers.CharField(help_text='id билета')
    origin = serializers.CharField(
        max_length=10, help_text='Город отправления')
    destination = serializers.CharField(
        max_length=10, help_text='Город назначения')
    origin_airport = AirportField(
        max_length=10, help_text='Аэропорт отправления')
    destination_airport = AirportField(
        max_length=10, help_text='Аэропорт назначения')
    price = serializers.IntegerField(help_text='Цена')
    airline = serializers.CharField(max_length=10, help_text='Авиакомпания')
    flight_number = serializers.CharField(max_length=10,
                                          help_text='Номер борта')
    departure_at = serializers.DateField(help_text='Дата отправления')
    return_at = serializers.DateField(help_text='Дата возвращения')
    transfers = serializers.IntegerField(
        help_text='Количество пересадок на пути')
    return_transfers = serializers.IntegerField(
        help_text='Количество пересадок на обратном пути')
    duration = serializers.IntegerField(help_text='Длительность')
    link = serializers.URLField(help_text='Ссылка')
    currency = serializers.CharField(max_length=10, help_text='Валюта')
    arrival_time = serializers.DateField(help_text='Время прибытия')


class TicketDataserializer(serializers.Serializer):
    """Вложенный сериализатор для TickerResponseSerializer."""
    origin = serializers.CharField(help_text='Город отправления')
    destination = serializers.CharField(help_text='Город назначения')
    origin_airport = serializers.CharField(help_text='Аэропорт отправления')
    destination_airport = serializers.CharField(
        help_text='Аэропорт назначения')
    price = serializers.IntegerField(help_text='Цена')
    airline = serializers.CharField(help_text='Авиакомпания')
    flight_number = serializers.CharField(help_text='Номер борта')
    departure_at = serializers.DateTimeField(help_text='Дата отправления')
    transfers = serializers.IntegerField(
        help_text='Количество пересадок на пути')
    return_transfers = serializers.IntegerField(
        help_text='Количество пересадок на обратном пути')
    duration = serializers.IntegerField(help_text='Общая длительность')
    duration_to = serializers.IntegerField(help_text='Время пути туда')
    duration_back = serializers.IntegerField(help_text='Время пути обратно')
    link = serializers.CharField(help_text='Ссылка')


class TicketResponseSerializer(serializers.Serializer):
    """Сериализатор обрабатывает данные возвращаемые TravelPayout."""
    status = serializers.BooleanField(help_text='Статус ответа')
    data = TicketDataserializer(many=True, help_text='Данные билета')
    currency = serializers.CharField(help_text='Валюта')


class TicketRequestSerializer(serializers.Serializer):
    """Сериализатор для данных вводимых пользователем."""
    origin = serializers.CharField(help_text='Город отправления')
    destination = serializers.CharField(help_text='Город назначения')
    sorting = serializers.CharField(help_text='Сортировка')
    departure_at = serializers.CharField(help_text='Время отправления')


class UserCreateSerializer(DjUserCreateSerializer):
    """Унаследовано от Djoser, добавлены поля."""
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',
                  'sex', 'phone_number', 'birth_date')
        write_only_fields = ('password',)


class UserSerializer(DjUserSerializer):
    """Унаследовано от Djoser, добавлены поля."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'sex',
                  'phone_number', 'birth_date')


class Base64ImageField(serializers.ImageField):
    """Кастомный тип поля для декодирования медиафайлов."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format_file, image_str = data.split(';base64,')
            extension = format_file.split('/')[-1]
            data = ContentFile(
                base64.b64decode(image_str), name='temp.' + extension
            )
        return super().to_internal_value(data)


class TravelListSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода списка путешествий."""
    class Meta:
        model = Travel
        fields = ('name', 'start_date', 'end_date', 'image', 'traveler')


class TravelSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода путешествия с активностями."""
    image = Base64ImageField(required=False, allow_null=True)
    # activity = ActivitySerializer(many=True, source='travel')

    class Meta:
        model = Travel
        fields = ('name', 'start_date', 'end_date', 'image', 'traveler',
                  'travel')
        read_only_fields = ('traveler', 'travel')

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError(
                'Дата окончания путешествия не может быть раньше даты начала!'
            )
        return data


class ActivityBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для карточек."""
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Activity
        fields = ('author',
                  'travel',
                  'id',
                  'name',
                  'category',
                  'date',
                  'time',
                  'price',
                  'media')

    def validate(self, data):
        if data['category'] not in CATEGORIES:
            raise serializers.ValidationError(
                f'Допустимые категории {CATEGORIES}'
            )
        date = datetime.strptime(str(data['date']), '%Y-%m-%d')
        if date < datetime.today():
            raise serializers.ValidationError(
                'Дата не может быть раньше сегодня.'
            )
        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError(
                'Цена не может быть ниже 0.'
            )
        return data


class FlightSerializer(ActivityBaseSerializer):
    """Сериализатор для вывода перелетов."""
    origin = serializers.CharField(help_text='Введите пункт отправления',
                                   max_length=50,
                                   required=True)
    destination = serializers.CharField(help_text='Введите пункт назначения',
                                        max_length=50,
                                        required=True)

    class Meta(ActivityBaseSerializer.Meta):
        fields = ActivityBaseSerializer.Meta.fields + ('origin', 'destination')


class HotelSerializer(ActivityBaseSerializer):
    """Сериализатор для вывода отелей."""
    address = serializers.CharField(help_text='Укажите адрес',
                                    max_length=255,
                                    required=True)

    class Meta(ActivityBaseSerializer.Meta):
        fields = ActivityBaseSerializer.Meta.fields + ('address',)


class ActivitySerializer(ActivityBaseSerializer):
    """Сериализатор для вывода активностей."""
    address = serializers.CharField(help_text='Укажите адрес',
                                    max_length=255,
                                    required=True)

    class Meta(ActivityBaseSerializer.Meta):
        fields = ActivityBaseSerializer.Meta.fields + ('address',)
