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
import logging
import logging.handlers

logfilename = '/var/log/wekkerradio/wekkerradio.log'
log = logging.getLogger('MyLogger')
log.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(logfilename, maxBytes=1000000, backupCount=2)
log.addHandler(handler)

radio = Radio()
minvolume=-25
fadeoutvolume=minvolume
targetvolume=-10
fadeinvolume=targetvolume
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
    
def startradio():
    """
    A manual start of the radio
    Prepare the radio and fadeout to the target volume
    """
    lcd.dpOff(3) # Switch is in on mode, so no alarm indicator in the lcd
    global fadeoutvolume
    global fadeinvolume
    radio.prepare()
    if radio.volume > targetvolume:
        fadeoutvolume=targetvolume
    else:
        fadeoutvolume=radio.volume
    fadeinvolume=targetvolume
    timer.interval(deltat=timedelta(seconds=0.1),event='fadeout',initialtime=timedelta(seconds=0))
    timer.schedule(timespec=timedelta(minutes=70),event='radiotimeout')

def handlealarm():
    global fadeoutvolume
    global fadeinvolume
    log.debug('Alarm triggered')
    radio.prepare()
    fadeoutvolume=minvolume
    fadeinvolume=targetvolume
    timer.schedule(timespec=timedelta(minutes=70),event='radiotimeout')
    timer.interval(deltat=timedelta(seconds=0.1),event='fadeout',initialtime=timedelta(seconds=0))

def handlefadeout():
    if radio.volume == fadeoutvolume:
        timer.delete('fadeout')
        amplifier.on()
        timer.interval(deltat=timedelta(seconds=0.5),event='fadein',initialtime=timedelta(seconds=0))
        log.debug('Fadeout reached ' + str(fadeoutvolume) + '. Turning amplifier on and scheduling fadein.')
        return True
    else:
        radio.dec()
        log.debug('Volume is ' + str(radio.volume) + '. Fading out till ' + str(fadeoutvolume))
        return False

def handlefadein():
    if radio.volume == fadeinvolume:
        timer.delete('fadein')
        log.debug('Fadein reached ' + str(fadeinvolume) + '.')
        return True
    else:
        radio.inc()
        log.debug('Volume is ' + str(radio.volume) + '. Fading in till ' + str(fadeinvolume))
        return False

def handlevolumeinc():
    global targetvolume
    radio.inc()
    targetvolume = radio.volume
    
def handlevolumedec():
    global targetvolume
    radio.dec()
    targetvolume = radio.volume
    
def stopradio():
    amplifier.off()
    log.debug('Stopping radio')
    radio.stop()
    timer.delete('radiotimeout')

def displayalarmtime():
    lcd.displayString( str(alarmtime) )
    timer.schedule(timespec=timedelta(seconds=3),event='alarmdisplaytimeout')

def alarmindicatoron():
    lcd.dpOn(3)

def alarmindicatoroff():
    lcd.dpOff(3)
    
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
statemachine.append_state('playing',on_exit=stopradio)

statemachine.append_transition('idle','tick',action=updatetimedisplay)
statemachine.append_transition('fadingout','tick',action=updatetimedisplay)
statemachine.append_transition('fadingin','tick',action=updatetimedisplay)
statemachine.append_transition('playing','tick',action=updatetimedisplay)

statemachine.append_transition('idle','switch-auto',action=alarmindicatoron)
statemachine.append_transition('idle','switch-off',action=alarmindicatoroff)
statemachine.append_transition('playing','switch-auto',action=alarmindicatoron)

statemachine.append_transition('idle','switch-on',action=startradio,dst='fadingout')
statemachine.append_transition('idle','alarm',action=handlealarm,dst='fadingout')
statemachine.append_transition('fadingout','fadeout',condition=handlefadeout,dst='fadingin')
statemachine.append_transition('fadingin','fadein',condition=handlefadein,dst='playing')

statemachine.append_transition('playing','switch-off',action=alarmindicatoroff,dst='idle')
statemachine.append_transition('playing','radiotimeout',dst='idle')

statemachine.append_transition('playing','wheel-inc',action=handlevolumeinc)
statemachine.append_transition('playing','wheel-dec',action=handlevolumedec)

statemachine.append_transition('idle','wheel-pushdown',action=displayalarmtime,dst='alarmtime')
statemachine.append_transition('alarmtime','alarmdisplaytimeout',action=updatetimedisplay,dst='idle')
statemachine.append_transition('alarmtime','wheel-inc',action=incalarmtime)
statemachine.append_transition('alarmtime','wheel-dec',action=decalarmtime)

# Initial setup
updatetimedisplay()
if switch.is_auto():
    lcd.dpOn(3)
timer.interval(deltat=timedelta(minutes=1),initialtime=deltanextminute(),event='tick')
amplifier.off()

while True:
    try:
        event = q.get(block=True, timeout=timer.nextdelay())
    except queue.Empty:
        event = timer.get()
    log.debug(event)
    statemachine.event(event)
