#!/usr/bin/python

from gpiozero import Button

knop = Button(16)

def pressed():
  print("pressed")

def released():
  print("released")

knop.when_pressed = pressed
knop.when_released = released

input("push the knob, press Enter to quit.\n")