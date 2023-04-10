from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opt_out_all = models.BooleanField(default=False)
    opt_out_led_wall = models.BooleanField(default=False)
    opt_out_door_display = models.BooleanField(default=False)
    opt_out_social_bot = models.BooleanField(default=False)
    opt_out_accolade_display = models.BooleanField(default=False)
    rgb_value = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return f"{self.user.username}'s profile"


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, default="Mehmbership")

    def __str__(self):
        return f"{self.user.username}'s payment on {self.date}"