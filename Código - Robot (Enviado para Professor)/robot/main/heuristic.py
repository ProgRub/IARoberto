#!/usr/bin/env python3
import random

field = [] # variavel que contem a matriz do campo

#cria uma matriz 6x6 com todos os elementos aij = val
def initMatrix(val):
	global field
	field = []
	for i in range(6):
		row = []
		for j in range(6):
			row.append(val)
		field.append(row)

#retorna as posicoes dos zombies atordoados 
def koZombie(gameField):
        pos = []
        for i in range(6):
                for j in range(6):
                        if(gameField[i][j] == 'a'):
                                pos.append([j + 1, i + 1])
        return pos

#calcula a distancia mais curta entre os zombies atordoados e o robo
def zombieDistance(coord, koZombie):
        dist = 36
        for pos in koZombie:
                disZom = abs(coord[0] - pos[0]) + abs(coord[1] - pos[1])
                if(disZom < dist):
                        dist = disZom
        return dist

#calcula a heristica do ponto 'point'
#'obj' e o objetivo do movimento
#'coord' e a posicao atual
#'smellZombie' e o array com os cheiros dos zombies
#'twoMove' diz se a prioridade e o movimento de duas casas
def heuristic(coord, smellZombie, point, obj, gameField, twoMove):
        if(point != [0, 0]):
                koZom = koZombie(gameField)
                distZom = zombieDistance(coord, koZom)
                distObj = abs(point[0] - obj[0]) + abs(point[1] - obj[1])
                distOrg = abs(coord[0] - point[0]) + abs(coord[1] - point[1])
                if(twoMove):
                        return distObj
                elif(koZombie != []):
                        return distObj + 3*distOrg - distZom
                else:
                        return distObj + 2*distOrg
        else:
                print("Error point: outside of the board");

# escreve o valor 'value' na posicao dada por point da heuristica no filed
def writeHeur(point, value):
	global field
	field[point[1] - 1][point[0] - 1] = value

#calcula a heuristica de todas as casas onde o movimento e possivel
#e retorna o menor valor da heuristica
def decideNext(coord, smellZombie, obj, gameField, twoMove=False):
	point = [0, 0]
	heur = 20
	writeHeur(coord, "   H") #escreve no field a posição em que está
	writeHeur(obj, "   O") #escreve no field a posiçaõ objetivo
    
	if(coord[0] > 2): #coord x > 2
		point[0] = coord[0] - 2
		point[1] = coord[1]
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur): #se a nova heuristica for melhor 
			heur = nHeur #substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[0] > 1): #coord x > 1
		point[0] = coord[0] - 1
		point[1] = coord[1]
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur #substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[0] < 6): #x < 6
		point[0] = coord[0] + 1
		point[1] = coord[1]
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[0] < 5): #x < 5
		point[0] = coord[0] + 2
		point[1] = coord[1]
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[1] > 2): #y > 2
		point[0] = coord[0]
		point[1] = coord[1] - 2
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[1] > 1): #y > 1
		point[0] = coord[0]
		point[1] = coord[1] - 1
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[1] < 6): #y < 6 
		point[0] = coord[0]
		point[1] = coord[1] + 1
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[1] < 5): #y < 5
		point[0] = coord[0]
		point[1] = coord[1] + 2
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[0] > 1 and coord[1] > 1): #x > 1 e y > 1
		point[0] = coord[0] - 1
		point[1] = coord[1] - 1
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[0] > 1 and coord[1] < 6): #x > 1 e y < 6
		point[0] = coord[0] - 1
		point[1] = coord[1] + 1
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur
		writeHeur(point, nHeur)
	if(coord[0] < 6 and coord[1] > 1): #x < 6 e y > 1
		point[0] = coord[0] + 1
		point[1] = coord[1] - 1
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur)
	if(coord[0] < 6 and coord[1] < 6): #x < 6 e y < 6
		point[0] = coord[0] + 1
		point[1] = coord[1] + 1
		nHeur = heuristic(coord, smellZombie, point, obj, gameField, twoMove)
		if(nHeur < heur):#se a nova heuristica for melhor 
			heur = nHeur#substitui a melhor heristica
		writeHeur(point, nHeur) 
	return heur

#Escreve o tabuleito do jogo
def showField():
    for x in field:
        for y in x:
            print('{:4}'.format(y), end = " ", flush=True)
        print()

#retorna uma array com todas as posicoes com o valor 'val'
def posOpt(val):
    pos = []
    for i in range(len(field)):
        for j in range(len(field[0])):
            if(field[i][j] == val):
                pos.append([j+1, i+1])
    return pos

#Escreve a lista lst
def printList(lst):
    print('[%s]' % ', '.join(map(str, lst)))

#Escolhe e retorna um elemento aleatorio da lista lst
def chooseRand(lst):
    return random.choice(lst)
