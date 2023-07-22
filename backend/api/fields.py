import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .constants import MEDIA_FORMATS


class Base64ImageField(serializers.ImageField):
    """Кастомный тип поля для декодирования медиафайлов."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format_file, image_str = data.split(';base64,')
            extension = format_file.split('/')[-1]
            if extension not in MEDIA_FORMATS:
                raise serializers.ValidationError(
                    'Не поддерживаемый медиа-формат! '
                    'Разрешены следующие форматы: jpg, jpeg, png, svg.'
                )
            return ContentFile(
                base64.b64decode(image_str), name='temp.' + extension
            )