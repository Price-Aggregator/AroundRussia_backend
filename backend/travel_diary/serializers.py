from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """Сериализатор для вывода активностей."""
    class Meta:
        model = Activity
        fields = '__all__'
