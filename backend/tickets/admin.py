from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import City


class CityAdmin(ModelAdmin):
    list_display = ('name', 'code', 'latitude', 'longitude')
    list_display_links = ('name', 'code')
    search_fields = ('name', 'code')


admin.site.register(City)
