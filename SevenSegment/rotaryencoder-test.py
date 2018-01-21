#!/usr/bin/python

from rotaryencoder import Rotaryencoder
import Queue

eventq = Queue.Queue()

wheel = Rotaryencoder(11,7,6,eventq)

while True:
    message = eventq.get()
    print(message)
    print wheel.value
    
    