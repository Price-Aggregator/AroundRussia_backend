from django.db import models


class City(models.Model):
    code = models.CharField(
        'IATA-код города',
        max_length=3,
        unique=True,
        help_text='Укажите IATA-код города'
    )
    name = models.CharField(
        'Наименование города',
        max_length=100,
        help_text='Укажите наименование города'
    )
    latitude = models.FloatField(
        'Координата широты города',
        help_text='Укажите координату широты города'
    )
    longitude = models.FloatField(
        'Координата долготы города',
        help_text='Укажите координату долготы города'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name
