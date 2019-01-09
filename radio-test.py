#!/usr/bin/python

from radio import Radio
import time


r = Radio()
r.prepare()
count = 0
while not r.isprepared():
    r.connect()
    count += 1
    print("Connect to omxplayer attempt {count}".format(count=count))
    time.sleep(0.1)
print("Connected")
for i in range (6):
    print("dec")
    r.dec()
    time.sleep(0.5)
for i in range (6):
    print("inc")
    r.inc()
    time.sleep(0.5)
time.sleep(2)
print("Time to say goodby")
r.stop()
