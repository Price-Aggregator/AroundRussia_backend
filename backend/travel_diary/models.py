from django.db import models


class Activity(models.Model):
    """Модель активностей."""
    name = models.CharField(verbose_name='Название события',
                            help_text='Введите название',
                            max_length=255,)
    category = models.CharField(verbose_name='Категория события',
                                help_text='Выберите категорию')
    address = models.CharField(verbose_name='Адрес',
                               help_text='Укажите адрес',
                               max_length=255,
                               blank=True)
    date = models.DateField(verbose_name='Дата',
                            help_text='Введите дату',
                            db_index=True)
    time = models.TimeField(verbose_name='Время',
                            help_text='Введите время',
                            db_index=True)
    description = models.TextField(verbose_name='Описание',
                                   help_text='Введите описание',
                                   blank=True)
    price = models.IntegerField(verbose_name='Цена',
                                help_text='Введите цену',
                                blank=True)
    media = models.FileField(upload_to='files/',
                             verbose_name='Файл',
                             help_text='Загрузите файл',
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
