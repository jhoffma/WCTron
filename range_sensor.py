import person_detector
from grovepi import *
<<<<<<< HEAD
import paho.mqtt.client as mqtt
=======
import json
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("localhost", 1883, 60)
>>>>>>> cabin status every 1 second

distance_sensor_pin = 4
treshold = 50
freeLedPin = 5
busyLedPin = 6

last_published_status = False
last_sensor_status = False
consecutive_change_counter = 0
change_state_threshold = 8

digitalWrite(freeLedPin, 1)
digitalWrite(busyLedPin, 0)

def publisher_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

publisher = mqtt.Client()
publisher.on_connect = publisher_on_connect
publisher.connect("localhost", 1883, 60)
publisher.loop_start()
topic = "WaaS/personDetector"

def distanceCheck():
  global distance_sensor_pin, treshold, cabinStatus, last_published_status, last_sensor_status, consecutive_change_counter
  
  if last_published_status != last_sensor_status:
    consecutive_change_counter += 1
    print "Increasing consecutiv state change counter"
  else:
    consecutive_change_counter = 0  

  last_sensor_status = person_detector.isPersonPresent(distance_sensor_pin, treshold)

<<<<<<< HEAD
  if consecutive_change_counter == change_state_threshold:
    consecutive_change_counter = 0
    print "Publishing sensor status: ", last_sensor_status
    publisher.publish(topic, last_sensor_status)
    last_published_status = last_sensor_status
    digitalWrite(busyLedPin, int(last_published_status))
    digitalWrite(freeLedPin, 1 - int(last_published_status))
=======
  if int(person_detector.isPersonPresent(distance_sensor_pin, treshold)) != cabinStatus:
    digitalWrite(freeLedPin, cabinStatus)
    digitalWrite(busyLedPin, 1 - cabinStatus)
    cabinStatus = 1 - cabinStatus

def sendStatus():
  global client
  if cabinStatus == 0:
    action = 'free'
  else:
    action = 'busy'

  status = {'gender': 'm', 'action': action, 'id': 3 }
  client.publish('WaaS/user', json.dumps(status))
>>>>>>> cabin status every 1 second
