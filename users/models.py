from django.contrib.auth.models import AbstractUser
from django.db import models
from locations.models import City

class User(AbstractUser):
    """Base User model"""
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True
    )
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_user'


class Client(User):
    """User model for clients"""
    birth_date = models.DateField()

    class Meta:
        db_table = 'users_client'


class Provider(User):
    """User model for providers"""
    name = models.CharField(max_length=100, default="")
    identifier_number = models.IntegerField(unique=True, default=0)
    description = models.TextField()
    phone_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'users_provider'
