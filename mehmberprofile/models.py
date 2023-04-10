from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opt_out_all = models.BooleanField(default=False)
    opt_out_led_wall = models.BooleanField(default=False)
    opt_out_door_display = models.BooleanField(default=False)
    opt_out_social_bot = models.BooleanField(default=False)
    opt_out_accolade_display = models.BooleanField(default=False)
    rgb_value = models.CharField(max_length=7, default="#000000")
    led_number = models.IntegerField(verbose_name="LED Number", blank=True, null=True,
                                     validators=[MaxValueValidator(200), MinValueValidator(0)])

    def __str__(self):
        return f"{self.user.username}'s profile"


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255, default="Mehmbership")

    def __str__(self):
        return f"{self.user.username}'s payment on {self.date}"


class MembershipHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_price = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(0)], default=30)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, default="Mehmbership")

    def __str__(self):
        return f"{self.user.username}'s mehmbership starting {self.start_date}"
