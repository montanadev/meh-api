from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from api.models.iot import IotCommand
from api.serializers import IotCommandSerializer


@permission_classes([AllowAny])
def get_iot_commands(request):
    commands = IotCommand.objects.all()
    commands_serialized = [IotCommandSerializer(command).data for command in commands]
    return JsonResponse(data=commands_serialized, safe=False)


@permission_classes([AllowAny])
def ack_iot_command(request, id):
    iot_command: IotCommand = get_object_or_404(IotCommand, id=id)
    iot_command.acked = True
    iot_command.save()
    return JsonResponse(data=IotCommand(iot_command).data)
