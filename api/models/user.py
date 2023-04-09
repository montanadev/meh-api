from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class LEDProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    red = models.PositiveIntegerField(default=0)
    green = models.PositiveIntegerField(default=0)
    blue = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


