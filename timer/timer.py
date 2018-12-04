from datetime import datetime, timedelta
import sched, time
import uuid

class Event:
    def __init__(self,deltatime,action):
        self.time = datetime.now() + deltatime
        self.action = action
        self.id = uuid.uuid4()
    def reschedule(self,deltatime):
        self.time = datetime.now() + deltatime
    def __str__(self):
        return self.action
    def __eq__(self,other):
        return self.id == other.id

class Timer:
    def __init__(self,func):
        self.eventq = []
        self.timer = sched.scheduler(time.time, time.sleep)
        self.callback = func
    def schedule(self,event):
        if not event in self.eventq:
            self.eventq.append(event)
        else:
            print(event, " is already in the queue.")
        self.sort()
    def sort(self):
        self.eventq.sort(key=lambda x: x.time)
    def run(self):
        self.sort()
        self.timer.enterabs(self.eventq[0].time,self.callback,())
    def pop(self):
        return self.eventq.pop(0)
    def has(self,event):
        return event in self.eventq

def action(act):
    print(act)

if __name__ == '__main__':
    clock = Timer(func=action)
    start = Event(timedelta(seconds=16),'start')
    clock.schedule(start)
    if clock.has(start):
        print("yes")
    start.reschedule(timedelta(seconds=23))
    stop = Event(timedelta(seconds=48),'stop')
    clock.schedule(stop)
    tussentijd = Event(timedelta(seconds=32),'blib')
    clock.schedule(tussentijd)
    stop.reschedule(timedelta(seconds=29))
    clock.schedule(stop)
    clock.run()
    print(clock.pop())
    print(clock.pop())
    print(clock.pop())
