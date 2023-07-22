from datetime import datetime

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjUserCreateSerializer
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from tickets.models import City
from travel_diary.models import Activity, Image, Travel

from .constants import BLOCK_CITY, CATEGORIES
from .fields import Base64ImageField
from .validators import travel_dates_validator

User = get_user_model()


class AirportField(serializers.CharField):
    """Поле для сериализатора.
       Проверяет что все города сейчас доступны."""

    def to_representation(self, value: str) -> str:
        return value

    def to_internal_value(self, data: str) -> str | None:
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


class UserSerializer(DjUserCreateSerializer):
    """Унаследовано от Djoser, добавлены поля."""
    class Meta:
        model = User
        fields = ('email', 'password')
        write_only_fields = ('password',)

    def save(self, **kwargs) -> User:
        username = self.validated_data.get('email')
        kwargs['username'] = username
        return super().save(**kwargs)


class ActivityListSerializer(serializers.ModelSerializer):
    """Сериализатор списочного представления активностей."""

    class Meta:
        model = Activity
        fields = ('id', 'name', 'category', 'address', 'date',
                  'time', 'price', 'media', 'origin', 'destination')

    def to_representation(self, instance: Activity) -> dict:
        answer = (
            super(ActivityListSerializer, self).to_representation(instance))
        if instance.category != 'flight':
            answer.pop('origin')
            answer.pop('destination')
        else:
            answer.pop('address')
        return answer


class TravelSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для путешествий."""

    class Meta:
        model = Travel
        fields = ('id', 'name', 'description', 'start_date', 'end_date')

    def validate(self, data: dict) -> dict | None:
        start_date, end_date = data.get('start_date'), data.get('end_date')
        if start_date is None and end_date is None:
            return data
        if None not in (start_date, end_date):
            travel_dates_validator(start_date, end_date)
            return data
        msg = ('Укажите дату начала путешествия!' if start_date is None else
               'Укажите дату окончания путешествия!')
        raise serializers.ValidationError(msg)


class TravelPostSerializer(TravelSerializer):
    """Сериализатор для создания путешествия."""
    images = serializers.ListField(
        child=Base64ImageField(), allow_empty=True, write_only=True)

    class Meta(TravelSerializer.Meta):
        fields = TravelSerializer.Meta.fields + ('images',)

    def create(self, validated_data):
        images = validated_data.pop('images')
        travel = Travel.objects.create(**validated_data)
        Image.objects.bulk_create(
            Image(image=image, travel=travel) for image in images
        )
        return travel


class TravelListSerializer(TravelSerializer):
    """Сериализатор для вывода списка путешествий с активностями."""

    activities = ActivityListSerializer(many=True)
    total_price = serializers.FloatField()
    images = serializers.SerializerMethodField()

    @extend_schema_field(list[str])
    def get_images(self, object):
        return [str(image.image) for image in object.images.all()]

    class Meta(TravelSerializer.Meta):
        fields = TravelSerializer.Meta.fields + ('images',
                                                 'activities',
                                                 'total_price')


class ActivitySerializer(serializers.ModelSerializer):
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
                  'media',
                  'address',
                  'origin',
                  'destination')

    def validate(self, data: dict) -> dict | None:
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
        if data['category'] == 'flight':
            if 'origin' not in data or 'destination' not in data:
                raise serializers.ValidationError(
                    'Необходимо указать место отправления и назначения'
                )
        if data['category'] != 'flight':
            if 'address' not in data:
                raise serializers.ValidationError(
                    'Необходимо указать адрес.'
                )
        return data
