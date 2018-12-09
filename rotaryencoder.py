from gpiozero import Button

class Rotaryencoder():
    def pin_a_rising(self):                               # Pin A rising while A is active is a counter clockwise turn
        if self.pin_b.is_pressed:
            self.value -= 1
            if self.q: self.q.put("dec")
                                                
    def pin_b_rising(self):                               # Pin B rising while A is active is a clockwise turn
        if self.pin_a.is_pressed:
            self.value += 1
            if self.q: self.q.put("inc")

    def pin_btn_rising(self):                             # Push button event handler
        if self.q: self.q.put("pushdown")
    def pin_btn_falling(self):                            # Push button event handler
        if self.q: self.q.put("pushup")

    def __init__(self,pa,pb,pbtn,q=None):
        self.pin_a = Button(pa)
        self.pin_a.when_pressed = self.pin_a_rising       # Register the event handler for rotary pin A
        self.pin_b = Button(pb)
        self.pin_b.when_pressed = self.pin_b_rising       # Register the event handler for rotary pin A
        self.pin_btn = Button(pbtn)
        self.pin_btn.when_pressed  = self.pin_btn_rising  # Register the event handler for rotary push button
        self.pin_btn.when_released = self.pin_btn_falling # Register the event handler for rotary push button
        self.value = 0
        self.q = q


