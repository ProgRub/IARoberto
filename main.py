#!/usr/bin/env python3

from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.button import Button
import movement
import os
import sys
import time
os.system('setfont Lat15-TerminusBold14')

#TODO: guardar último quadrado visitado e verificar que não volta atrás, verificar se está num beco (só pode ir para um lado) e reorganizar a função moveTo
TAMANHO_TABULEIRO = 6
DIREITA = 1
ESQUERDA = -1
CIMA = TAMANHO_TABULEIRO
BAIXO = -TAMANHO_TABULEIRO
PAREDE = "2"
SEM_PAREDE = "1"
DESCONHECIDO = "0"
POS_NORTE = 0
POS_SUL = 2
POS_ESTE = 1
POS_OESTE = 3
POS_OVELHA = 4
NORTE = "N"
ESTE = "E"
OESTE = "W"
SUL = "S"
OVELHA = "1"
ROBOT_ORIENTACOES = NORTE + ESTE + SUL + OESTE
indexRobotOrientacoes = 0
indexRobot = 0
ultimoIndexRobot=-1
indexOvelha1=-1
indexOvelha2=-1
colorSensor = ColorSensor()
colorSensor.mode = 'COL-REFLECT'
colorSensor.calibrate_white()
sonic = UltrasonicSensor()
sonic.mode = UltrasonicSensor.MODE_US_DIST_CM
units = sonic.units


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


tabuleiro = []

"""
                    BOARD FUNCTIONS
"""
def fillStartingBoard():
    for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
        # Preencher cada posição do array. Vai ser uma string do genero "00000" e cada caracter da string diz respeito a ter ovelha, parede etc. No inicio não se sabe de nada dai começar com 00000
        tabuleiro.append(DESCONHECIDO*5)

    # Definir as bordas do tabuleiro
    # O index vai ter todas as posições de 0 a 35
    for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
        # Se o index for 0
        if (index % TAMANHO_TABULEIRO == 0):
            # Criar uma lista de strings em cada posição
            # passar string para lista para poder alterar carateres individuais
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_OESTE] = PAREDE  # Parede a oeste
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index >= TAMANHO_TABULEIRO*(TAMANHO_TABULEIRO-1)):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_NORTE] = PAREDE  # Parede a norte
            tabuleiro[index] = "".join(tabuleiro[index])
        if ((index - (TAMANHO_TABULEIRO-1)) % TAMANHO_TABULEIRO == 0):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_ESTE] = PAREDE  # Parede a este
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index < TAMANHO_TABULEIRO):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_SUL] = PAREDE  # Parede a sul
            tabuleiro[index] = "".join(tabuleiro[index])


# Função chamada no reconhecimento para atualizar os quadrados com os estados das paredes e das ovelhas
def updateBoard(foundWall: bool, foundSheep: bool):
    if indexRobotOrientacoes == POS_NORTE:  # Virado para norte
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_NORTE] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a norte
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + CIMA] = list(tabuleiro[indexRobot + CIMA])
        # A célula acima da atual do robot tem uma parede a sul
        tabuleiro[indexRobot +
                  CIMA][POS_SUL] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep and tabuleiro[indexRobot+CIMA][POS_OVELHA] != OVELHA:
            tabuleiro[indexRobot+CIMA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + CIMA] = "".join(tabuleiro[indexRobot + CIMA])
    elif indexRobotOrientacoes == POS_ESTE:  # Virado para este
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_ESTE] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a este
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot +
                  DIREITA] = list(tabuleiro[indexRobot +
                                            DIREITA])
        tabuleiro[
            indexRobot +
            DIREITA][POS_OESTE] = (PAREDE if foundWall else SEM_PAREDE)  # A célula à direita do robot tem uma parede a oeste
        if foundSheep and tabuleiro[indexRobot+DIREITA][POS_OVELHA] != OVELHA:
            tabuleiro[indexRobot+DIREITA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot +
                  DIREITA] = "".join(tabuleiro[indexRobot +
                                               DIREITA])
    elif indexRobotOrientacoes == POS_OESTE:  # Virado para oeste
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_OESTE] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a oeste
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot +
                  ESQUERDA] = list(tabuleiro[indexRobot + ESQUERDA])
        # A célula à esquerda do robot tem uma parede a este
        tabuleiro[indexRobot +
                  ESQUERDA][POS_ESTE] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep and tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] != OVELHA:
            tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + ESQUERDA] = "".join(tabuleiro[indexRobot +
                                                             ESQUERDA])
    else:  # Virado para sul
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_SUL] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a sul
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + BAIXO] = list(tabuleiro[indexRobot + BAIXO])
        # A célula acima da atual do robot tem uma parede a norte
        tabuleiro[indexRobot +
                  BAIXO][POS_NORTE] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep and tabuleiro[indexRobot+BAIXO][POS_OVELHA] != OVELHA:
            tabuleiro[indexRobot+BAIXO][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + BAIXO] = "".join(tabuleiro[indexRobot + BAIXO])


#Função que simplesmente imprime o tabuleiro para facilitar debugging
def printTabuleiro():
    aux = []
    toPrint = []
    for index in range(len(tabuleiro)):
        aux = list(tabuleiro[index])
        toPrint.append(str(index) + " N:" + aux[POS_NORTE] + " E:" + aux[POS_ESTE] +
                       " S:" + aux[POS_SUL] + " W:" + aux[POS_OESTE] + " Ovelha:" + aux[POS_OVELHA])
    debug_print("\n".join(toPrint))

"""
                    CHECKING FUNCTIONS
"""
# Função que verifica se existe parede ou ovelha a sua frente, para entao poder avancar na sua posicao atual


def canGoForward(orientacao):
    if orientacao == POS_NORTE:
        try:
            ovelhaFrente = list(tabuleiro[indexRobot + CIMA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == POS_ESTE:
        try:
            ovelhaFrente = list(tabuleiro[indexRobot+DIREITA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == POS_SUL:
        try:
            ovelhaFrente = list(tabuleiro[indexRobot+BAIXO])[4] == "1"
        except:
            ovelhaFrente = False
    else:
        try:
            ovelhaFrente = list(tabuleiro[indexRobot+ESQUERDA])[4] == "1"
        except:
            ovelhaFrente = False
    return not(list(tabuleiro[indexRobot])[orientacao] == PAREDE or ovelhaFrente)


def sheepCanGoForward(orientacao,indexOvelha):
    return not(list(tabuleiro[indexOvelha])[orientacao] == PAREDE)

def isBeco():
    global indexRobot
    return list(tabuleiro[indexRobot]).count(PAREDE)==3


# Função que obtém os lados que é necessário verificar na posição atual, isso é, ainda são DESCONHECIDAS do robot


def sidesToCheck():
    global indexRobot
    currentSquare = list(tabuleiro[indexRobot])
    sides = []
    for index in range(len(currentSquare) - 1):
        if currentSquare[index] == DESCONHECIDO:
            sides.append(index)
    return sides

# Função que verifica se tem parede à frente ou não


def checkFrontWall():
    movement.moveForwardForever()
    parede = False
    while True:
        # debug_print(colorSensor.rgb)
        try:
            # detetar azul claro (parede)
            if (colorSensor.rgb[0] < 70 and colorSensor.rgb[1] > 200 and colorSensor.rgb[2] > 200):
                parede = True
                break
            # detetar preto (não é parede)
            elif (colorSensor.rgb[0] < 80 and colorSensor.rgb[1] < 80 and colorSensor.rgb[2] < 80):
                break
        except:
            # detetar azul claro (parede)
            if (colorSensor.rgb[0] < 70 and colorSensor.rgb[1] > 200 and colorSensor.rgb[2] > 200):
                parede = True
                break
            # detetar preto (não é parede)
            elif (colorSensor.rgb[0] < 80 and colorSensor.rgb[1] < 80 and colorSensor.rgb[2] < 80):
                break
    movement.stopRobot()
    movement.backup()
    return parede

# Função que verifica se há uma ovelha à sua frente


def checkSheep():
    global sonic
    # debug_print("ULTRASONIC "+str(sonic.value()//10))
    if (sonic.value() // 10) > 15 and (sonic.value() // 10) < 40:
        movement.beep()
        return True
    return False

# Função que devolve para que lado o robot deverá ir e pode ir, para reconhecer o tabuleiro


def nextSquareToCheck(quadradosDesconhecidos,ultimosQuadrados):
    global indexRobot
    precisaVoltarAtras = False
    precisaIrEsquerda = False
    precisaIrDireita = False
    # Vê os quadrados nas fila imediatamente atrás do robot e verifica se ainda são desconhecidos
    for index in range(((indexRobot // TAMANHO_TABULEIRO) - 1) * TAMANHO_TABULEIRO, (indexRobot // TAMANHO_TABULEIRO) * TAMANHO_TABULEIRO):
        if index in quadradosDesconhecidos:
            precisaVoltarAtras = True
            break
    # Vê os quadrados à esquerda na fila que o robot se encontra e verifica se ainda são desconhecidos
    for index in range((indexRobot//TAMANHO_TABULEIRO)*TAMANHO_TABULEIRO, indexRobot):
        if index in quadradosDesconhecidos:
            precisaIrEsquerda = True
            break
    if (indexRobot+1) % 6 != 0:
        # Vê os quadrados à direita na fila que o robot se encontra e verifica se ainda são desconhecidos
        for index in range(indexRobot+1, ((indexRobot//TAMANHO_TABULEIRO)+1)*TAMANHO_TABULEIRO):
            if index in quadradosDesconhecidos:
                precisaIrDireita = True
                break
    debug_print(str(precisaVoltarAtras)+" " +
                str(precisaIrEsquerda)+" "+str(precisaIrDireita))
    if indexRobot % (TAMANHO_TABULEIRO * 2) <= 5:  # está nas linhas 0,2 ou 4
        if precisaVoltarAtras:
            if (indexRobot+BAIXO) in quadradosDesconhecidos and canGoForward(POS_SUL):
                return BAIXO
            else:
                if precisaIrDireita and (indexRobot + DIREITA) in quadradosDesconhecidos and canGoForward(POS_ESTE):
                    return DIREITA
                if precisaIrEsquerda and (indexRobot + ESQUERDA) in quadradosDesconhecidos and canGoForward(POS_OESTE):
                    return ESQUERDA
        else:
            if precisaIrEsquerda and (indexRobot + ESQUERDA) in quadradosDesconhecidos and canGoForward(POS_OESTE):
                return ESQUERDA
            if precisaIrDireita and (indexRobot + DIREITA) in quadradosDesconhecidos and canGoForward(POS_ESTE):
                return DIREITA
        if canGoForward(POS_NORTE) and ultimosQuadrados[0]!=indexRobot+CIMA:
            return CIMA
        if canGoForward(POS_ESTE) and ultimosQuadrados[0]!=indexRobot+DIREITA:
            return DIREITA
        if canGoForward(POS_OESTE) and ultimosQuadrados[0]!=indexRobot+ESQUERDA:
            return ESQUERDA
        if canGoForward(POS_SUL) and ultimosQuadrados[0]!=indexRobot+BAIXO:
            return BAIXO
    else:  # está nas linhas 1, 3 ou 4
        # debug_print("LINHA_IMPAR")
        if precisaVoltarAtras:
            if (indexRobot + BAIXO) in quadradosDesconhecidos and canGoForward(POS_SUL):
                return BAIXO
            else:
                if precisaIrEsquerda and (indexRobot + ESQUERDA) in quadradosDesconhecidos and canGoForward(POS_OESTE):
                    return ESQUERDA
                if precisaIrDireita and (indexRobot + DIREITA) in quadradosDesconhecidos and canGoForward(POS_ESTE):
                    return DIREITA
        else:
            if precisaIrDireita and (indexRobot + DIREITA) in quadradosDesconhecidos and canGoForward(POS_ESTE):
                return DIREITA
            if precisaIrEsquerda and (indexRobot + ESQUERDA) in quadradosDesconhecidos and canGoForward(POS_OESTE):
                return ESQUERDA
        if canGoForward(POS_NORTE) and ultimosQuadrados[0]!=indexRobot+CIMA:
            return CIMA
        if canGoForward(POS_ESTE) and ultimosQuadrados[0]!=indexRobot+DIREITA:
            return DIREITA
        if canGoForward(POS_OESTE) and ultimosQuadrados[0]!=indexRobot+ESQUERDA:
            return ESQUERDA
        if canGoForward(POS_SUL) and ultimosQuadrados[0]!=indexRobot+BAIXO:
            return BAIXO


#Função que remove da lista de quadrados desconhecidos todos os quadrados cujo robot já conhece o estado de todos os lados, se tem parede ou não
def removeKnownSquares(quadradosDesconhecidos):
    for index in range(len(tabuleiro)):
        if (DESCONHECIDO not in list(tabuleiro[index])[:4]):
            try:
                quadradosDesconhecidos.remove(index)
            except:
                pass
"""
                    MOVEMENT FUNCTIONS
"""
# Função que vira o robot para a direita e atualiza a orientação do robot


def turnRight():
    global indexRobotOrientacoes
    movement.turnRight()
    indexRobotOrientacoes = (indexRobotOrientacoes+1) % 4

# Função que vira o robot para trás e atualiza a orientação do robot
def turn180():
    global indexRobotOrientacoes
    movement.do180()
    indexRobotOrientacoes = (indexRobotOrientacoes+2) % 4

# Função que vira o robot para a esquerda e atualiza a orientação do robot


def turnLeft():
    global indexRobotOrientacoes
    movement.turnLeft()
    indexRobotOrientacoes = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1

# Função que movimenta o robot um quadrado para a frente e atualiza indexRobot(varivel global da posicao atual do robot) que é a posicao para que vai se mover no tabuleiro


def goForward():
    global indexRobot, indexRobotOrientacoes
    if indexRobotOrientacoes == POS_NORTE:
        indexRobot += CIMA
    elif indexRobotOrientacoes == POS_ESTE:
        indexRobot += DIREITA
    elif indexRobotOrientacoes == POS_SUL:
        indexRobot += BAIXO
    else:
        indexRobot += ESQUERDA
    movement.forwardOneSquare()


def sheepMove(indexRobot,indexOvelha):
    if indexRobot+DIREITA==indexOvelha:
        if sheepCanGoForward(POS_ESTE,indexOvelha):
            indexOvelha+=DIREITA
        elif sheepCanGoForward(POS_SUL,indexOvelha):
            indexOvelha+=BAIXO
        elif sheepCanGoForward(POS_OESTE,indexOvelha):
            indexOvelha+=ESQUERDA
        else:
            indexOvelha+=CIMA
    elif indexRobot+BAIXO==indexOvelha:
        if sheepCanGoForward(POS_SUL,indexOvelha):
            indexOvelha+=BAIXO
        elif sheepCanGoForward(POS_OESTE,indexOvelha):
            indexOvelha+=ESQUERDA
        elif sheepCanGoForward(POS_NORTE,indexOvelha):
            indexOvelha+=CIMA
        else:
            indexOvelha+=DIREITA
    elif indexRobot+ESQUERDA==indexOvelha:
        if sheepCanGoForward(POS_OESTE,indexOvelha):
            indexOvelha+=ESQUERDA
        elif sheepCanGoForward(POS_NORTE,indexOvelha):
            indexOvelha+=CIMA
        elif sheepCanGoForward(POS_ESTE,indexOvelha):
            indexOvelha+=DIREITA
        else:
            indexOvelha+=BAIXO
    else:
        if sheepCanGoForward(POS_NORTE,indexOvelha):
            indexOvelha+=CIMA
        elif sheepCanGoForward(POS_ESTE,indexOvelha):
            indexOvelha+=DIREITA
        elif sheepCanGoForward(POS_SUL,indexOvelha):
            indexOvelha+=BAIXO
        else:
            indexOvelha+=ESQUERDA

def calculateSheepMovement(tipoAcao, indexOvelha):
    global tabuleiro, indexRobot
    ultimoIndexOvelha=indexOvelha
    if tipoAcao=="S":#S de scream,grito
        sheepMove(indexRobot,indexOvelha)
    else: #tocou na ovelha
        movimentos=0
        while movimentos<2:
            sheepMove(indexRobot,indexOvelha)
            movimentos+=1
    aux=list(tabuleiro[ultimoIndexOvelha])
    aux[4]=int(aux[4])-1
    tabuleiro[ultimoIndexOvelha]="".join(aux)
    aux=list(tabuleiro[indexOvelha])
    aux[4]=int(aux[4])+1
    tabuleiro[indexOvelha]="".join(aux)

def moveTo(indexDestino):
    global indexRobot,tabuleiro,ultimoIndexRobot
    orientacaoDestino=-1
    hasMove=False
    while indexRobot!=indexDestino:
        if isBeco():
            if canGoForward(POS_OESTE):
                orientacaoDestino= POS_OESTE
            elif canGoForward(POS_ESTE):
                orientacaoDestino= POS_ESTE
            elif canGoForward(POS_SUL):
                orientacaoDestino= POS_SUL
            else:
                orientacaoDestino= POS_NORTE
        else:
            if indexDestino%TAMANHO_TABULEIRO<indexRobot%TAMANHO_TABULEIRO:
                if canGoForward(POS_OESTE) and indexRobot!=(ultimoIndexRobot+ESQUERDA):
                    orientacaoDestino= POS_OESTE
                    hasMove=True
                elif canGoForward(POS_ESTE) and indexRobot!=(ultimoIndexRobot+DIREITA):
                    orientacaoDestino= POS_ESTE
                    hasMove=True
            if indexDestino%TAMANHO_TABULEIRO>indexRobot%TAMANHO_TABULEIRO and not hasMove:
                if canGoForward(POS_ESTE) and indexRobot!=(ultimoIndexRobot+DIREITA):
                    orientacaoDestino= POS_ESTE
                    hasMove=True
                elif canGoForward(POS_OESTE) and indexRobot!=(ultimoIndexRobot+ESQUERDA):
                    orientacaoDestino= POS_OESTE
                    hasMove=True
            if indexRobot//TAMANHO_TABULEIRO>indexDestino//TAMANHO_TABULEIRO and not hasMove:
                if canGoForward(POS_SUL) and indexRobot!=(ultimoIndexRobot+BAIXO):
                    orientacaoDestino= POS_SUL
                    hasMove=True
            if indexRobot//TAMANHO_TABULEIRO<indexDestino//TAMANHO_TABULEIRO and not hasMove:
                if canGoForward(POS_NORTE) and indexRobot!=(ultimoIndexRobot+CIMA):
                    orientacaoDestino= POS_NORTE
        numeroRotacoes=0
        ultimoIndexRobot=indexRobot
        while numeroRotacoes<4:
            if indexRobotOrientacoes == orientacaoDestino and canGoForward(indexRobotOrientacoes):
                break
            indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
            if(list(tabuleiro[indexRobot])[indexToLeft] == SEM_PAREDE and indexToLeft == orientacaoDestino):
                turnLeft()
            elif(orientacaoDestino%2==indexRobotOrientacoes%2):
                turn180()
            else:
                turnRight()
            numeroRotacoes+=1
        goForward()



"""
                    BOARD RECON FUNCTION
"""
#Função que trata do reconhecimento inicial do tabuleiro
def recon():
    global indexRobot, indexRobotOrientacoes
    numeroParedes = 0
    numeroOvelhas = 0
    indexRobot = 0
    quadradosDesconhecidos = list(range(len(tabuleiro)))
    ultimosQuadrados=[-1,-1,-1,-1]
    indexOvelha1=-1
    indexOvelha2=-1
    while True:
        # printTabuleiro()
        # debug_print(quadradosDesconhecidos)
        ladosVerificar = sidesToCheck()
        if indexRobotOrientacoes in ladosVerificar:
            aux = ladosVerificar[0]
            auxIndex = ladosVerificar.index(indexRobotOrientacoes)
            ladosVerificar[0] = indexRobotOrientacoes
            ladosVerificar[auxIndex] = aux
            # ladosVerificar=ladosVerificar[0]+ladosVerificar[1:].sort()
        # debug_print(indexRobot)
        # debug_print(ladosVerificar)
        for lado in ladosVerificar:
            while (indexRobotOrientacoes != lado):
                indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
                if(indexToLeft == lado):
                    turnLeft()
                elif(lado%2==indexRobotOrientacoes%2):
                    turn180()
                else:
                    turnRight()
            ovelha = checkSheep()
            parede = checkFrontWall()
            if not ovelha:
                ovelha = checkSheep()
            if parede:
                numeroParedes += 1
            updateBoard(parede, ovelha)
        removeKnownSquares(quadradosDesconhecidos)
        numeroOvelhas = 0
        indexOvelha1 = -1
        indexOvelha2 = -1
        for index in range(len(tabuleiro)):  # Contar ovelhas
            aux = list(tabuleiro[index])
            if aux[4] == "1":
                numeroOvelhas += 1
                if indexOvelha1 == -1:
                    indexOvelha1 = index
                else:
                    indexOvelha2 = index
        if (numeroParedes == 6 and numeroOvelhas==2) or len(quadradosDesconhecidos) == 0 or (numeroOvelhas == 2 and len(quadradosDesconhecidos) == 2 and ((indexOvelha1+DIREITA) == indexOvelha2 or (indexOvelha1+ESQUERDA) == indexOvelha2 or (indexOvelha1+CIMA) == indexOvelha2 or (indexOvelha1+BAIXO) == indexOvelha2)):
            break
        direcao = nextSquareToCheck(quadradosDesconhecidos,ultimosQuadrados)
        debug_print(direcao)
        moveTo(indexRobot+direcao)
        # debug_print(str(numeroParedes)+" "+str(numeroOvelhas))
        # orientacao = indexRobotOrientacoes
        # if proximoIndex == BAIXO:
        #     orientacao = POS_SUL
        # elif proximoIndex == DIREITA:
        #     orientacao = POS_ESTE
        # elif proximoIndex == ESQUERDA:
        #     orientacao = POS_OESTE
        # else:
        #     orientacao = POS_NORTE
        # numeroRotacoes=0
        # while numeroRotacoes<4:
        #     if indexRobotOrientacoes == orientacao and canGoForward(indexRobotOrientacoes):
        #         break
        #     indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
        #     if(list(tabuleiro[indexRobot])[indexToLeft] == SEM_PAREDE and indexToLeft == orientacao):
        #         turnLeft()
        #     else:
        #         turnRight()
        #     numeroRotacoes+=1
        ultimosQuadrados=[indexRobot]+ultimosQuadrados[1:]
        # ultimosQuadrados[indexUltimosQuadrados]=indexRobot
        # indexUltimosQuadrados=(indexUltimosQuadrados+1)%4
        # if numeroRotacoes!=4:
        #     goForward()
        # debug_print(str(ultimosQuadrados))
        # if numeroRotacoes==4 or (ultimosQuadrados[0]==ultimosQuadrados[2] and ultimosQuadrados[1]==ultimosQuadrados[3]):
        #     break
    debug_print(quadradosDesconhecidos)
    if numeroParedes == 6:
        for quadrado in quadradosDesconhecidos:
            auxList = list(tabuleiro[quadrado])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = SEM_PAREDE
            tabuleiro[quadrado] = "".join(auxList)
        numeroOvelhas = 0
        for index in range(len(tabuleiro)):  # Contar ovelhas
            aux = list(tabuleiro[index])
            if aux[4] == "1":
                numeroOvelhas += 1
                if indexOvelha1 == -1:
                    indexOvelha1 = index
                else:
                    indexOvelha2 = index
        if numeroOvelhas==1:
            aux = list(tabuleiro[indexOvelha1])
            aux[4]="2"
            tabuleiro[indexOvelha1]="".join(aux)
    else:
        for quadrado in quadradosDesconhecidos:
            auxList = list(tabuleiro[quadrado])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = PAREDE
            tabuleiro[quadrado] = "".join(auxList)
    printTabuleiro()


# movement.backup()
# movement.scream()
fillStartingBoard()
recon()
moveTo(15)
# movement.turnLeft()
# time.sleep(1)
# movement.turnRight()
# movement.touchSheep()
# while True:
#     checkSheep()
