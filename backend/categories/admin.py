from django.contrib import admin

from .models import (Activity, Flight, Travel, TravelActivity,
                     TravelFlight)


EMPTY_DISPLAY = '-пусто-'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'start_time',
                    'address', 'phone', 'website', 'email', 'price')
    search_fields = ('name', 'start_date')
    list_filter = ('name', 'start_date')
    empty_value_display = EMPTY_DISPLAY


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('departure_date', 'departure_time', 'airline',
                    'flight_number', 'seats', 'price')
    search_fields = ('departure_date', 'departure_time')
    list_filter = ('departure_date', 'departure_time')
    empty_value_display = EMPTY_DISPLAY


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author')
    empty_value_display = EMPTY_DISPLAY


@admin.register(TravelActivity)
class TravelActivityAdmin(admin.ModelAdmin):
    list_display = ('travel', 'activity')
    search_fields = ('travel', 'activity')
    list_filter = ('travel', 'activity')
    empty_value_display = EMPTY_DISPLAY


@admin.register(TravelFlight)
class TravelFlightAdmin(admin.ModelAdmin):
    list_display = ('travel', 'flight')
    search_fields = ('travel', 'flight')
    list_filter = ('travel', 'flight')
    empty_value_display = EMPTY_DISPLAY
