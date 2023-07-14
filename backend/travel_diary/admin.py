from django.contrib import admin

from .models import Activity, Travel


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    """Модель путешествий в Админке."""
    list_display = ('name', 'start_date', 'end_date')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Activity)
