from django.contrib.auth import get_user_model
from django.db import models

from api.validators import validate_file_extension

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


class Activity(models.Model):
    """Модель активностей."""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author')
    travel = models.ForeignKey(Travel,
                               on_delete=models.CASCADE,
                               related_name='travel')
    name = models.CharField(verbose_name='Название события',
                            help_text='Введите название',
                            max_length=255,)
    category = models.CharField(verbose_name='Категория события',
                                help_text='Выберите категорию',
                                max_length=50)
    address = models.CharField(verbose_name='Адрес',
                               help_text='Укажите адрес',
                               max_length=255,
                               null=True)
    date = models.DateField(verbose_name='Дата',
                            help_text='Введите дату',
                            db_index=True)
    time = models.TimeField(verbose_name='Время',
                            help_text='Введите время',
                            db_index=True)
    description = models.CharField(verbose_name='Описание',
                                   help_text='Введите описание',
                                   max_length=255,
                                   null=True,
                                   blank=True)
    price = models.IntegerField(verbose_name='Цена',
                                help_text='Введите цену',
                                null=True,
                                blank=True)
    media = models.FileField(upload_to='files/',
                             verbose_name='Файл',
                             help_text='Загрузите файл',
                             validators=[validate_file_extension],
                             null=True,
                             blank=True)
    origin = models.CharField(verbose_name='Откуда',
                              help_text='Введите пункт отправления',
                              max_length=50,
                              null=True)
    destination = models.CharField(verbose_name='Куда',
                                   help_text='Введите пункт назначения',
                                   max_length=50,
                                   null=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Карточка активностей'
        verbose_name_plural = 'Карточки активностей'

    def __str__(self):
        return self.name
