# Generated by Django 4.2.1 on 2023-09-14 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='latitude',
            field=models.DecimalField(decimal_places=6, help_text='Укажите координату широты города', max_digits=10, verbose_name='Координата широты города'),
        ),
        migrations.AlterField(
            model_name='city',
            name='longitude',
            field=models.DecimalField(decimal_places=6, help_text='Укажите координату долготы города', max_digits=10, verbose_name='Координата долготы города'),
        ),
    ]
