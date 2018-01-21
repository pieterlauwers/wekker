#!/usr/bin/python

from hourmin import Hourmin

alarm = Hourmin()
print(alarm)
alarm.inc()
print(alarm)
alarm.dec()
alarm.dec()
print(alarm)
