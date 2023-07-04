# Generated by Django 4.2.1 on 2023-07-04 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите название', max_length=50, verbose_name='Название события')),
                ('description', models.TextField(help_text='Укажите описание', verbose_name='Описание')),
                ('start_date', models.DateField(help_text='Укажите дату начала', verbose_name='Дата начала')),
                ('start_time', models.TimeField(help_text='Укажите время начала', verbose_name='Время начала')),
                ('address', models.CharField(help_text='Укажите адрес', verbose_name='Адрес')),
                ('phone', models.CharField(help_text='Укажите телефон', max_length=20, verbose_name='Телефон')),
                ('website', models.CharField(help_text='Укажите сайт', verbose_name='Сайт')),
                ('email', models.EmailField(help_text='Укажите почту', max_length=254, verbose_name='Электронная почта')),
                ('price', models.CharField(help_text='Укажите цену', verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Активность',
                'verbose_name_plural': 'Активности',
                'ordering': ['-start_date', '-start_time'],
            },
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Назовите свое путешествие', max_length=50, verbose_name='Имя путешествия')),
            ],
            options={
                'verbose_name': 'Путешествие',
                'verbose_name_plural': 'Путешествия',
            },
        ),
        migrations.CreateModel(
            name='TravelActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='categories.activity')),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel', to='categories.travel')),
            ],
            options={
                'verbose_name': 'Активность в путешествии',
                'verbose_name_plural': 'Активности в путешествии',
            },
        ),
        migrations.AddField(
            model_name='travel',
            name='activities',
            field=models.ManyToManyField(through='categories.TravelActivity', to='categories.activity', verbose_name='Активности'),
        ),
        migrations.AddField(
            model_name='travel',
            name='author',
            field=models.ForeignKey(help_text='Укажите автора', on_delete=django.db.models.deletion.CASCADE, related_name='travel', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddConstraint(
            model_name='travelactivity',
            constraint=models.UniqueConstraint(fields=('travel', 'activity'), name='unique_activity'),
        ),
    ]
