from radio import Radio
from rotaryencoder import Rotaryencoder
import queue
from SevenSegmentDisplay import Display
from switch import Switch
from gpiozero import LED
from fsm import Fsm
from timer import Timer
from hourmin import Hourmin
import time
from datetime import datetime
from datetime import timedelta

radio = Radio()
q = queue.Queue()
switch = Switch(12,16,name='switch',queue=q)
wheel = Rotaryencoder(11,7,6,name='wheel',queue=q)
amplifier = LED(19)
lcd = Display([4,10,23,17,15,18,25,27],[14,22,24,9])
alarmtime = Hourmin()
statemachine = Fsm('idle')
timer = Timer()


def deltanextminute():
    now = datetime.now()
    plus1min = now + timedelta(minutes=1)
    nextmin = datetime( year=plus1min.year, month = plus1min.month, day=plus1min.day, hour=plus1min.hour, minute=plus1min.minute)
    deltaseconds = nextmin - now
    return deltaseconds

def updatetimedisplay():
    timestring = datetime.now().strftime('%H%M')
    lcd.displayString(timestring)
    timer.schedule('tick',deltanextminute())

def radioconnect():
    print('Attempt connect')
    radio.connect()
    if radio.isprepared():
        timer.schedule('gotoconnected',timedelta(seconds=0))
    else:
        timer.schedule('connect',timedelta(seconds=5))

def prepareradio():
    print('preparing')
    radio.prepare()
    print('Scheduling connect')
    timer.schedule('connect',timedelta(seconds=5))

def stopradio():
    print('Stopping radio')
    radio.stop()

def displayalarmtime():
    lcd.displayString( str(alarmtime) )
    timer.schedule('timeout',timedelta(seconds=3))

def incalarmtime():
    alarmtime.inc()
    lcd.displayString( str(alarmtime) )
    timer.schedule('timeout',timedelta(seconds=3))
    
def decalarmtime():
    alarmtime.dec()
    lcd.displayString( str(alarmtime) )
    timer.schedule('timeout',timedelta(seconds=3))

statemachine.append_state('playing',on_exit=stopradio)
statemachine.append_transition('idle','tick',action=updatetimedisplay)
statemachine.append_transition('preparing','tick',action=updatetimedisplay)
statemachine.append_transition('playing','tick',action=updatetimedisplay)
statemachine.append_transition('idle','switch-on',action=prepareradio,dst='preparing')
statemachine.append_transition('preparing','connect',action=radioconnect)
statemachine.append_transition('preparing','gotoconnected',dst='playing')
statemachine.append_transition('playing','switch-off',dst='idle')
statemachine.append_transition('playing','wheel-inc',action=radio.inc)
statemachine.append_transition('playing','wheel-dec',action=radio.dec)

statemachine.append_transition('idle','wheel-pushdown',action=displayalarmtime,dst='alarmtime')
statemachine.append_transition('alarmtime','timeout',action=updatetimedisplay,dst='idle')
statemachine.append_transition('alarmtime','wheel-inc',action=incalarmtime)
statemachine.append_transition('alarmtime','wheel-dec',action=decalarmtime)

# Initial setup
updatetimedisplay()

while True:
    try:
        event = q.get(block=True, timeout=timer.nextdelay())
    except queue.Empty:
        event = timer.pop()
    print(event)
    statemachine.event(event)
