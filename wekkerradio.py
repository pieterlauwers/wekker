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
    delta = nextmin - now
    return delta

def updatetimedisplay():
    timestring = datetime.now().strftime('%H%M')
    lcd.displayString(timestring)

def prepareradio():
    print('preparing')
    radio.prepare()
    print('Scheduling connect')
    timer.interval(deltat=timedelta(seconds=1),event='connect',initialtime=timedelta(seconds=10))

def startradio():
    amplifier.on()
    print('Delete connect event')
    timer.delete('connect')
    print('Schedule radio timeout')
    timer.schedule(timespec=timedelta(minutes=70),event='radiotimeout')

def stopradio():
    amplifier.off()
    print('Stopping radio')
    radio.stop()
    timer.delete('radiotimeout')

def displayalarmtime():
    lcd.displayString( str(alarmtime) )
    timer.schedule(timespec=timedelta(seconds=3),event='alarmdisplaytimeout')

def deltaalarm():
    now = datetime.now()
    alarmtoday = datetime(now.year, now.month, now.day, alarmtime.dt.hour, alarmtime.dt.minute)
    if now < alarmtoday:
        return alarmtoday - now
    else:
        return alarmtoday + timedelta(days=1) - now
    
def incalarmtime():
    alarmtime.inc()
    lcd.displayString( str(alarmtime) )
    timer.schedule(timespec=timedelta(seconds=3),event='alarmdisplaytimeout')
    timer.interval(deltat=timedelta(days=1),event='alarm',initialtime=deltaalarm())
    
def decalarmtime():
    alarmtime.dec()
    lcd.displayString( str(alarmtime) )
    timer.schedule(timespec=timedelta(seconds=3),event='alarmdisplaytimeout')
    timer.interval(deltat=timedelta(days=1),event='alarm',initialtime=deltaalarm())

# Define the states and the transitions in the state machine
statemachine.append_state('playing',on_enter=startradio,on_exit=stopradio)

statemachine.append_transition('idle','tick',action=updatetimedisplay)
statemachine.append_transition('preparing','tick',action=updatetimedisplay)
statemachine.append_transition('playing','tick',action=updatetimedisplay)

statemachine.append_transition('idle','switch-on',action=prepareradio,dst='preparing')
statemachine.append_transition('idle','alarm',action=prepareradio,dst='preparing')
statemachine.append_transition('preparing','connect',condition=radio.connect,dst='playing')
statemachine.append_transition('playing','switch-off',dst='idle')
statemachine.append_transition('playing','radiotimeout',dst='idle')

statemachine.append_transition('playing','wheel-inc',action=radio.inc)
statemachine.append_transition('playing','wheel-dec',action=radio.dec)

statemachine.append_transition('idle','wheel-pushdown',action=displayalarmtime,dst='alarmtime')
statemachine.append_transition('alarmtime','alarmdisplaytimeout',action=updatetimedisplay,dst='idle')
statemachine.append_transition('alarmtime','wheel-inc',action=incalarmtime)
statemachine.append_transition('alarmtime','wheel-dec',action=decalarmtime)

# Initial setup
updatetimedisplay()
timer.interval(deltat=timedelta(minutes=1),initialtime=deltanextminute(),event='tick')
amplifier.off()

while True:
    try:
        event = q.get(block=True, timeout=timer.nextdelay())
    except queue.Empty:
        event = timer.get()
    print(event)
    statemachine.event(event)
