#!/usr/bin/python3

from w1thermsensor import W1ThermSensor
import time
import paho.mqtt.client as mqtt

outside = W1ThermSensor(sensor_id='00000b2aa601')
bottom_plate = W1ThermSensor(sensor_id='00000b2a90e2')
inside =W1ThermSensor(sensor_id='00000b2ab1d5')

BROKER_ADDRESS = "192.168.1.2"
topic_bottom = 'brewie/temp/bottom'
topic_inside = 'brewie/temp/inside'
topic_outside = 'brewie/temp/outside'

client = mqtt.Client('brewie')
print("Connecting to broker")
client.connect(host=BROKER_ADDRESS)
client.loop_start()

while True:
    try:
        client.publish(topic_bottom, payload=bottom_plate.get_temperature())
        print('Bottom plate: {}'.format(bottom_plate.get_temperature()))
    except:
        print("Failure in {}".format(topic_bottom))
    try:
        client.publish(topic_inside, payload=inside.get_temperature())
        print('Inside case: {}'.format(inside.get_temperature()))
    except:
        print("Failure in {}".format(topic_inside))
    try:
        client.publish(topic_outside, payload=outside.get_temperature())
        print('Waterm Temp: {}'.format(outside.get_temperature()))
    except:
        print("Failure in {}".format(topic_outside))
    print('........................')
    time.sleep(5)
