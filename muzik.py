import paho.mqtt.client as mqtt
import json
import subprocess
import os

topic = "WaaS/personDetector"

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    client.subscribe('WaaS/timer')


def on_message(client, userdata, msg):
    event = json.loads(msg.payload)
    print event
    if 'action' in event and event['action'] == 'busy':
        subprocess.Popen(["mpg321", "/home/pi/kabina_" + str(event['id']) + ".mp3"])
    elif 'action' in event and event['action'] == 'free':
        subprocess.Popen(["mpg321", "/home/pi/koniec_1.mp3"])
 

    if "runSeconds" in event and event['runSeconds'] == 120:
        subprocess.Popen(["mpg321", "/home/pi/2_minuty.mp3"])


       


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
