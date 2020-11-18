#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

# Connect EV3 color sensor
cl = ColorSensor()

cl.mode='COL-REFLECT'

def color():
	# Connect EV3 color sensor
	cl = ColorSensor()
	print(cl.value())
	# Put the color sensor into COL-REFLECT mode
	# to measure reflected light intensity.
	# In this mode the sensor will return a value between 0 and 100
	cl.mode='COL-REFLECT'
		
	if(cl.value() >= 9 and cl.value() < 15):
		return "green"
	elif(cl.value() >= 15 and cl.value() < 24):
		return "blue"
	
	elif(cl.value() >= 67 and cl.value() < 84):
		return("white")
	elif(cl.value() >= 4 and cl.value() < 9):
		return ("dark blue")
	
	elif(cl.value() >= 53 and cl.value() < 65):
		return("red")
	elif(cl.value() >=2 and cl.value() < 3):
		return("black")
	else:
		return("v")
		
#print(color())
