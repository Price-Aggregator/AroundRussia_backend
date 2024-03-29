# Generated by Django 4.2.1 on 2023-07-25 10:54

import api.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_diary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='media',
        ),
        migrations.AlterField(
            model_name='activity',
            name='price',
            field=models.IntegerField(blank=True, help_text='Введите цену', null=True, verbose_name='Цена'),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(help_text='Загрузите файл', upload_to='files/', validators=[api.validators.validate_file_extension], verbose_name='Файл')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='travel_diary.activity', verbose_name='Активность')),
            ],
            options={
                'verbose_name': 'Медиа файл',
                'verbose_name_plural': 'Медиа файлы',
                'ordering': ('activity',),
            },
        ),
    ]
