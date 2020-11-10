#!/usr/bin/env python3

from colorSensor import color
from recon import recon
from movement import move, move2
from attack import letGo, updatePos ,takeBullet, takePart, macheteAttack, gunAttack, smell
from heuristic import initMatrix, decideNext, showField, posOpt, printList, chooseRand, zombieDistance, koZombie
from time import sleep
from ev3dev.ev3 import TouchSensor, Sound
from threading import Thread

sound = Sound()

coord = [1,1] #coordenada inicial do robo
bikeFixed = False # váriavel para saber se a mota está arranjada
hasBullet = False # variável boleana para saber se robo tem bala
hasPart = False # variável boleana para saber se robo tem peça
numParts = 0 #variável que guarda o numero de peças na mota
squareRecon = ["-","-","-","-"] #S E N array com o reconhecimento das casa em seu redor
smellZombie = ["-","-"] # cheiro de zombie dos dois zombies pode ser 1 ou 2 
squareAction = False # variável que permite saber se efetuou alguma ação tendo em conta os quadrados a seu redor
zombieSmell1 = False #tem pelo menos um zombie a 1 casa
zombieSmell2 = False #tem pelo menos um zombie a 2 casas
zombie1 = [] #guarda a posição do zombie 1
zombie2 = [] #guarda a posição do zombie 2
sleepZombie1 = [] #coordenada do zombie atordoado 
sleepZombie2 = [] #coordenada do zombie atordoado
sleepTime1 = 2 #numero de turnos que o zombie 1 fica atordoado
sleepTime2 = 2 #numero de turmos que o zombie 2 fica atordoado

gameField = [["v","-","-","-","-","-"]
			,["-","-","-","-","-","-"]
			,["-","-","-","-","-","-"]
			,["-","-","-","-","-","-"]
			,["-","-","-","-","-","-"]
			,["-","-","-","-","-","-"]] # matriz do campo de jogo com as casas já visitadas

twoMovement = False #Permite o movimento de duas casas (nao é utilizado devidoà probabilidade do robo perder ser maior)

obj = [2,1] #coordenada do objetivo inicial
#definição dos objetivos que permitem percorrer o campo de forma a minimizar os movimentos e maximizar a area visitada
obj1 = [2, 1] 
obj2 = [2, 6]
obj3 = [5, 6]
obj4 = [5, 1]

part = [] #coordenada de uma peça no campo 
bullet = [] #coordenada da bala no campo


#função que permite mostrar o campo de jogo
def showGameField():
    for x in gameField:
        for y in x:
            print('{:4}'.format(y), end = " ", flush=True)
        print()

#função que define o casa objetivo do robo
def defObj():
	global obj, part, bullet
	
	if(coord == part): #se tiver na coordenada da peça
		part = []
	
	if(coord == bullet): #se tiver as coordenadas da bala
		bullet =[]
	
	if(hasPart == True): #se tem peça vai em direção à mota
		obj = [6, 6]
	else:
		if(part != []): #se tiver a coordenada da peça move-se em direção a ela
			obj = part
		elif(bullet != []):#se tiver a coordenada da bala move-se em direça a ela
			obj = bullet
		elif(coord == [6,6]): #se tiver na casa [6,6] volta para o objetivo [5,6]
			obj = obj3
		elif(coord == obj1): # se tiver no obj1 move-se para o proximo objetivo
			obj = obj2 
		elif(coord == obj2): #se tiver no obj2 move-se para o proximo objetivo
			obj = obj3
		elif(coord == obj3): #se tiver no obj3 move-se para o próximo objetivo
			obj = obj4
		elif(coord == obj4): #se tiver no obj4 move-se para o próximo objetivo inicial
			obj == obj1
		
		elif(coord == part): #se estiver na coordenada da peça e não tem peça, move-se para o objetivo mais proximo
			if(coord[0] <= 3 and coord[1] <= 3):
				obj = obj1
			elif(coord[0] <= 3 and coord[1] >= 3):
				obj = obj2
			elif(coord[0] >= 3 and coord[1] >= 3):
				obj = obj3
			else:
				obj = obj4
		
		elif(coord == bullet): #se estiver na coordenada da bala e não tem bala, move-se para o objetivo mais proximo (supostamente isto nunca acontece)
			if(coord[0] <= 3 and coord[1] <= 3):
				obj = obj1
			elif(coord[0] <= 3 and coord[1] >= 3):
				obj = obj2
			elif(coord[0] >= 3 and coord[1] >= 3):
				obj = obj3
			else:
				obj = obj4
				
		else: #caso contrario segue o mesmo objetivo
			obj = obj
	
	return obj
	
#função que verifica se foi precionado o sensor de toque
def waitTouchSensor():
	ts = TouchSensor()
	
	print('\nPrecione o botao para incializar o turno...')
	while (not ts.value()): #enquanto não é precionado o sensor de toque
			
			if(hasPart): #se tiver peça soa o alarme
				Sound.tone(1000, 200)
				sleep(0.1)
			else:
				sleep(0.1)
				
#função que altera a posição do array 0,1,2,3 para S, E, N, W
def directionDef(numberDir):
	if(numberDir == 0):
		return "S"
	elif(numberDir == 1):
		return "E"
	elif(numberDir == 2):
		return "N"
	elif(numberDir == 3):
		return "W"
	else:
		return ""

#função que permite mover o robo uma casa na direção que se pretende e atualiza as coordenadas da posição do robo
def moveAction(dir):
	global coord
	
	coord = move(coord, dir) #movimenta o robo 

	#método que atualiza a matriz do campo (gameField) colocando a casa atual como verificada 
	if(gameField[coord[1]-1][coord[0]-1] == "-"):
		gameField[coord[1]-1][coord[0]-1] = "v"

#função que permite mover o robo duas casas consecutivas e atualiza as coordenadas da posição
def moveAction2 (dir1, dir2):
	global coord, bullet, part
	
	coord = move(coord, dir1) #movimenta uma casa
	
	moveSecond = move2(coord, dir2)#movimenta outra casa
	coord = moveSecond[0] #guarda a nova coordenada
	catch = moveSecond[1] #varável que permite saber se o robo ao entrar na segunda casa apanhou alguma peça ou bala
	
	if(catch == 'part'): #se apanhou peça atualiza a variável para true
		part = True
	
	if(catch == 'bullet'): #se apanhou bala atualiza a variável para true
		bullet = True
	
	#método que atualiza a variável gameField colocando a casa atual como verificada 
	if(gameField[coord[1]-1][coord[0]-1] == "-"):
		gameField[coord[1]-1][coord[0]-1] = "v"

#função que permite mover o robo dado umas coordenadas
def moveActionCoord (nxt):
	if(coord[0] +1 == nxt[0] and coord[1] == nxt[1]): #mover para (x+1,y)
		moveAction("E")
		
	if(coord[0] +2 == nxt[0] and coord[1] == nxt[1]): #mover para (x+2,y)
		moveAction2("E","E")
		
	if(coord[0] -1 == nxt[0] and coord[1] == nxt[1]): #mover para (x-1,y)
		moveAction("W")
	
	if(coord[0] -2 == nxt[0] and coord[1] == nxt[1]): #mover para (x-2,y)
		moveAction2("W","W")
	
	if(coord[0] == nxt[0] and coord[1] -1 == nxt[1]): #mover para (x,y-1)
		moveAction("N")
	
	if(coord[0] == nxt[0] and coord[1] -2 == nxt[1]): #mover para (x,y-2)
		moveAction2("N","N")

	if(coord[0] == nxt[0] and coord[1] +1 == nxt[1]): #mover para (x,y+1)
		moveAction("S")
		
	if(coord[0] == nxt[0] and coord[1] +2 == nxt[1]): #mover para (x,y+2)
		moveAction2("S","S")
	
	if(coord[0] +1 == nxt[0] and coord[1] +1 == nxt[1]): #mover para (x+1,y+1)
		moveAction2("E","S")
	
	if(coord[0] +1 == nxt[0] and coord[1] -1 == nxt[1]): #mover para (x+1,y-1)
		moveAction2("E","N")
				
	if(coord[0] -1 == nxt[0] and coord[1] +1 == nxt[1]): #mover para (x-1,y+1)
		moveAction2("W","S")
		
	if(coord[0] -1 == nxt[0] and coord[1] -1 == nxt[1]): #mover para (x-1,y-1)
		moveAction2("W","N")
	
#função que atualiza a variável gameField com os quadrados verificados pelo robo
def viewedSquares():
	if(squareRecon[0] != "-"): #S
		gameField[coord[1]-1][coord[0]-1] = "v"

	if(squareRecon[1] != "-"): #E
		gameField[coord[1]-1][coord[0]] = "v"

	if(squareRecon[2] != "-"): #N
		gameField[coord[1]-2][coord[0]-1] = "v"

	if(squareRecon[3] != "-"): #W
		gameField[coord[1]-1][coord[0]-2] = "v"

#função que executa o cheiro para receber informação sobre se existe zombies a 1 ou 2 casas
def smellAction():
	global smellZombie, zombieSmell1, zombieSmell2
	
	smellZombie = smell()

	#se existe zombie a 2 casas
	if((smellZombie[0] == 2 or smellZombie[1] == 2) and zombieDistance(coord, koZombie(gameField)) > 2):
		zombieSmell2 = True
	
	#se existe zombie a 1 casa
	if(smellZombie[0] == 1 or smellZombie[1] == 1):
			zombieSmell1 = True
		
#função que executa o reconhecimento e atualiza o array com a informação das casas a redor
def reconAction():
	global squareRecon, initialMovement, zombie1, zombie2, bullet, part
	
	squareRecon = recon(coord)
	
	#se existir zombies à sua volta guarda as suas coordenadas
	for x in range(len(squareRecon)):
		#altera os valores 0,1,2,3 para S,E,N,W
		dir = directionDef(x)
		
		if(squareRecon[x] == 'red' or squareRecon[x] == 'blue'): #se tiver zombie
			if (zombie1 == []): #guarda a posição do zombie1
				zombie1 = updatePos(coord, dir)
			else: #guarda a posição do zombie 2
				zombie2 = updatePos(coord, dir)
	
	#se existir peças às sua volta guarda as coordenadas
	for x in range(len(squareRecon)):
		#altera os valores 0,1,2,3 para S,E,N,W
		dir = directionDef(x)
		
		if(squareRecon[x] == 'green'): #se tiver peça e econtra peça
			part = updatePos(coord, dir)
	
	#se existir bala à sua volta guarda as coordenadas
	for x in range(len(squareRecon)):
		#altera os valores 0,1,2,3 para S,E,N,W
		dir = directionDef(x)
		
		if(squareRecon[x] == 'dark blue'): #se tiver peça e econtra bala 
			bullet = updatePos(coord, dir)
		
	viewedSquares() # atualiza na variável gameField os quadrados verificadas pelo robo


#função que faz a decisão da ação a fazer em conta as casas em seu redor
def decisionAction():
	global hasBullet, hasPart, coord, part, bullet, sleepZombie1, sleepZombie2, squareAction
	
	decision = True #variável que fica True até que seja efetuado uma ação

	#caso exista uma baça à sua volta
	if(decision == True):
		for x in range(len(squareRecon)):		
			#altera os valores 0,1,2,3 para S,E,N,W
			dir = directionDef(x)
			
			if(squareRecon[x] == 'dark blue'): #caso exista uma bala
				if(hasPart == True): #caso tenha uma peça
					bullet = updatePos(coord, dir) #guarda a posição da bala
					print('Save bullet coord: ', bullet)
					
				else:	
					#efetua o apanho da peça e atualiza a sua coordenada com a nova posição
					coord = takeBullet(coord, dir)
					bullet = []
					hasBullet = True
					decision = False
					squareAction = True
					break
    
	#caso exista um zombie à sua volta
	if(decision == True):
		for x in range(len(squareRecon)):
			#altera os valores 0,1,2,3 para S,E,N,W
			dir = directionDef(x)
		
			if (squareRecon[x] == 'red'): #caso existe zombie
				if(hasBullet == True): #se tiver bala
					#efetua o ataque e atualiza a sua coordenada com a nova posição
					coord = gunAttack(coord, dir)
					#já utlizou a bala e fica false
					hasBullet = False
					decision = False
					squareAction = True
					break
					
				else: #se não tiver bala
					#efetua o ataque e atualiza a sua coordenada com a nova posição
					coord = macheteAttack(coord, dir)
					gameField[coord[1]-1][coord[0]-1] = 'a' #escreve na posição em que o zombie foi atordoado
					if(sleepZombie1 == []):
						sleepZombie1 = coord
					else:
						sleepZombie2 = coord
					decision = False
					squareAction = True
					break
	
	#caso exista um zombie com peça à sua volta
	if(decision == True):
		for x in range(len(squareRecon)):
			#altera os valores 0,1,2,3 para S,E,N,W
			dir = directionDef(x)
			
			if(squareRecon[x] == 'blue'): #caso exista um zombie com peça
				
				if(hasPart == True): #caso já tenha uma peça
					coord = macheteAttack(coord, dir) #ataca o zombie
					gameField[coord[1]-1][coord[0]-1] = 'a' #escreve na posição em que o zombie foi atordoado
					if(sleepZombie1 == []):
						sleepZombie1 = coord
					else:
						sleepZombie2 = coord
					decision = False
					squareAction = True
					break
					
				else:
					if(hasBullet == True):#caso o robo tenha uma bala
						#efetua o ataque e atualiza a sua coordenada com a nova posição
						print('Gun Atack dir:' ,dir)
						sound.play('Gun_Shot-Marvin-1140816320.wav')
						letGo()
						sleep(5)#para tirarmos a bala da frente do robo
						#já utlizou a bala e fica false
						coord = takePart(coord, dir)
						part = []
						hasBullet = False
						decision = False
						hasPart = True
						squareAction = True
						break
						
					else:
						#efetua o apanho da peça e atualiza a sua coordenada com a nova posição
						print('Manchete Atack dir:' ,dir)
						coord = takePart(coord, dir)
						part = []
						sound.play('str_st.wav')
                                                
						gameField[coord[1]-1][coord[0]-1] = 'a' #escreve na posição em que o zombie foi atordoado
						if(sleepZombie1 == []):
							sleepZombie1 = coord
						else:
							sleepZombie2 = coord
						hasPart = True 
						decision = False
						squareAction = True
						break
	
	#caso exista uma peça à sua volta
	if(decision == True):
		for x in range(len(squareRecon)):
			#altera os valores 0,1,2,3 para S,E,N,W
			dir = directionDef(x)
			
			if(squareRecon[x] == 'green'): #caso exista uma peça
				if(hasPart == True): #caso já tenha uma peça
					part = updatePos(coord, dir) #guarda a posição da outra peça
					print('Save part coord: ', part)
				
				else:
					if(hasBullet == True):#caso o robo tenha uma bala
						bullet = updatePos(coord, dir) #guarda coordenada da bala
						print('Save bullet coord: ', bullet)
						letGo()
						sleep(3)#para tirarmos a bala da frente do robo
						hasBullet = False
						
					#efetua o apanho da peça e atualiza a sua coordenada com a nova posição
					coord = takePart(coord, dir)
					part = []
					hasPart = True 
					decision = False
					squareAction = True
					break
		
	decision = False # caso contrário se não existir nada à sua volta torna a variável false 

#função que permite mostrar no gameField a posição em que o zombie ficou atordoado
def zombieSleep():
	global sleepZombie1, sleepZombie2, sleepTime1, sleepTime2
	
	if(sleepZombie1 != []): #se o primeiro zombie está atordoado
		if(sleepTime1 == 2): #fica atordoado no primeiro turno
			sleepTime1 = 1
		else: #se for no segundo turno renicia as váriaveis para poder se movimentar no proximo
			sleepTime1 = 2
			gameField [sleepZombie1[1]-1][sleepZombie1[0]-1] = 'v' # apaga o 'a'
			sleepZombie1 = [] # apaga as coordenadas 
	
	if(sleepZombie2 != []): # se o segundo zombie está atordoado
		if(sleepTime2 == 2): #fica atordoado no primeiro turno
			sleepTime2 = 1
		else: #se for no segundo turno renicia as variaveis para poder se movimentar no proximo
			sleepTime2 = 2
			gameField [sleepZombie2[1]-1][sleepZombie2[0]-1] = 'v' #apaga o 'a'
			sleepZombie2 = [] # apaga as coordenadas
	

#inicio do jogo
while (not bikeFixed):
	
	#som para saber que o robo está pronto para o proximo turno
	Sound.beep()

	#espera que seja carregado o botão
	waitTouchSensor()

	print('\nTwo Movements: ', twoMovement)
	print('\nhasBullet:' ,hasBullet)
	print('hasPart: ',hasPart,'\n')
	print('part: ', part)
	print('bullet: ', bullet, '\n')
	print('coord: ', coord, '\n')
	
	#efetua a ação de cheiro
	print('Smell Zombies...')
	smellAction()
	print(smellZombie, '\n')
	
	sleep(3)

	#efetua a ação de reconhecimento
	print('Recon Squares...')
	reconAction()
	print(squareRecon)
	sleep(3)
	
	print('\nZombie1: ', zombie1)
	print('Zombie2: ', zombie2, '\n')
	
	
	if(not hasPart): #se não tiver a peça efeuta a função de decisão
		decisionAction()
		
	showGameField()
	print()
	
	
	if(squareAction == True or (zombieSmell2 == True and not hasPart)): #caso tenha efetuado uma ação ou cheiro de zombie a 2 não se movimenta mais neste turno
		squareAction = False
		zombieSmell = False
	
	#parte "intelegente" do robo
	else: #executa a heuristica caso tenha peça e cheiro do Zombies ou não tenha sido feito nenhuma ação  
    
		obj = defObj() #define objetivo qual casa deve ir
		print("Objetivo:")
		printList(obj)
		print("")
		initMatrix(20) #escreve 20 em todas as posições da matrix
		best = decideNext(coord, smellZombie, obj, gameField, twoMovement) #calcula a heuristica das casas posiveis
		showField()
		print("\nBest = ", best)
		opt = posOpt(best) #retorna uma array com as opções possiveis
		print("\nOpcoes: ")
		printList(opt)
		nxt = chooseRand(opt)
		print("\nNext: ")
		printList(nxt)
		
		if(zombie1 == nxt or zombie2 == nxt): # se exsitir zombie na direção em que se movimenta faz manchete atack
			print('Manchete Attack : ', nxt)
			
		moveActionCoord(nxt)
		
		if(zombie1 == nxt or zombie2 == nxt): #emite o som do ataque
			sound.play('str_st.wav')
			sleep(3)
		
	if(coord == [6,6] and hasPart == True): #se tiver a peça e estiver na coordenada [6,6]
		letGo() #larga a peça
		hasPart = False #deixa de ter a peça
		numParts = numParts + 1 #atualiza a varíavel do numero de peças
		print('Let go part...')
		print('Number of parts: ', numParts) 
	    
		if(numParts == 2): #se já tem duas peças
			bikeFixed = True
			print('VICTORYYYYYY')
		
	#renicia as variaveis das posições dos zombies
	zombie1 = []
	zombie2 = []
	
	zombieSleep() #verifica a situação dos zombies caso tenham sido atordoados

