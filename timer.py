from datetime import datetime
from datetime import timedelta
import time
class Timer:
    """
    Schedule events (plain strings) in the future.
    Get the time till the first event.
    Retrieve the first event.
    Reschedule an event to a new time.
    Each event can only appear once.
    """
    def __init__(self):
        self.eventq = {}
    def schedule(self, timespec=datetime.now(), event=None):
        if not event in self.eventq:
            self.eventq[event] = {}
        if isinstance(timespec, datetime):
            self.eventq[event]['time'] = timespec
        elif isinstance(timespec, timedelta):
            self.eventq[event]['time'] = datetime.now() + timespec
    def interval(self,deltat=timedelta(seconds=1),event=None,initialtime=None):
        if not event in self.eventq:
            self.eventq[event] = {}
        if isinstance(initialtime, datetime):
            self.eventq[event]['time'] = initialtime
        elif isinstance(initialtime, timedelta):
            self.eventq[event]['time'] = datetime.now() + initialtime
        else:
            self.eventq[event]['time'] = datetime.now() + deltat
        self.eventq[event]['period'] = deltat
    def __gettimeof__(self, event):
        return self.eventq[event]['time']
    def nextdelay(self):
        if not self.empty():
            first_event = min(self.eventq, key=self.__gettimeof__)
            deltat = self.eventq[first_event]['time'] - datetime.now()
        else:
            deltat = timedelta(seconds=0)
        return max(deltat.total_seconds(), 0)
    def get(self,block=True):
        if block:
            time.sleep(self.nextdelay())
        if self.nextdelay() == 0:
            first_event = min(self.eventq, key=self.__gettimeof__)
            if 'period' in self.eventq[first_event]:
                self.eventq[first_event]['time'] += self.eventq[first_event]['period']
            else:
                self.eventq.pop(first_event)
            return first_event
        else:
            return None
    def delete(self,event):
        if event in self.eventq:
            self.eventq.pop(event)
    def has(self,event):
        return event in self.eventq
    def empty(self):
        return len(self.eventq) == 0
