from django.contrib import admin
# noqa: I004
from travel_diary.models import Travel


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    """Модель путешествий в Админке."""
    list_display = ('name', 'start_date', 'end_date')
    list_display_links = ('name',)
    search_fields = ('name',)
