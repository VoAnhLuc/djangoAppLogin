from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

class Users(AbstractUser):
    username = None
    email = models.EmailField(max_length=50, unique=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    facebook = models.CharField(max_length=500, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def get_info(self):
        data = {
            'email': self.email,
            'date_joined': self.date_joined,
        }
        return data