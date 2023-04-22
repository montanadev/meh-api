import logging
import time

import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")

        client = mqtt.Client()
        client.on_connect = on_connect
        # might change to 192.168.1.250
        client.connect("192.168.2.5", 1883, 60)
        for i in range(3):
            client.publish('a/b', payload=i, qos=0, retain=False)
            print(f"send {i} to a/b")
            time.sleep(1)

        client.loop_forever()
