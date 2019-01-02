from gpiozero import LED
import time
import threading

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

class Display(threading.Thread):
  
  def __init__(self,segmentpins,digitpins):
    threading.Thread.__init__(self)
    self.segment = []
    for pin in segmentpins:
      led = LED(pin,False) # Segments are active LOW
      self.segment.append(led)

    self.digit = []
    for pin in digitpins:
      led = LED(pin,True) # Digits are active HIGH
      self.digit.append(led)
    
    self.displayString("    ")
    self.refreshrate = 50 #HZ
    self.brightness = 20 # %
    self.breaks = False
    self.running = True
    self.start()

  def info(self):
    print("Segments are")
    for led in self.segment:
      print(led.pin)
    print
    
    print("Digits are")
    for led in self.digit:
      print(led.pin)
    print

  def displayString(self,text):
    mypattern=[]
    for ch in text:
      mypattern.append(num[ch])
    self.pattern = mypattern
    
  def displayNumber(self,nr):
    nrstring = str(nr)
    self.displayString(nrstring)
    
  # Go over each segment of each digit    
  def snake(self):
    for d in self.digit:
      for s in self.segment:
        s.on()
        d.on()
        time.sleep(0.2)
        s.off()
        d.off()
        #time.sleep(0.01)

  def on(self):
    self.running = True
    
  def off(self):
    self.running = False

  def _timeOn(self):
    return self.brightness / (400.0 * self.refreshrate)
  
  def _timeOff(self):
    return (100 - self.brightness) / (400.0 * self.refreshrate)
    
  def run(self):
    while not self.breaks:
      if (self.running):
        for digi,dig in enumerate(self.digit):
          tupple = self.pattern[digi]
          for segi,seg in enumerate(self.segment):
            if (tupple[segi] == 1):
              seg.on()
            else:
              seg.off()
          dig.on()
          time.sleep( self._timeOn() )
          dig.off()
          time.sleep( self._timeOff() )
      else:
        time.sleep(0.001)
