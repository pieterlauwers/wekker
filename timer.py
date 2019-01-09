from datetime import datetime
from datetime import timedelta
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
    def schedule(self,event,deltat=timedelta(seconds=0)):
        self.eventq[event] = datetime.now() + deltat
    def nextdelay(self):
        if not self.empty():
            first_event = min(self.eventq, key=self.eventq.get)
            deltat = self.eventq[first_event] - datetime.now()
        else:
            deltat = timedelta(seconds=0)
        return max(deltat.total_seconds(), 0)
    def pop(self):
        first_event = min(self.eventq, key=self.eventq.get)
        self.eventq.pop(first_event)
        return first_event
    def has(self,event):
        return event in self.eventq
    def empty(self):
        return len(self.eventq) == 0
