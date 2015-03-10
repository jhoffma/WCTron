import time
from grovepi import *

def fartLight():
  try:
    digitalWrite(fartLightPin, int(analogRead(soundSensor) > 400))
  except:
    pass

soundSensor = 0
fartLightPin = 8
pinMode(soundSensor, "INPUT")
pinMode(fartLightPin, "OUTPUT")
