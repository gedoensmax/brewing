#%% imports
import time
import yaml
import paho.mqtt.client as mqtt


#%% Initialize client
BROKER_ADDRESS = "localhost"
topic_temp = 'brewie/temp'
topic_relais = 'brewie/relais'

client = mqtt.Client('brewie')
print("Connecting to broker")
client.connect(host=BROKER_ADDRESS)
client.loop_start()
print('Subscribing to topics')
client.subscribe(topic=topic_temp)
client.subscribe(topic=topic_relais)



#%% PI exclusive
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO

relais_pin = 17
recipe_path ='recipes/923.yml'

GPIO.setmode(GPIO.BCM)
GPIO.setup(relais_pin, GPIO.OUT)
outside = W1ThermSensor(sensor_id='00000b2aa601')
inside = W1ThermSensor(sensor_id='00000b2a90e2')

#%% function definition
def heatup(temp, sensor=inside):
    '''

    :param temp: Target temperature
    '''
    if sensor.get_temperature() > temp:
        raise Exception('DAMN THATS HOT')
    while sensor.get_temperature() <= temp:
        GPIO.output(relais_pin, GPIO.HIGH)
        time.sleep(10000)
        print('.')
    GPIO.output(relais_pin, GPIO.LOW)
    print('The temperature is {}°C, heating has stopped'.format(sensor.get_temperature()))


def keep_temp(temp, time, sensor=temp_local):
    '''

    :param temp: Temperature to be kept
    :param time: in minutes
    :param sensor: temperature sensor(s)
    '''
    for i in range(time * 60):
        # Running in 1sec intervall
        if sensor.get_temperature() < (temp - 1):
            GPIO.output(relais_pin, GPIO.HIGH)
        else:
            GPIO.output(relais_pin, GPIO.LOW)

        if not i % 10:
            # Print every 10 seconds the temperature
            print('Time remaining: {:0}{:2}min, Temperature: {}°C'.format(i / 60, i % 60, sensor.get_temperature()))

        time.sleep(1000)

    GPIO.output(relais_pin, GPIO.LOW)
    print('Time is over')


#%%
recipe_path ='recipes/923.yml'
with open(recipe_path) as f:
    recipe = yaml.load(f, Loader=yaml.FullLoader)

def malt_process(recipe):
    for step in recipe['malt-process']:
        heatup(step['degree'])
        if 'malt' in step:
            '''
            Implement a way to wait for adding the malts before continuing
            '''
        keep_temp(step['degree'], step['time'])


def hop_process(recipe):
    GPIO.output(relais_pin, GPIO.HIGH)
    time.sleep(1000*60*10)
    for step in recipe['hop_process']:
        '''
        Implement way to wait for putting in hops
        '''
        time.sleep(1000 * 60 * step[])

    GPIO.output(relais_pin, GPIO.LOW)




client.loop_stop()