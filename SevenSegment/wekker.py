#!/usr/bin/python

from SevenSegmentDisplay import Display
from hourmin import Hourmin
from radio import Radio
from rotaryencoder import Rotaryencoder
import time
from datetime import datetime, timedelta
import sys
from gpiozero import Button
import Queue

lcd = Display([4,10,23,17,15,18,25,27],[14,22,24,9])
eventq = Queue.Queue()
wheel = Rotaryencoder(11,7,6,eventq)

alarmtime=Hourmin()
preparedelta=timedelta(seconds=30)
playdelta=timedelta(seconds=20)
playingtime=timedelta(minutes=1)
radio = Radio()

def timebetween(t,min,max):
    return ( min.time() <= t.time() ) and ( t.time() <= max.time() )

while True:

    # Handle events from buttons
    try:
        message = eventq.get(True, 1)      # Get an item from the event queue, raise the empty exception after 1 second
        print("message: ",message)
        if message == "inc":
            if wheel.pin_btn.is_pressed:
                alarmtime.inc()
            elif radio.isplaying():
                radio.inc()
            else:
                lcd.brightness = min( lcd.brightness + 5 , 100)
                print(lcd.brightness)
        elif message == "dec":
            if wheel.pin_btn.is_pressed:
                alarmtime.dec()
            elif radio.isplaying():
                radio.dec()
            else:
                lcd.brightness = max( lcd.brightness - 5 , 0)
                print(lcd.brightness)
        else:
            #print "No event handler for ", message
            None
    except Queue.Empty:
        print "no action"
        #pass #print "no action"
    except KeyboardInterrupt:
        lcd.breaks = True
        sys.exit()

    # Handle time based events
    now = datetime.now()
    if timebetween(now,alarmtime.dt-preparedelta,alarmtime.dt-playdelta) and not radio.isprepared():
        radio.prepare()
    elif timebetween(now,alarmtime.dt-playdelta,alarmtime.dt):
        if not radio.isplaying():
            radio.play()
        elif radio.volume < 0:
            radio.inc()
    elif timebetween(now, alarmtime.dt + playingtime, alarmtime.dt + playingtime + playdelta) and radio.isplaying():
        radio.stop()
        
    # Update display
    if wheel.pin_btn.is_pressed:
        lcd.displayString( str(alarmtime) )
    else:
        timestring = now.strftime('%H%M')
        lcd.displayString(timestring)
