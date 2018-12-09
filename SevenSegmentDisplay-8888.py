#!/usr/bin/python

from SevenSegmentDisplay import Display
import time

#lcd = Display([2,3,4,17,27,22,10,9],[14,15,18,23])
lcd = Display([4,10,23,17,15,18,25,27],[14,22,24,9])

lcd.info()

lcd.displayNumber(8888)
lcd.on()

input("Press Enter to quit.\n")