from django.db import models


class IotCommand(models.Model):
    acked = models.BooleanField()
    sensor = models.TextField()
