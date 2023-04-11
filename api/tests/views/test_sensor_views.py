from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models.sensor import Sensor
from api.tests.helpers import reverse


def _create_test_sensor() -> Sensor:
    return Sensor.objects.create(id='test-sensor')


class TestSensorViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_sensor_registration(self):
        url = reverse('sensor-list-create')

        # register a sensor via id, expect 201 CREATED
        response = self.client.post(url, {'id': 'hallway-led-esp8266'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sensor_command_registration_and_list_and_ack(self):
        test_sensor = _create_test_sensor()

        url = reverse('sensor-commands-list-create', args=(test_sensor.id,))
        # enqueue a command via sensor id, expect 201 CREATED
        response = self.client.post(url, {'command': 'set-led-5-green'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # lookup pending commands, there should be at least one
        url = reverse('sensor-commands-list-create', args=(test_sensor.id,))
        response = self.client.get(url)
        self.assertEqual(response.json()['count'], 1)

        # acking a command
        sensor_command = response.json()['results'][0]
        sensor_command['acked'] = True
        url = reverse('sensor-commands-update', args=(test_sensor.id, sensor_command['id']))
        response = self.client.put(url, sensor_command)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # acked commands shouldn't appear in list
        url = reverse('sensor-commands-list-create', args=(test_sensor.id,))
        response = self.client.get(url)
        self.assertEqual(response.json()['count'], 0)
