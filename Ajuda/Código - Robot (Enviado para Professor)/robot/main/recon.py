#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_C, OUTPUT_B, OUTPUT_A, SpeedPercent
from ev3dev.ev3 import ColorSensor
from time import sleep
from colorSensor import color

#reconhecimento das casa em seu redor
#devolve um array com as cores respetivas lidas e casa verificadas
def recon(coord):
	x = coord[0]
	y = coord[1]
	#associação a variáveis o tipo de motor e a sua porta de OUTPUT
	l = LargeMotor(OUTPUT_B)
	l1 = LargeMotor(OUTPUT_C)
	m = MediumMotor(OUTPUT_A)

	square = ["-","-","-","-"]
	
	#variáveis para facilitar a alteração dos valores
	angle = 100
	speed_steering = 50
	speed_moving = 50

	if(x == 1 and y == 1): #(1,1)
		#verifica casa da frente(x+1,y)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3)
		sleep(0.5)
		square[0] = color()
		
		#verifica casa da esquerda(x+1,y)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.3)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		sleep(1.5)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.8)
		sleep(1.5)
		square[1] = color()
		
		#volta à mesma posição
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.6)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -0.8)
	
	elif(x == 1 and 1<y<6): #(1,1<y<6)
		
		#verifica casa da frente(x+1,y)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3)
		sleep(1.5)
		square[0] = color()
		
		#verifica casa de trás(x,y-1)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.3)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		sleep(1.5)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.3)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		sleep(1.5)
		square[2] = color()
		
		#verifica casa da esquerda(x,y+1)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.6)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		sleep(1.5)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.4)
		sleep(1.5)
		square[1] = color()
		
		#voltar à mesma posição
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.6)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		sleep(1.5)
		l1.on_for_rotations(SpeedPercent(speed_moving), -0.8)
		
	elif(x == 1 and y == 6): #(1,6)
		
		#verifica casa da esquerda (x+1,y)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.4)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		sleep(1.5)
		square[1] = color()
		
		
		#verifica casa de trás(x,y-1)
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.3)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.4)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -0.8)
		sleep(1.5)
		square[2] = color()
		
		#voltar à mesma posição
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.3)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), -2.8)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.5)
		
	elif(1<x<6 and y == 1): #(1<x<6,1)
		
		# verifica casa da frente (x,y+1)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3)
		sleep(1.5)
		square[0] = color()
		
		# verifica casa da direita (x+1,y)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.6)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		sleep(1.5)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.4)
		sleep(1.5)
		square[3] = color()
		
		#volta à posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 3)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		
		#verifica casa da esquerda (x-1,y)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.6)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		sleep(1.5)
		square[1] = color()
		
		#volta à posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.8)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
				
	elif(x == 6 and y == 1): #(6,1)
		
		#verifica casa da frente (x,y+1)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3)
		sleep(1.5)
		square[0] = color()
		
		#verifica da da direita (x,y-1)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.6)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.5)
		sleep(1.5)
		square[3] = color()
		
		#volta à posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering),  angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.4)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial	
		l1.on_for_rotations(SpeedPercent(speed_moving), -0.8)
				
	elif(x == 6 and 1<y<6): #(6,1<y<6)
		
		#verifica cada da frente (x,y+1)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3)
		sleep(1.5)
		square[0] = color()
		
		#verifica casa de trás (x,y-1)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.8)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.2)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -0.5)
		sleep(1.5)
		square[2] = color()
		
		#verifica casa à direita (x-1,y)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.6)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -4.4)
		sleep(1.5)
		square[3] = color()
		
		#volta à posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.6)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -1)
		
	elif(x == 6 and y == 6): #(6,6)
		
		#verifica casa de trás (x,y-1)
		l1.on_for_rotations(SpeedPercent(speed_moving), -3)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 3)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.2)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -0.2)
		sleep(1.5)
		square[2] = color()
		
		#verifica casa da direita (x-1,y)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.8)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -4.8)
		sleep(1.5)
		square[3] = color()
		
		#volta à posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.4)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -0.4)
		
		
	elif(1<x<6 and y == 6): #(1<x<6,y)
		
		#verifica casa à direita(x-1,y)
		l1.on_for_rotations(SpeedPercent(speed_moving), 1)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
		l1.on_for_rotations(SpeedPercent(speed_moving), -3.8)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		sleep(1.5)
		square[3] = color()
		
		#verifica casa de trás
		l.on_for_degrees(SpeedPercent(speed_steering),  -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 2.6)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -4.2)
		sleep(1.5)
		square[2] = color()
		
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 3)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -4.6)
		sleep(1.5)
		square[1] = color()
		
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#vira roda para a direita
		l1.on_for_rotations(SpeedPercent(speed_moving), 3)
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#posição inicial
		l1.on_for_rotations(SpeedPercent(speed_moving), -1.8)
		
	else: #reconhecimento dos 4 quadrados
		
		#verifica casa da frente
		l1.on_for_rotations(SpeedPercent(speed_moving), -3)
		sleep(1)
		square[0] = color()
		sleep(1)
		
		#verifica casa à esquerda
		
		#virar a roda para fazer a curva à direita
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
			
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.6)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		sleep(1)
		l1.on_for_rotations(SpeedPercent(speed_moving), -4)
		
		sleep(1)
		square[1] = color()
		sleep(1)
		
		#virar a roda para fazer a curva à direita
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
			
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.6)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		sleep(1)
		l1.on_for_rotations(SpeedPercent(speed_moving), -4)
		
		sleep(1)
		square[2] = color()
		sleep(1)
		
		#verifica casa à esquerda
		
		#virar a roda para fazer a curva à direita
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
			
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.6)
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		sleep(1)
		l1.on_for_rotations(SpeedPercent(speed_moving), -4)
		
		sleep(1)
		square[3] = color()
		sleep(1)
		
		
		#virar a roda para fazer a curva à direita
		l.on_for_degrees(SpeedPercent(speed_steering), angle)#vira roda para a esquerda
			
		l1.on_for_rotations(SpeedPercent(speed_moving), 3.8)
		#virar a roda para a posição inicial
		l.on_for_degrees(SpeedPercent(speed_steering), -angle)#posição inicial
		
		l1.on_for_rotations(SpeedPercent(speed_moving), -1.2)
	
	return (square)