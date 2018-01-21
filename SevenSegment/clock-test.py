#!/usr/bin/python

from SevenSegmentDisplay import Display
import time

lcd = Display([4,10,23,17,15,18,25,27],[14,22,24,9])
lcd.brightness = 60
#lcd.on()

while True:
  timestring = time.ctime()
  minutes_seconds = timestring[14:16]+timestring[17:19]
  lcd.displayString(minutes_seconds)
  time.sleep(1)
