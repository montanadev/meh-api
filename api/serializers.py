from rest_framework import serializers

from api.models.iot import IotCommand


class IotCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = IotCommand
        fields = "__all__"
