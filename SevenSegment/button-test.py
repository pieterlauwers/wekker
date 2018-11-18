#!/usr/bin/python

from gpiozero import Button

knop = Button(12)

def pressed():
  print("pressed")

def released():
  print("released")

knop.when_pressed = pressed
knop.when_released = released

input("push the knob, press Enter to quit.\n")