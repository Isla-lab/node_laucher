from paho.mqtt import client as mqtt_client
import uuid
import typing


class MqttClient():
    def __init__(self, callback=None):
        self._client = mqtt_client.Client(uuid.uuid4().hex)
        self.broker = "127.0.0.1"
        self.port = 1883
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.connect(self.broker, self.port)
        self._client.loop_start()
        #self._client.loop_forever()
        self._running = True
        self.callback = callback

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected\n")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        if self.callback is not None:
            self.callback(msg.topic, msg.payload.decode())

    def publish(self, topic, payload):
        self._client.publish(topic, payload)

    def subscribe(self, topic):
        self._client.subscribe(topic)

    def stop(self):
        if self._running:
            self._running = False
            self._client.loop_stop()
            self._client = None