# Generated by Django 4.2.1 on 2023-07-19 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel_diary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='traveler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travels', to=settings.AUTH_USER_MODEL, verbose_name='Путешественник'),
        ),
        migrations.AddField(
            model_name='image',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='travel_diary.travel', verbose_name='Путешествие'),
        ),
        migrations.AddField(
            model_name='activity',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='travel_diary.travel'),
        ),
    ]
