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
  eventq.put("press")
def button_up():
  global showalarm
  showalarm = False
  eventq.put("release")
button.when_pressed = button_down
button.when_released = button_up

bit1 = Button(pin=20, pull_up=True, bounce_time=None)
bit2 = Button(pin=21, pull_up=True, bounce_time=None)
prev_bit1 = False
prev_bit2 = False
delta=-1
count=0
prevcount=0
deltacount=0
value=0
def changed(pin):
  global delta
  global count
  if (pin==bit1):
    count += delta
  else:
    count -= delta
  delta = (-1) * delta
  if (count % 4 == 0): eventq.put("turn")
  #print "pin %s changed, count=%d next delta=%d"%(pin.pin,count,delta)
bit1.when_pressed = changed
bit1.when_released = changed
bit2.when_pressed = changed
bit2.when_released = changed

q = Queue.Queue()
eventq = Queue.Queue()
showalarm = False
alarmtime=1122
timestring = time.ctime()
minutes_seconds = timestring[14:16]+time.ctime()[17:19]
lcd.displayString(minutes_seconds)
lcd.on()
message=""
while True:
  try:
    message = eventq.get(True,1)  # get events with timeout of 1 second
  except Queue.Empty:
    pass
  if (message == "turn"):
    if button.is_pressed:
      verschil = (count - prevcount) / 4
      alarmtime = alarmtime + verschil
    prevcount = count
  timestring = time.ctime()
  minutes_seconds = timestring[14:16]+time.ctime()[17:19]
  if showalarm:
    lcd.displayNumber(alarmtime)
  else:
    lcd.displayString(minutes_seconds)
