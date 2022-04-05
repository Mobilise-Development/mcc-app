from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db import models


class MCCUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    date_updated = models.DateField(auto_now=True)
    date_deleted = models.DateField(default=None, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
