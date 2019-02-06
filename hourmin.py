from datetime import datetime, timedelta

class Hourmin():
  def __init__(self):
    self.dt = datetime.strptime('22220000','%Y%H%M')
    self.changetime = datetime.now()
    self.threshlodtime0 = timedelta(milliseconds=10)
    self.threshlodtime1 = timedelta(milliseconds=60)
    self.threshlodtime2 = timedelta(milliseconds=300)
    self.threshouldcount = 3

  def __str__(self):
    return self.dt.strftime('%H%M')

  def _adjust(self,i):
    now = datetime.now()
    deltat = now - self.changetime 
    ##print("time since last change is ",deltat.microseconds)
    if deltat < self.threshlodtime0:
        return  # debouncing
    elif deltat < self.threshlodtime1:
        delta = timedelta(hours=i)
    elif deltat < self.threshlodtime2:
        delta = timedelta(minutes=i*10)
    else:
        delta = timedelta(minutes=i)
    self.dt += delta
    self.changetime = now

  def inc(self):
    #print("inc")
    self._adjust(1)

  def dec(self):
    #print("dec")
    self._adjust(-1)
  