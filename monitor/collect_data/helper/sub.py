'''
This is just a test subscriber, to read the published data from the mqtt-broker
'''
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    topic = "sensor/temperature"
    client.subscribe(topic)
    topic = "sensor/humidity"
    client.subscribe(topic)


def on_message(client, userdata, msg):
    print(msg.topic + ":" + msg.payload.decode())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("nextcloud-mac.local", 1883, 60)

client.loop_forever()
