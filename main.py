
import time
from grovepi import *
from range_sensor import *
from paper_button import paperButton
from fart_light import fartLight


def schedule(interval, callback):
  global schedules
  schedules[callback] = {'last': 0, 'interval': interval}

def run_schedule():
  current = time.time()
  for callback in schedules.keys():
    if schedules[callback]['last'] + schedules[callback]['interval'] < current:
      globals()[callback]()
      schedules[callback]['last'] = current

start=time.time()

schedules = {}
schedule(.3, 'distanceCheck')
schedule(0.05, 'paperButton')
schedule(0.5, 'fartLight')
schedule(1, 'sendStatus')


while True:
  run_schedule() 
  time.sleep(0.01)
