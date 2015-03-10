from grovepi import *

def paperButton():
  if digitalRead(noPaperButton) == 1:
    paperLedStatus = 1
    digitalWrite(paperLedPin, paperLedStatus)

  if digitalRead(newPaperButton) == 1:
    paperLedStatus = 0
    digitalWrite(paperLedPin, paperLedStatus)

noPaperButton = 3
newPaperButton = 7
paperLedPin = 2
paperLedStatus = 0
pinMode(paperLedPin, "OUTPUT")
pinMode(noPaperButton, "INPUT")
pinMode(newPaperButton, "INPUT")
digitalWrite(paperLedPin, paperLedStatus)
