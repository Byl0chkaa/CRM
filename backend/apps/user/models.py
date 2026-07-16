from core.models import BaseModel
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from apps.user.managers import UserManager


class UserRole(models.TextChoices):
    ADMIN = 'admin'
    MANAGER = 'manager'

class UserModel(AbstractUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ['-id']

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=7, choices=UserRole.choices)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=16)

    objects = UserManager()


