from gpiozero import Button
import queue

class Switch():
    """
    Three state switch based on two pins and a common ground
    Returns states: on, auto, off
    Puts the state on an event queue is a queue object is provided during initialisation
    """
    def pushq(self):
        if self.queue:
            if self.name:
                event = self.name + '-' + self.state
            else:
                event = self.state
            self.queue.put(event)
    def pin_a_rising(self):
        self.state = "on"
        self.pushq()
    def pin_a_falling(self):
        self.state = "auto"
        self.pushq()
    def pin_b_rising(self):
        self.state = "off"
        self.pushq()
    def pin_b_falling(self):
        self.state = "auto"
        self.pushq()
    def __init__(self,pa,pb,name=None,queue=None):
        if name:
            self.name = name
        else:
            self.name = ""
        self.queue = queue
        self.pin_a = Button(pa)
        self.pin_b = Button(pb)
        self.pin_a.when_pressed = self.pin_a_rising       # Register the event handler for rotary pin A
        self.pin_a.when_released = self.pin_a_falling       # Register the event handler for rotary pin A
        self.pin_b.when_pressed = self.pin_b_rising       # Register the event handler for rotary pin A
        self.pin_b.when_released = self.pin_b_falling       # Register the event handler for rotary pin A
        if self.pin_a.is_pressed:
            self.state = "on"
        elif self.pin_b.is_pressed:
            self.state = "off"
        else:
            self.state = "auto"
    def is_on(self):
        return "on" == self.state
    def is_off(self):
        return "off" == self.state
    def is_auto(self):
        return "auto" == self.state