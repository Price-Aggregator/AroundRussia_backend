from django.contrib import admin

from .models import Activity, Travel, TravelActivity


EMPTY_DISPLAY = '-пусто-'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'start_time',
                    'address', 'phone', 'website', 'email', 'price')
    search_fields = ('name', 'start_date')
    list_filter = ('name', 'start_date')
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
