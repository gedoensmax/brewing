import paho.mqtt.client as mqtt
import time


client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, rc):
	print("Disconnected From Broker")


client.on_connect = on_connect

client.connect("137.226.248.146", 1883 ,60)
#client.loop_start()
import sys
topic =  "/1234/fmu/attrs"
payload = "sp|25.6"

time.sleep(1)
print("Publisher publishing input variable!!!!")
print("" +str(topic) + ":" +  str(payload))
client.publish(topic, str(payload) )

sys.stdout.flush()

