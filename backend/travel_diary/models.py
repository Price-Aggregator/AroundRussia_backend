from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Travel(models.Model):
    name = models.CharField(
        'Наименование путешествия',
        max_length=200,
        unique=True,
        help_text='Укажите наименование путешествия'
    )
    start_date = models.DateField(
        'Дата начала путешествия',
        help_text='Укажите дату начала путешествия'
    )
    end_date = models.DateField(
        'Дата окончания путешествия',
        help_text='Укажите дату окончания путешествия'
    )
    image = models.ImageField(
        upload_to='travel_diary/images/',
        null=True,
        default=None
    )
    traveler = models.ForeignKey(
        User,
        verbose_name='Путешественник',
        on_delete=models.CASCADE,
        related_name='travels'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'

    def __str__(self):
        return self.name
