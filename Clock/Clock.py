import SevenSegmentDisplay
import time

class Clock():
  def __init__(self,segmentpins,digitpins):
    self.lcd = Display(segmentpins,digitpins)
    self.lcd.on()
    while True:
      now=time.ctime()
      self.lcd.displayString(now[11:13]+now[14:16]
      time.sleep(1)