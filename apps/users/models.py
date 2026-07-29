from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_DISPATCHER = 'dispatcher'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_DISPATCHER, 'Dispatcher'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_DISPATCHER,
        verbose_name='Rol'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_dispatcher(self):
        return self.role == self.ROLE_DISPATCHER
