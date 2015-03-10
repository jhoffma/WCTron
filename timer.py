# Grovepi + grove RGB LCD module
 
# Example for using the Grove I2C color LCD
from grove_rgb_lcd import *
import socket
import paho.mqtt.client as mqtt
import json

changesTopic = "WaaS/personDetector"
statusTopic = "WaaS/user"
timerTopic = "WaaS/timer"

cabins = { '2': {'busy': False, 'beginTime': int(time.time()), 'endTime': int(time.time())}, '3': {'busy': False, 'beginTime': int(time.time()), 'endTime': int(time.time())}}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(changesTopic)
    client.subscribe(statusTopic)

def on_message(client, userdata, msg):
    global cabins
    #print(msg.payload)
    jsonObj = json.loads(msg.payload)
    cabinId = str(jsonObj["id"])
    if msg.topic == statusTopic:
        cabins[cabinId]["busy"] = jsonObj["action"] == "busy"
    elif msg.topic == changesTopic:
        t = int(time.time())
        if (jsonObj["action"] == "free"):
            cabins[cabinId]["busy"] = False
            cabins[cabinId]["endTime"] = t
        if (jsonObj["action"] == "busy"):
            cabins[cabinId]["busy"] = True
	    cabins[cabinId]["beginTime"] = t

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()

setText("-" * 16 + "\n" + "-" * 16)

setRGB(0,255,255)

def process(id, status, row):
    print str(id) + ": " + str(status)

    isBusy = status['busy']
    beginTime = status['beginTime']
    endTime = status['endTime']

    runSeconds = int(time.time() - beginTime)
    
    data = {}
    data['id'] = id
    data['busy'] = isBusy
    data['hasJustChanged'] = runSeconds == 0
    if not isBusy:
        data['runSeconds'] = int(time.time()) - endTime
    else:
        data['runSeconds'] = runSeconds
    data['gender'] = 'm'

    #print "id: " + str(id) + ", isBusy: " + str(isBusy) + ", row: " + str(row)

    if not isBusy:
        #pass
	runSeconds = endTime - beginTime
	seconds = int(runSeconds) % 60
	minutes = int(runSeconds / 60)
        setTextInRow("Srano: " + str(minutes) + "m " + str(seconds) + "s ", row)
    else:
        seconds = int(runSeconds) % 60
        minutes = int(runSeconds / 60)
        setTextInRow("Srasz: " + str(minutes) + "m " + str(seconds) + "s ", row)

    client.publish(timerTopic, json.dumps(data))


try:
    while(True):
        process(2, cabins['2'], 0) 
        process(3, cabins['3'], 1)

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
