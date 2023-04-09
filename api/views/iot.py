import json

from django.http import JsonResponse

from api.models.iot import IotCommand
from api.serializers import IotCommandSerializer


def get_iot_commands(request):
    commands = IotCommand.objects.all()
    commands_serialized = [IotCommandSerializer(command).data for command in commands]
    return JsonResponse(data=commands_serialized, safe=False)
