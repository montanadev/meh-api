import json

from django.http import JsonResponse

from api.models.iot import IotCommand


def get_iot_commands(request):
    commands = IotCommand.objects.all()
    return JsonResponse(data=json.dumps(commands), safe=False)
