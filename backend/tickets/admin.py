from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'latitude', 'longitude')
    list_display_links = ('name', 'code')
    search_fields = ('name', 'code')
