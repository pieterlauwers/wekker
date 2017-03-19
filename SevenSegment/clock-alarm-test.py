#!/usr/bin/python

from SevenSegmentDisplay import Display
from gpiozero import Button
import time
import Queue

lcd = Display([2,3,4,17,27,22,10,9],[14,15,18,23])
button = Button(13,pull_up=True)
def button_down():
  global showalarm
  showalarm = True
  eventq.put(1)
def button_up():
  global showalarm
  showalarm = False
  eventq.put(1)
button.when_pressed = button_down
button.when_released = button_up

q = Queue.Queue()
eventq = Queue.Queue()
showalarm = False
alarmstring="1122"
timestring = time.ctime()
minutes_seconds = timestring[14:16]+time.ctime()[17:19]
lcd.displayString(minutes_seconds)
lcd.on()
while True:
  try:
    message = eventq.get(True,1)  # get events with timeout of 1 second
  except Queue.Empty:
    pass
  timestring = time.ctime()
  minutes_seconds = timestring[14:16]+time.ctime()[17:19]
  if showalarm:
    lcd.displayString(alarmstring)
  else:
    lcd.displayString(minutes_seconds)
