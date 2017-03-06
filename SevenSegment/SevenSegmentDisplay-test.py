#!/usr/bin/python

from SevenSegmentDisplay import Display
import time

lcd = Display([2,3,4,17,27,22,10,9],[14,15,18,23])
lcd.info()
lcd.snake()

num = {' ':(0,0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0,0),
    '1':(0,1,1,0,0,0,0,0),
    '2':(1,1,0,1,1,0,1,0),
    '3':(1,1,1,1,0,0,1,0),
    '4':(0,1,1,0,0,1,1,0),
    '5':(1,0,1,1,0,1,1,0),
    '6':(1,0,1,1,1,1,1,0),
    '7':(1,1,1,0,0,0,0,0),
    '8':(1,1,1,1,1,1,1,0),
    '9':(1,1,1,1,0,1,1,0)}
p = [num['8'],num['1'],num['2'],num['3']] 
#lcd.printPattern(p)
#lcd.printNumber(8123)
lcd.on()
time.sleep(1)
lcd.setNumber(1234)
time.sleep(4)
lcd.off()
time.sleep(2)
lcd.setNumber(9876)
lcd.on()
time.sleep(4)
lcd.off()
lcd.breaks = True