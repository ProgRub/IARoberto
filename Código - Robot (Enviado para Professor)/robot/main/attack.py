#!/usr/bin/env python3
import random
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_B, OUTPUT_C, OUTPUT_A, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
#from ev3dev.ev3 import *
from colorSensor import color
from time import sleep

angle = 100
steering = LargeMotor(OUTPUT_B)
movementMotor = LargeMotor(OUTPUT_C)
claw = MediumMotor(OUTPUT_A)
ultrasonics = UltrasonicSensor(INPUT_1)
sound = Sound()
speed_moving = 50
speed_steering = 50
hasBullet = False
rotation = 3

#atualiza a posição do robô
def updatePos(coord, dire):
    temp = coord.copy()
    if(dire == "N"):
        temp[1] = temp[1] - 1;
    elif(dire == "S"):
        temp[1] = temp[1] + 1;
    elif(dire == "W"):
        temp[0] = temp[0] - 1;
    elif(dire == "E"):
        temp[0] = temp[0] + 1;
    else:
        print("Direction not defined!");
    return temp
    
    
#fecha a garra
def grab():
    global hasBullet
    hasBullet = True
    claw.on_for_degrees(SpeedPercent(100), 1000)
    claw.reset()

#abre a garra
def letGo():
    claw.on_for_degrees(SpeedPercent(75), -500)
    claw.reset()

#avanca
def moveForward(rotation):
    movementMotor.on_for_rotations(SpeedPercent(speed_moving), -rotation)
    movementMotor.reset()

#retrocede
def moveBackward(rotation):
    movementMotor.on_for_rotations(SpeedPercent(speed_moving), rotation)
    movementMotor.reset()

#muda a direção das rodas no sentido do relogio
def turnConClk(angle):
    steering.on_for_degrees(SpeedPercent(speed_steering), angle)

#muda a direção das rodas no sentido contrario ao relogio
def turnClock(angle):
    steering.on_for_degrees(SpeedPercent(speed_steering), -angle)

#posiciona o robo na direcao dada por newDirection
def changeDirection(newDirection):
    global angle
    rotation = 3
    if(newDirection == 'N'):
        #turn north
        moveForward(rotation + 0.8)
        turnClock(angle)
        moveBackward(rotation + 0.5)
        turnConClk(2*angle)
        moveForward(rotation + 0.5)
        turnClock(angle)
        moveBackward(rotation - 0.1)
    elif(newDirection == 'S'):
        #turn south
        print("South")
    elif(newDirection == 'W'):
        #turn west
        moveForward(rotation + 0.1)
        turnClock(angle)
        moveBackward(rotation + 0.2)
        turnConClk(angle)
        moveForward(0.5)
    elif(newDirection == 'E'):
        #turn east
        moveForward(rotation + 0.1)
        turnConClk(angle)
        moveBackward(rotation + 0.5)
        turnClock(angle)
        moveForward(0.8)
    else:
        print("Invalid direction. Valid directions are N, S, E or W")

#volta a apontar para o sul
def retInitialPos(currentO):
    if(currentO == 'N'):
        changeDirection('N')
    elif(currentO == 'W'):
        changeDirection('E')
    elif(currentO == 'E'):
        changeDirection('W')

#Ataque com machete
#apos reconhecer a posição do zombie
def macheteAttack(coord, dir):
	print('Manchete Attack dir: ', dir)
        #posicionar o robo em direcao ao zombie
	changeDirection(dir)
        #acelerar nessa direção ate bater o robo
	moveForward(rotation + 2)
	sound.play('str_st.wav')
	coord = updatePos(coord, dir)
	sleep(2)
	retInitialPos(dir)
	return coord

#Ataque com pistola (supõe que tem a bala)
#reconhecer a posição do zombie
def gunAttack(coord, dir):
	print('Gun Attack dir: ', dir)
	#posicionar o robo em direcao ao zombie
	changeDirection(dir)
        #acelarar nessa diração
	moveForward(rotation)

        #fazer o som do disparo
	sound.play('Gun_Shot-Marvin-1140816320.wav')
        #deixar cair a bala no chão
	letGo()
	retInitialPos(dir)
	coord = updatePos(coord, dir)
	return coord

#apanha a bala na direção escolhida
#retorna a sua nova posição 
def takeBullet(coord, dir):
	print('Take Bullet dir: ', dir)	
	changeDirection(dir)
	hasBullet = False
	while(not hasBullet):
		distance = ultrasonics.distance_centimeters
		print(distance)
		moveForward(0.55)
		if(distance < 16.6):
			hasBullet = True
	movementMotor.stop()
	if(hasBullet):
		grab()
		print("grab")
		sleep(2)
		claw.stop()
		retInitialPos(dir)
		coord = updatePos(coord, dir)
	return coord

#apanha a peça na direção escolhida
#retorna a sua nova posição
def takePart(coord,dir):
	print('Take Part dir: ', dir)
	changeDirection(dir)
	hasBullet = False
	while(not hasBullet):
		distance = ultrasonics.distance_centimeters
		print(distance)
		moveForward(0.55)
		if(distance < 17):
			hasBullet = True
	movementMotor.stop()
	if(hasBullet):
		grab()
		print("grab")
		sleep(2)
		claw.stop()
		retInitialPos(dir)
		coord = updatePos(coord, dir)
	return coord

#verifica o cheiro dos dois zombies
#retorna um array com o cheiro de cada um
def smell():
    smellZombie = [10,10]
    zombie1 = color()
    if(zombie1 == "blue"):
        smellZombie[0] = 1
    elif(zombie1 == "white"):
        smellZombie[0] = 2
    turnConClk(angle)
    moveForward(rotation - 1)
    sleep(0.5)
    zombie2 = color()
    if(zombie2 == "blue"):
        smellZombie[1] = 1
    elif(zombie2 == "white"):
        smellZombie[1] = 2
    sleep(0.5)
    moveBackward(rotation - 1)
    turnClock(angle)
	
    return smellZombie
