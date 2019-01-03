#!/usr/bin/python

from rotaryencoder import Rotaryencoder
from queue import Queue

eventq = Queue()

wheel = Rotaryencoder(11,7,6,name='wheel',queue=eventq)

while True:
    message = eventq.get()
    print(message)
    print(wheel.value)
