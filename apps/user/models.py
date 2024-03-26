from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class UserType(models.TextChoices):
        COMPANY_OWNER = 'CO', _('Company Owner')
        FEEDING_TEAM = 'FT', _('Feeding Team')
        BARCODE_TEAM = 'BT', _('Barcode Team')

    user_type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.BARCODE_TEAM,
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name+ ' ' + self.last_name
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return ''

    objects = CustomUserManager()
