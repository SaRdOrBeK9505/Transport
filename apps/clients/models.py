from django.db import models
from apps.common.models import TimeStampedModel, OrderableModel


class PartnerClient(TimeStampedModel, OrderableModel):
    name = models.CharField(max_length=150, verbose_name='Kompaniya nomi')
    logo = models.ImageField(upload_to='clients/', verbose_name='Logotip')
    website = models.URLField(blank=True, verbose_name='Veb-sayt')
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta(OrderableModel.Meta):
        verbose_name = 'Hamkor'
        verbose_name_plural = 'Hamkorlar'

    def __str__(self):
        return self.name
