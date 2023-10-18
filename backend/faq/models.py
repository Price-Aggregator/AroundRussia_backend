from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
# noqa: I004, I001
from api.constants import FAQ_CACHE_KEY, FAQ_LENGTH  # noqa: I001


class FAQ(models.Model):
    question = models.CharField(max_length=FAQ_LENGTH, unique=True)
    answer = models.TextField()

    class Meta:
        ordering = ('question',)

    def __str__(self):
        return f'{self.question}: {self.answer[:FAQ_LENGTH]}'


@receiver([post_save, post_delete], sender=FAQ)
def clear_cache(**kwargs):
    cache.delete(FAQ_CACHE_KEY)
