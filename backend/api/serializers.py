from datetime import datetime

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjUserCreateSerializer
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from tickets.models import City
from travel_diary.models import Activity, Image, Media, Travel

from .constants import CATEGORIES
from .fields import AirportField, Base64FileField, Base64ImageField
from .validators import travel_dates_validator

User = get_user_model()


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


class ActivitySerializer(serializers.ModelSerializer):
    """Базовый сериализатор для карточек."""
    travel = serializers.IntegerField(source='travel_id', write_only=True)

    class Meta:
        model = Activity
        fields = ('id',
                  'travel',
                  'name',
                  'category',
                  'date',
                  'time',
                  'price',
                  'description',
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


class ActivityMediaSerializer(serializers.Serializer):
    media = Base64FileField()

    def to_representation(self, instance):
        return super().to_representation(instance).get('media')


class ActivityListSerializer(ActivitySerializer):
    """Сериализатор списочного представления активностей."""
    medias = serializers.SerializerMethodField()

    @extend_schema_field(list[str])
    def get_medias(self, obj):
        request = self.context.get('request')
        return ActivityMediaSerializer(obj.medias,
                                       many=True,
                                       context={'request': request}).data

    class Meta(ActivitySerializer.Meta):
        fields = ActivitySerializer.Meta.fields + ('medias',)

    def to_representation(self, instance: Activity) -> dict:
        answer = (
            super(ActivityListSerializer, self).to_representation(instance))
        if instance.category != 'flight':
            answer.pop('origin')
            answer.pop('destination')
        else:
            answer.pop('address')
        return answer


class ActivityPostSerializer(ActivitySerializer):
    """Сериализатор для создания активности."""
    medias = serializers.ListField(
        child=Base64FileField(use_url=True),
        allow_empty=True, write_only=True
    )

    class Meta(ActivitySerializer.Meta):
        fields = ActivitySerializer.Meta.fields + ('medias',)

    def add_medias(self, medias, activity):
        Media.objects.bulk_create(
            [Media(
                media=media,
                activity=activity
            ) for media in medias]
        )

    def create(self, validated_data):
        medias = validated_data.pop('medias', None)
        activity = Activity.objects.create(**validated_data)
        if medias:
            self.add_medias(medias, activity)
        return activity

    def update(self, instance, validated_data):
        medias = validated_data.pop('medias', None)
        if medias:
            Media.objects.filter(activity_id=instance.id).delete()
            self.add_medias(medias, instance)
        return super().update(instance, validated_data)


class TravelSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для путешествий."""
    images = serializers.ListField(child=Base64ImageField(), write_only=True)

    class Meta:
        model = Travel
        fields = (
            'id', 'name', 'description', 'start_date', 'end_date', 'images')

    def _add_images(self, travel: Travel, images: list[str] | None) -> None:
        if images is not None:
            Image.objects.bulk_create(Image(image=image, travel=travel)
                                      for image in images)

    def create(self, validated_data):
        images = validated_data.pop('images')
        travel = Travel.objects.create(**validated_data)
        self._add_images(travel, images)
        return travel

    def update(self, instance: Travel, validated_data: dict):
        try:
            images = validated_data.pop('images')
            instance.images.all().delete()
            self._add_images(instance, images)
        except KeyError:
            pass

        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        if start_date is None and end_date is None:
            return super().update(instance, validated_data)
        if start_date is None:
            start_date = instance.start_date
        if end_date is None:
            end_date = instance.end_date
        travel_dates_validator(start_date, end_date)
        return super().update(instance, validated_data)


class TravelListSerializer(TravelSerializer):
    """Сериализатор для вывода списка путешествий с активностями."""

    activities = ActivityListSerializer(many=True)
    total_price = serializers.FloatField()
    images = serializers.SerializerMethodField()

    @extend_schema_field(list[str])
    def get_images(self, object):
        return [str(image.image) for image in object.images.all()]

    class Meta(TravelSerializer.Meta):
        fields = TravelSerializer.Meta.fields + ('activities', 'total_price')
