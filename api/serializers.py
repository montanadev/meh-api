from rest_framework import serializers

from api.models.sensor import Sensor, SensorCommand


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        read_only_fields = ('last_heartbeat',)
        fields = "__all__"


class SensorCommandSerializer(serializers.ModelSerializer):
    acked = serializers.BooleanField(default=False)

    class Meta:
        model = SensorCommand
        fields = "__all__"
