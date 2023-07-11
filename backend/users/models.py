from django.contrib.auth.models import AbstractUser
from django.db import models

SEX_CHOICES = (
    ('М', 'Мужской'),
    ('Ж', 'Женский')
)


class User(AbstractUser):
    email = models.EmailField('Электронная почта', unique=True)
    sex = models.CharField('Пол', max_length=1, choices=SEX_CHOICES,
                           blank=True, null=True)
    phone_number = models.IntegerField('Телефонный номер', blank=True,
                                       null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
