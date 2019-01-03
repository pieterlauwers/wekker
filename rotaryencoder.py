from gpiozero import Button

class Rotaryencoder():
    def pin_a_rising(self):                               # Pin A rising while A is active is a counter clockwise turn
        if self.pin_b.is_pressed:
            self.value -= 1
            if self.queue:
                event = 'dec'
                if self.name:
                    event = self.name + '-' + event
                self.queue.put(event)
                                                
    def pin_b_rising(self):                               # Pin B rising while A is active is a clockwise turn
        if self.pin_a.is_pressed:
            self.value += 1
            if self.queue:
                event = 'inc'
                if self.name:
                    event = self.name + '-' + event
                self.queue.put(event)

    def pin_btn_rising(self):                             # Push button event handler
        if self.queue:
            event = 'pushdown'
            if self.name:
                event = self.name + '-' + event
            self.queue.put(event)
    def pin_btn_falling(self):                            # Push button event handler
        if self.queue:
            event = 'pushup'
            if self.name:
                event = self.name + '-' + event
            self.queue.put(event)

    def __init__(self,pa,pb,pbtn,name=None,queue=None):
        self.pin_a = Button(pa)
        self.pin_a.when_pressed = self.pin_a_rising       # Register the event handler for rotary pin A
        self.pin_b = Button(pb)
        self.pin_b.when_pressed = self.pin_b_rising       # Register the event handler for rotary pin A
        self.pin_btn = Button(pbtn)
        self.pin_btn.when_pressed  = self.pin_btn_rising  # Register the event handler for rotary push button
        self.pin_btn.when_released = self.pin_btn_falling # Register the event handler for rotary push button
        self.value = 0
        self.queue = queue
        self.name = name


