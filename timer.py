# Grovepi + grove RGB LCD module
 
# Example for using the Grove I2C color LCD
from grove_rgb_lcd import *
import socket
import paho.mqtt.client as mqtt
import json

topic = "WaaS/personDetector"
timerTopic = "WaaS/timer"

cabins = { '1': {'busy': False, 'time': time.time()}, '2': {'busy': False, 'time': time.time()}, '3': {'busy': False, 'time': time.time()}, '4': {'busy': False, 'time': time.time()}}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global cabins
    print(msg.payload)
    jsonObj = json.loads(msg.payload)
    cabinId = str(jsonObj["id"])
    if (jsonObj["action"] == "free"):
        cabins[cabinId]["busy"] = False
    if (jsonObj["action"] == "busy"):
        cabins[cabinId]["busy"] = True
	cabins[cabinId]["time"] = time.time()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()

setText("-" * 16 + "\n" + "-" * 16)

setRGB(0,255,255)

def process(id, isBusy, startTime, row):
    runSeconds = int(time.time() - startTime)
    
    data = {}
    data['id'] = id
    data['busy'] = isBusy
    data['hasJustChanged'] = runSeconds == 0
    data['runSeconds'] = runSeconds

    print "id: " + str(id) + ", isBusy: " + str(isBusy) + ", row: " + str(row)

    if not isBusy:
        pass
        #setTextInRow("Wolne,zapraszam!", row)
    else:
        seconds = int(runSeconds) % 60
        minutes = int(runSeconds / 60)
        setTextInRow("Srasz: " + str(minutes) + "m " + str(seconds) + "s ", row)
    client.publish(timerTopic, json.dumps(data))

try:
    while(True):
        process(2, cabins['2']['busy'], cabins['2']['time'], 0) 
        process(3, cabins['3']['busy'], cabins['3']['time'], 1)

        if cabins['2']["busy"] and cabins['3']["busy"]:
            setRGB(255, 0, 0)
        elif cabins['2']["busy"] or cabins['3']["busy"]:
            setRGB(255, 255, 0)
        else:
            setRGB(0, 255, 0)
        time.sleep(1)

except KeyboardInterrupt:
    setText("Not working\nSorry bro!")
    setRGB(255,255,255)
except IOError:
    setText("Not working\nSorry bro!")
    setRGB(255,255,255)
