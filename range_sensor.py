import person_detector
from grovepi import *

distance_sensor_pin = 4
treshold = 50
freeLedPin = 5
busyLedPin = 6
cabinStatus = 0

digitalWrite(freeLedPin, 1 - cabinStatus)

def distanceCheck():
  global distance_sensor_pin, treshold, cabinStatus  

  if int(person_detector.isPersonPresent(distance_sensor_pin, treshold)) != cabinStatus:
    digitalWrite(freeLedPin, cabinStatus)
    digitalWrite(busyLedPin, 1 - cabinStatus)
    cabinStatus = 1 - cabinStatus
