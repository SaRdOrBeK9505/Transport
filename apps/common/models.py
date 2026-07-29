from django.db import models


class TimeStampedModel(models.Model):
    """
    Barcha modellarga created_at va updated_at qo'shuvchi abstract base model.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderableModel(models.Model):
    """
    order maydoni orqali tartiblanadigan abstract model.
    """
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ['order']
