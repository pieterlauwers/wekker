#!/usr/bin/python

from SevenSegmentDisplay import Display
import time

lcd = Display([2,3,4,17,27,22,10,9],[14,15,18,23])

timestring = time.ctime()
minutes_seconds = timestring[14:16]+time.ctime()[17:19]
lcd.displayString(minutes_seconds)
lcd.on()
while True:
  timestring = time.ctime()
  minutes_seconds = timestring[14:16]+time.ctime()[17:19]
  lcd.displayString(minutes_seconds)
  time.sleep(1)
