from django.db import models

from api.models.base import BaseModel


class Sensor(models.Model, BaseModel):
    id = models.TextField(primary_key=True)
    last_heartbeat = models.DateTimeField(auto_now_add=True)


class SensorCommand(models.Model, BaseModel):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    command = models.TextField()
    acked = models.BooleanField()
