import paho.mqtt.client as mqtt
import json
import subprocess
import os

topic = "WaaS/personDetector"

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)


def on_message(client, userdata, msg):
    event = json.loads(msg.payload)
    if event['action'] == 'busy':
        subprocess.Popen(["mpg321", "/home/pi/kabina_3.mp3"])
       


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
