from django.db import models

class LED(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    red = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)
    green = models.IntegerField(default=0)