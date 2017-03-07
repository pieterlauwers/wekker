#!/usr/bin/python

from SevenSegmentDisplay import Display
import time

lcd = Display([2,3,4,17,27,22,10,9],[14,15,18,23])
lcd.info()

lcd.snake()

lcd.setNumber(1234)
lcd.on()
time.sleep(2)
lcd.off()
time.sleep(1)
lcd.setNumber(9876)
lcd.on()
time.sleep(3)

for i in range(10, 100, 10):
  lcd.brightness = i
  time.sleep(1)
lcd.brightness = 10
time.sleep(1)
lcd.breaks = True