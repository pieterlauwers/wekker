#!/usr/bin/python

from SevenSegmentDisplay import Display
import time

lcd = Display([2,3,4,17,27,22,10,9],[14,15,18,23])
lcd.info()

lcd.snake()

lcd.setNumber(1234)
lcd.on()
time.sleep(1)
lcd.off()
time.sleep(0.5)
lcd.setNumber(9876)
lcd.on()
time.sleep(1)

for i in range(10, 100, 10):
  lcd.brightness = i
  time.sleep(0.1)
lcd.brightness = 10

#Sinus values
sinv=[0.0000000,0.3090170,0.5877853,0.8090170,0.9510565,1.0000000,0.9510565,0.8090170,0.5877853,0.3090170,0.0000000,-0.3090170,-0.5877853,-0.8090170,-0.9510565,-1.0000000,-0.9510565,-0.8090170,-0.5877853,-0.3090170]
# Fade 10 times
for i in range (1,10):
  for b in sinv:
    lcd.brightness = (b + 1) * 50
    time.sleep(0.1)
lcd.brightness = 10
time.sleep(1)
lcd.breaks = True