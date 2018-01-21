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
    self.active = False
    self.omx = None

  def __str__(self):
    return self.url + self.volume

  def inc(self):
    if self.volume < MAXVOL and self.omx:
        print("Volume inc")
        self.omx.action(OmxControl.ACTION_INCREASE_VOLUME)
        self.volume = self.volume + 1

  def dec(self):
    if self.volume > MINVOL and self.omx:
        print("Volume dec")
        self.omx.action(OmxControl.ACTION_DECREASE_VOLUME)
        self.volume = self.volume - 1
    
  def prepare(self):
    if not self.prepared:
        print("Radio prepared")
        subprocess.Popen(["omxplayer",self.url])
        count=0
        while count < 10 and not self.omx:
            count = count + 1
            try:
                self.omx = OmxControl()
            except OmxControlError:
                time.sleep(1)
        print("Count reached ",count)
        self.omx.pause()
        count = 0
        while count < 20:
            count = count + 1
            self.dec()
        self.prepared = True
      
  def play(self):
    if not self.active:
        print("Radio started")
        self.omx.pause()
        self.active = True

  def isprepared(self):
    return self.prepared

  def isplaying(self):
    return self.active

  def stop(self):
    print("Radio stopped")
    subprocess.Popen(["pkill","-f", "omxplayer"])
    self.active = False
