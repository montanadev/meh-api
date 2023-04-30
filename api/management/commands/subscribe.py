import logging
import time

import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # The callback function of connection
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")
            client.subscribe("test_sensor")

        # The callback function for received message
        def on_message(client, userdata, msg):
            print(msg.topic + " " + str(msg.payload))

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("192.168.0.254", 1883, 60)
        client.loop_forever()
