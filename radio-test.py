#!/usr/bin/python

from radio import Radio
import time

wr = Radio()
wr.play()
time.sleep(2)
print wr.isplaying()

#input("Enter to stop playing.\n")
time.sleep(10)
wr.stop()
print wr.isplaying()
input("Enter to quit.\n")
