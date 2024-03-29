# Generated by Django 4.2.1 on 2023-07-19 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Укажите IATA-код города', max_length=3, unique=True, verbose_name='IATA-код города')),
                ('name', models.CharField(db_index=True, help_text='Укажите наименование города', max_length=100, verbose_name='Наименование города')),
                ('latitude', models.FloatField(help_text='Укажите координату широты города', verbose_name='Координата широты города')),
                ('longitude', models.FloatField(help_text='Укажите координату долготы города', verbose_name='Координата долготы города')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('name',),
            },
        ),
    ]
