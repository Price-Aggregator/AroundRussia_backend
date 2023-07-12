# Generated by Django 4.2.1 on 2023-07-11 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('travel_diary', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='traveller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travels', to=settings.AUTH_USER_MODEL, verbose_name='Путешественник'),
        ),
        migrations.AddField(
            model_name='activity',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel', to='travel_diary.travel'),
        ),
    ]
