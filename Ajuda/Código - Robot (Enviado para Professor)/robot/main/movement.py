#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev2.motor import LargeMotor, OUTPUT_C, OUTPUT_B, SpeedPercent
from ev3dev2.sound import Sound
from time import sleep
from attack import takeBullet, takePart
from colorSensor import color
#--------------------------------------------------------------------------------

# Entradas / ligações EV3 motors.
# OUTPUT_C -> Motor responsável pelo movimento para frente e para trás.
# OUTPUT_B -> Motor responsável pelo movimento da direção.
# S - Sul.
# E - Este.
# N - Norte.
# W - Oeste.
#--------------------------------------------------------------------------------

# Declaração das entradas dos motores.
steering = LargeMotor(OUTPUT_B)
engine = LargeMotor(OUTPUT_C)
#--------------------------------------------------------------------------------

# Declaração das variáveis.
speed_steering = 20
speed_engine = 50
forward = -5.5
back = 5.5
right = 100
left = -100
#--------------------------------------------------------------------------------

# Casos dos movimentos posiveis para o robot.
def move(coord, dir) : 
	sound = Sound()
	newCoord = coord
	if(dir == 'N') :
		if(coord[1]>1) :
			engine.on_for_rotations(SpeedPercent(speed_engine), -3)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), -3.8)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), -4)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), -3.8)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.5)
			steering.reset()
			engine.reset()
			sound.speak('ok')
			newCoord[1] = coord[1] -1
		else:
			print('fora do tabuleiro')
	elif(dir == 'S') :
		if(coord[1] < 6) :
			engine.on_for_rotations(SpeedPercent(speed_engine), forward)
			sound.speak('ok')
			newCoord[1] = coord[1] +1
		else:
			print('fora do tabuleiro')    
	elif(dir =='W') :
		if(coord[0]>1) :
			engine.on_for_rotations(SpeedPercent(speed_engine), 0.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), -4.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), -5.4)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.6)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), -0.2)
			steering.reset()
			engine.reset()
			sound.speak('ok')
			newCoord[0] = coord[0] -1
		else:
			print('fora do tabuleiro')
	elif(dir == 'E') :
		if(coord[0]<6) :
			engine.on_for_rotations(SpeedPercent(speed_engine), 0.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), -3.6)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), -4.6)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.4)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			sound.speak('ok')
			steering.reset()
			engine.reset()
			newCoord[0] = coord[0] +1
		else:
			print('fora do tabuleiro') 
	else:
		sound.speak('Erro')
	return newCoord
#--------------------------------------------------------------------------------

# Casos dos movimentos posiveis para o robot para o segundo movimento com reconhecimento para a casa que vai.
def	move2(coord, dir):
	sound = Sound()
	newCoord = coord
	catch = ''
	if(dir == 'N') :
		if(coord[1]>1):
			engine.on_for_rotations(SpeedPercent(speed_engine), -3)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), -3.8)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			sleep(0.5)
			squareColor = color()
			sleep(0.5)
			if(squareColor == "dark blue"):
				takeBullet(coord,'S')
				catch = 'bullet'
				engine.on_for_rotations(SpeedPercent(speed_engine), -2)
			elif(squareColor == "green"):
				takePart(coord,'S')
				catch = 'part'
				engine.on_for_rotations(SpeedPercent(speed_engine), -2)
			else:				
				engine.on_for_rotations(SpeedPercent(speed_engine), -4)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), -3.6)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.5)
			steering.reset()
			engine.reset()
			sound.speak('ok')
			newCoord[1] = coord[1] -1
		else:
			print('fora do tabuleiro')
	elif(dir == 'S') :
		if(coord[1] < 6) :
			engine.on_for_rotations(SpeedPercent(speed_engine), forward/2 - 0.3)
			sleep(0.5)
			squareColor = color()
			sleep(0.5)
			if(squareColor == "dark blue"):
				takeBullet(coord,'S')
				catch = 'bullet'
				engine.on_for_rotations(SpeedPercent(speed_engine), 0.5)
			elif(squareColor == "green"):
				takePart(coord,'S')
				catch = 'part'
				engine.on_for_rotations(SpeedPercent(speed_engine), 0.5)
			else:
				engine.on_for_rotations(SpeedPercent(speed_engine), forward/2 + 0.3)
			sound.speak('ok')
			newCoord[1] = coord[1] +1
		else:
			print('fora do tabuleiro')    
	elif(dir =='W') :
		if(coord[0]>1) :
			engine.on_for_rotations(SpeedPercent(speed_engine), 0.4)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), -3.6)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			sleep(0.5)
			squareColor = color()
			sleep(0.5)
			if(squareColor == "dark blue"):
				takeBullet(coord,'S')
				catch = 'bullet'
				engine.on_for_rotations(SpeedPercent(speed_engine), -2.7)
			elif(squareColor == "green"):
				takePart(coord,'S')
				catch = 'part'
				engine.on_for_rotations(SpeedPercent(speed_engine), -2.7)
			else:				
				engine.on_for_rotations(SpeedPercent(speed_engine), -5.4)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.6)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), -0.2)
			steering.reset()
			engine.reset()
			sound.speak('ok')
			newCoord[0] = coord[0] -1
		else:
			print('fora do tabuleiro')
	elif(dir == 'E') :
		if(coord[0]<6) :
			engine.on_for_rotations(SpeedPercent(speed_engine), 0.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), -4.2)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			sleep(0.5)
			squareColor = color()
			sleep(0.5)
			if(squareColor == "dark blue"):
				takeBullet(coord,'S')
				catch = 'bullet'
				engine.on_for_rotations(SpeedPercent(speed_engine), -2.7)
			elif(squareColor == "green"):
				takePart(coord,'S')
				catch = 'part'
				engine.on_for_rotations(SpeedPercent(speed_engine), -2.7)
			else:				
				engine.on_for_rotations(SpeedPercent(speed_engine), -5.4)
			steering.on_for_degrees(SpeedPercent(speed_steering), left)
			engine.on_for_rotations(SpeedPercent(speed_engine), 3.4)
			steering.on_for_degrees(SpeedPercent(speed_steering), right)
			engine.on_for_rotations(SpeedPercent(speed_engine),0.4)
			#sound.speak('ok')
			steering.reset()
			engine.reset() 
			newCoord[0] = coord[0] +1
		else:
			print('fora do tabuleiro') 
	else:
		sound.speak('Erro')
	return newCoord, catch
#--------------------------------------------------------------------------------