import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .constants import BLOCK_CITY, FILE_FORMATS, MEDIA_FORMATS


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


class GenericBase64:
    """Кастомный тип поля для декодирования файлов.
       Производит валидацию и декодирование base64 строки."""
    def _to_internal_value(self, data, data_mime_prefix, file_formats, ):
        if not isinstance(data, str):
            raise serializers.ValidationError(
                f'Неверный тип данных {type(data)} для передачи файлов! '
                f'Ожидается type(str) ! '
            )
        if not data.startswith(data_mime_prefix):
            raise serializers.ValidationError(
                f'Неверный <MIME-type> — {data[:len(data_mime_prefix)]} ! '
                f'Ожидается {data_mime_prefix}'
            )
        format_file, data_str = data.split(';base64,')
        ext = format_file.split('/')[-1]
        if ext not in file_formats:
            raise serializers.ValidationError(
                f'Не поддерживаемый формат файла! '
                f'Разрешены следующие форматы: {file_formats}.'
            )
        return ContentFile(base64.b64decode(data_str), name='temp.' + ext)


class Base64ImageField(serializers.ImageField, GenericBase64):
    """Кастомный тип поля для декодирования медиафайлов."""
    def to_internal_value(self, data):
        return self._to_internal_value(data, 'data:image', MEDIA_FORMATS)


class Base64FileField(serializers.FileField):
    """Кастомный тип поля для декодирования медиафайлов."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:@file'):
            format_file, media_str = data.split(';base64,')
            extension = format_file.split('/')[-1]
            if extension not in FILE_FORMATS:
                raise serializers.ValidationError(
                    'Не поддерживаемый формат файла! '
                    'Разрешены следующие форматы: pdf.'
                )
            return ContentFile(
                base64.b64decode(media_str), name='temp.' + extension
            )
