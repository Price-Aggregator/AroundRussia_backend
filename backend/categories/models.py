from django.db import models
from users.models import User


class Activity(models.Model):
    """Модель активностей."""

    name = models.CharField(verbose_name='Название события',
                            help_text='Укажите название',
                            max_length=50)
    description = models.TextField(verbose_name='Описание',
                                   help_text='Укажите описание')
    start_date = models.DateField(verbose_name='Дата начала',
                                  help_text='Укажите дату начала')
    start_time = models.TimeField(verbose_name='Время начала',
                                  help_text='Укажите время начала')
    address = models.CharField(verbose_name='Адрес',
                               help_text='Укажите адрес')
    phone = models.CharField(verbose_name='Телефон',
                             help_text='Укажите телефон',
                             max_length=20)
    website = models.CharField(verbose_name='Сайт',
                               help_text='Укажите сайт')
    email = models.EmailField(verbose_name='Электронная почта',
                              help_text='Укажите почту')
    price = models.CharField(verbose_name='Цена',
                             help_text='Укажите цену')

    class Meta:
        """Meta модели Activity."""

        ordering = ['-start_date', '-start_time']
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'

    def __str__(self) -> str:
        """Функция __str__ модели Activity."""
        return self.name


class Travel(models.Model):
    """Модель путешествий."""

    name = models.CharField(verbose_name='Имя путешествия',
                            help_text='Назовите свое путешествие',
                            max_length=50)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='travel',
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    activity = models.ManyToManyField()

    class Meta:
        """Meta модели Travel."""

        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'

    def __str__(self) -> str:
        """Функция __str__ модели Activity."""
        return self.name


class TravelActivity(models.Model):
    """Модель для связи моделей Travel Activity."""

    travel = models.ForeignKey(Travel,
                               on_delete=models.CASCADE,
                               related_name='travel')
    activity = models.ForeignKey(Activity,
                                 on_delete=models.CASCADE,
                                 related_name='activity')

    class Meta:
        """Meta модели TravelActivity."""

        verbose_name = 'Активность в путешествии'
        verbose_name_plural = 'Активности в путешествии'
        constraints = [models.UniqueConstraint(
            fields=['travel', 'activity'],
            name='unique_activity'
        )]

    def __str__(self) -> str:
        """Функция __str__ модели TravelActivity."""
        return (f'Активность {self.activity.name}'
                f'в путешествии {self.travel.name}')
