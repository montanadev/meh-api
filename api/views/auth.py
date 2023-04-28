from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from api.models.iot import IotCommand
from api.serializers import IotCommandSerializer


@permission_classes([AllowAny])
def create_authentication_request(request):
    return JsonResponse(data={})
