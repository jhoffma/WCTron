import time
from grovepi import *
import person_detector

def distanceCheck():
  global cabinStatus
  if int(person_detector.isPersonPresent(4, 50)) != cabinStatus:
    digitalWrite(freeLedPin, cabinStatus)
    digitalWrite(busyLedPin, 1 - cabinStatus)
    cabinStatus = 1 - cabinStatus

def paperButton():
  if digitalRead(noPaperButton) == 1:
    paperLedStatus = 1
    digitalWrite(paperLedPin, paperLedStatus)

  if digitalRead(newPaperButton) == 1:
    paperLedStatus = 0
    digitalWrite(paperLedPin, paperLedStatus)

def schedule(interval, callback):
  global schedules
  schedules[callback] = {'last': 0, 'interval': interval}

def run_schedule():
  current = time.time()
  for callback in schedules.keys():
    if schedules[callback]['last'] + schedules[callback]['interval'] < current:
      globals()[callback]()
      schedules[callback]['last'] = current

def checkSound():
  print analogRead(soundSensor)
  

start=time.time()
schedules = {}
schedule(.3, 'distanceCheck')
schedule(0.05, 'paperButton')
schedule(0.5, 'checkSound')

noPaperButton = 3
newPaperButton = 7
paperLedPin = 2
freeLedPin = 5
busyLedPin = 6
soundSensor = 0
pinMode(paperLedPin, "OUTPUT")
pinMode(noPaperButton, "INPUT")
pinMode(newPaperButton, "INPUT")
pinMode(soundSensor, "INPUT")
paperLedStatus = 0
cabinStatus = 0
digitalWrite(paperLedPin, paperLedStatus)
digitalWrite(freeLedPin, 1 - cabinStatus)

while True:
  run_schedule() 
  time.sleep(0.01)
