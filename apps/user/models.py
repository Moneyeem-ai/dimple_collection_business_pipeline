from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
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
