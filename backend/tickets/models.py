from django.db import models


class City(models.Model):
    COORD_MAX_DIGITS = 10
    COORD_DECIMAL_PLACES = 6

    code = models.CharField(
        'IATA-код города',
        max_length=3,
        unique=True,
        help_text='Укажите IATA-код города'
    )
    name = models.CharField(
        'Наименование города',
        max_length=100,
        db_index=True,
        help_text='Укажите наименование города'
    )
    latitude = models.DecimalField(
        'Координата широты города',
        help_text='Укажите координату широты города',
        max_digits=COORD_MAX_DIGITS,
        decimal_places=COORD_DECIMAL_PLACES,
    )
    longitude = models.DecimalField(
        'Координата долготы города',
        help_text='Укажите координату долготы города',
        max_digits=COORD_MAX_DIGITS,
        decimal_places=COORD_DECIMAL_PLACES,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name
