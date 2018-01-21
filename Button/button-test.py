#!/usr/bin/python

from gpiozero import Button

button = Button(13,pull_up=True)
button.wait_for_press()
print("The button was pressed!")
