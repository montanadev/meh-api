from django.db import models

from api.models.base import BaseModel


class Sensor(BaseModel):
    id = models.TextField(primary_key=True)
    last_heartbeat = models.DateTimeField(auto_now_add=True)


class SensorCommand(BaseModel):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    command = models.TextField()
    acked = models.BooleanField()
