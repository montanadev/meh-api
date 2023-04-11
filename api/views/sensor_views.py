from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateAPIView

from api.models.sensor import Sensor, SensorCommand
from api.serializers import SensorSerializer, SensorCommandSerializer


class SensorListView(ListCreateAPIView):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()


class SensorCommandsListView(ListCreateAPIView):
    serializer_class = SensorCommandSerializer

    def get_queryset(self):
        # returns unacked commands in FIFO w.r.t the corresponding sensor
        return SensorCommand.objects.filter(sensor=self.kwargs['sensor_id']).filter(acked=False).order_by('created_at')

    def get_serializer(self, *args, **kwargs):
        sensor = get_object_or_404(Sensor, id=self.kwargs['sensor_id'])

        if self.request.method == "POST":
            # hydrate the sensor object from the URL parameter
            kwargs = {'data': {**kwargs['data'].dict(), 'sensor': sensor.id}}

        # fetching commands moves the heartbeat forward
        sensor.last_heartbeat = timezone.now()
        sensor.save()

        return super().get_serializer(*args, **kwargs)


class SensorCommandUpdateView(RetrieveUpdateAPIView):
    serializer_class = SensorCommandSerializer

    def get_queryset(self):
        return SensorCommand.objects.filter(sensor=self.kwargs['sensor_id'])
