from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


def find_lowest_available_LED_light():
    return 1


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opt_out_all = models.BooleanField(default=False)
    opt_out_led_wall = models.BooleanField(default=False)
    opt_out_door_display = models.BooleanField(default=False)
    opt_out_social_bot = models.BooleanField(default=False)
    opt_out_accolade_display = models.BooleanField(default=False)
    red_value = models.CharField(max_length=7, default="0")
    green_value = models.CharField(max_length=7, default="0")
    blue_value = models.CharField(max_length=7, default="0")
    led_number = models.IntegerField(verbose_name="LED Number", blank=True, null=True,
                                     default=find_lowest_available_LED_light(),
                                     validators=[MaxValueValidator(200), MinValueValidator(0)])

    def __str__(self):
        return f"{self.user.username}'s profile"


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(default=timezone.now)

    description = models.CharField(max_length=255, default="Mehmbership")

    class Meta:
        verbose_name_plural = "Payment Histories"

    def __str__(self):
        return f"{self.user.username}'s payment on {self.date}"


class MehmbershipHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_price = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(0)], default=30)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, default="Mehmbership")

    class Meta:
        verbose_name_plural = "Mehmbership Histories"

    def __str__(self):
        return f"{self.user.username}'s mehmbership starting {self.start_date}"
