from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

FAQ_CACHE_KEY = 'faq'
MAX_SIZE = 500


class FAQ(models.Model):
    question = models.CharField(max_length=MAX_SIZE, unique=True)
    answer = models.TextField()

    class Meta:
        ordering = ('question',)

    def __str__(self):
        return f'{self.question}: {self.answer[:MAX_SIZE]}'


@receiver([post_save, post_delete], sender=FAQ)
def clear_cache(**kwargs):
    cache.delete(FAQ_CACHE_KEY)
