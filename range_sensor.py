import person_detector
from grovepi import *
import json
import paho.mqtt.client as mqtt

distance_sensor_pins = {
  4: {'cabin': 3, 'gender': 'm', 'last_published': False, 'last_status': False, 'counter': 0},
  8: {'cabin': 4, 'gender': 'm', 'last_published': False, 'last_status': False, 'counter': 0},
}
treshold = 50
freeLedPin = 5
busyLedPin = 6

change_state_threshold = 2

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
  for pin in distance_sensor_pins.keys():
    sensor = distance_sensor_pins[pin]
    if distance_sensor_pins[pin]['last_published'] != distance_sensor_pins[pin]['last_status']:
      distance_sensor_pins[pin]['counter'] += 1
      print "Increasing consecutiv state change counter"
    else:
      distance_sensor_pins[pin]['counter'] =0

    distance_sensor_pins[pin]['last_status'] = person_detector.isPersonPresent(pin, treshold)

    if distance_sensor_pins[pin]['counter'] == change_state_threshold:
      distance_sensor_pins[pin]['counter'] =0
      if distance_sensor_pins[pin]['last_status'] == 0:
        action = 'free'
      else:
        action = 'busy'
      status = {'gender': sensor['gender'], 'action': action, 'id': sensor['cabin'] }
      publisher.publish(topic, json.dumps(status))
      print "Publishing sensor status: ", status
      s = distance_sensor_pins[pin]['last_published'] = distance_sensor_pins[pin]['last_status']
      digitalWrite(busyLedPin, int(s))
      digitalWrite(freeLedPin, 1 - int(s))

def sendStatus():
  for pin in distance_sensor_pins.keys():
    sensor = distance_sensor_pins[pin]
    if sensor['last_published'] == 0:
      action = 'free'
    else:
      action = 'busy'

    status = {'gender': sensor['gender'], 'action': action, 'id': sensor['cabin'] }
    publisher.publish('WaaS/user', json.dumps(status))
