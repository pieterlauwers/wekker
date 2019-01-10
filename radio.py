import subprocess
from omxcontrol import *
import time

MAXVOL=20
MINVOL=-20

class Radio():
  def __init__(self):
    self.url="http://icecast.vrtcdn.be/radio1-high.mp3"
    self.volume=0
    self.prepared = False
    self.omx = None

  def __str__(self):
    return self.url

  def inc(self):
    if self.volume < MAXVOL and self.omx:
        # print("Volume inc")
        self.omx.action(OmxControl.ACTION_INCREASE_VOLUME)
        self.volume += 1

  def dec(self):
    if self.volume > MINVOL and self.omx:
        # print("Volume dec")
        self.omx.action(OmxControl.ACTION_DECREASE_VOLUME)
        self.volume -= 1
    
  def prepare(self):
    if not self.prepared:
        # print("Radio preparing")
        subprocess.Popen(['omxplayer',self.url],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

  def connect(self):
    try:
      self.omx = OmxControl()
      self.prepared = True
      return True
    except OmxControlError:
      return False
      
##  Pause and resume are apparently not working in this setup
##  def play(self):
##    if not self.active:
##        print("Radio started")
##        self.omx.pause()
##        self.active = True

  def stop(self):
    self.omx.quit()
    self.prepared = False

  def isprepared(self):
    return self.prepared
