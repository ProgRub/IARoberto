#!/usr/bin/env python3

from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
import movement
import os
import sys
import time
os.system('setfont Lat15-TerminusBold14')

TAMANHO_LINHA_TABULEIRO = 6
DIREITA = 1
ESQUERDA = -1
CIMA = TAMANHO_LINHA_TABULEIRO
BAIXO = -TAMANHO_LINHA_TABULEIRO
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
ultimoIndexRobot = -15
indexOvelha1 = -15
indexOvelha2 = -15
colorSensor = ColorSensor()
colorSensor.mode = 'COL-REFLECT'
colorSensor.calibrate_white()
sonic = UltrasonicSensor()
sonic.mode = UltrasonicSensor.MODE_US_DIST_CM
units = sonic.units
numeroParedes = 0
numeroMovimentosRobot=2


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


tabuleiro = []
quadradosDesconhecidos = list(
    range(TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO))

"""
                    BOARD FUNCTIONS
"""


def fillStartingBoard():
    for index in range(TAMANHO_LINHA_TABULEIRO * TAMANHO_LINHA_TABULEIRO):
        # Preencher cada posição do array. Vai ser uma string do genero "00000" e cada caracter da string diz respeito a ter ovelha, parede etc. No inicio não se sabe de nada dai começar com 00000
        tabuleiro.append(DESCONHECIDO*5)

    # Definir as bordas do tabuleiro
    # O index vai ter todas as posições de 0 a 35
    for index in range(TAMANHO_LINHA_TABULEIRO * TAMANHO_LINHA_TABULEIRO):
        # Se o index for 0
        if (index % TAMANHO_LINHA_TABULEIRO == 0):
            # Criar uma lista de strings em cada posição
            # passar string para lista para poder alterar carateres individuais
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_OESTE] = PAREDE  # Parede a oeste
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index >= TAMANHO_LINHA_TABULEIRO*(TAMANHO_LINHA_TABULEIRO-1)):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_NORTE] = PAREDE  # Parede a norte
            tabuleiro[index] = "".join(tabuleiro[index])
        if ((index - (TAMANHO_LINHA_TABULEIRO-1)) % TAMANHO_LINHA_TABULEIRO == 0):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_ESTE] = PAREDE  # Parede a este
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index < TAMANHO_LINHA_TABULEIRO):
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


# Função que simplesmente imprime o tabuleiro para facilitar debugging
def printTabuleiro():
    aux = []
    toPrint = []
    for index in range(len(tabuleiro)):
        aux = list(tabuleiro[index])
        toPrint.append(str(index) + " N:" + aux[POS_NORTE] + " E:" + aux[POS_ESTE] +
                       " S:" + aux[POS_SUL] + " W:" + aux[POS_OESTE] + " Ovelha:" + aux[POS_OVELHA])
    debug_print("\n".join(toPrint))

# Função que remove da lista de quadrados desconhecidos todos os quadrados cujo robot já conhece o estado de todos os lados, se tem parede ou não


def removeKnownSquares():
    global quadradosDesconhecidos
    for index in range(len(tabuleiro)):
        if (DESCONHECIDO not in list(tabuleiro[index])[:4]):
            try:
                quadradosDesconhecidos.remove(index)
            except:
                pass


"""
                    CHECKING FUNCTIONS
"""
# Função que verifica se existe parede ou ovelha a sua frente, para entao poder avancar na sua posicao atual


def canGoForward(orientacao, index):
    if orientacao == POS_NORTE:
        try:
            ovelhaFrente = list(tabuleiro[index + CIMA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == POS_ESTE:
        try:
            ovelhaFrente = list(tabuleiro[index+DIREITA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == POS_SUL:
        try:
            ovelhaFrente = list(tabuleiro[index+BAIXO])[4] == "1"
        except:
            ovelhaFrente = False
    else:
        try:
            ovelhaFrente = list(tabuleiro[index+ESQUERDA])[4] == "1"
        except:
            ovelhaFrente = False
    return not(list(tabuleiro[index])[orientacao] == PAREDE or ovelhaFrente)


def sheepCanGoForward(orientacao, indexOvelha):
    return not(list(tabuleiro[indexOvelha])[orientacao] == PAREDE)


def isBeco():
    global indexRobot
    return list(tabuleiro[indexRobot]).count(PAREDE) == 3


# Função que obtém os lados que é necessário verificar na posição atual, isso é, ainda são DESCONHECIDAS do robot


def sidesToCheck():
    global indexRobot
    currentSquare = list(tabuleiro[indexRobot])
    sides = []
    for index in range(len(currentSquare) - 1):
        if currentSquare[index] == DESCONHECIDO:
            sides.append(index)
    return sides


def checkSides():
    global indexRobot, indexRobotOrientacoes, quadradosDesconhecidos, numeroParedes
    ladosVerificar = sidesToCheck()
    if indexRobotOrientacoes in ladosVerificar:
        aux = ladosVerificar[0]
        auxIndex = ladosVerificar.index(indexRobotOrientacoes)
        ladosVerificar[0] = indexRobotOrientacoes
        ladosVerificar[auxIndex] = aux
        # ladosVerificar=ladosVerificar[0]+ladosVerificar[1:].sort()
    # debug_print(indexRobot)
    # debug_print(ladosVerificar)
    parede = False
    for lado in ladosVerificar:
        while (indexRobotOrientacoes != lado):
            indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
            if(indexToLeft == lado):
                turnLeft()
            elif(lado % 2 == indexRobotOrientacoes % 2):
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
    removeKnownSquares()
    return parede
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

# def checkRowInUnknownSquares(quadradosDesconhecidos):
#     global indexRobot
#     for index in range((indexRobot)//TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO,((indexRobot)//TAMANHO_LINHA_TABULEIRO+1)*TAMANHO_LINHA_TABULEIRO):
#         if index in quadradosDesconhecidos:
#             return True
#     return False


def nextSquareToCheck():
    global indexRobot, tabuleiro, quadradosDesconhecidos
    # precisaVoltarAtras = False
    precisaIrEsquerda = False
    precisaIrDireita = False
    # for index in range(((indexRobot // TAMANHO_LINHA_TABULEIRO) - 1) * TAMANHO_LINHA_TABULEIRO, (indexRobot // TAMANHO_LINHA_TABULEIRO) * TAMANHO_LINHA_TABULEIRO):
    #     if index in quadradosDesconhecidos:
    #         precisaVoltarAtras = True
    #         break
    # debug_print(range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, indexRobot))
    for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, indexRobot):
        if index in quadradosDesconhecidos:
            precisaIrEsquerda = True
            break
    # debug_print(range(indexRobot+1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO))
    if (indexRobot+1) % 6 != 0:
        for index in range(indexRobot+1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
            if index in quadradosDesconhecidos:
                precisaIrDireita = True
                break
    if indexRobot % (TAMANHO_LINHA_TABULEIRO * 2) <= 5:  # está nas linhas 0,2 ou 4
        # if precisaVoltarAtras:
        # if (indexRobot + BAIXO) in quadradosDesconhecidos and canGoForward(POS_SUL):
        #     return BAIXO
        # else:
        if precisaIrDireita:
            for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
                debug_print(str(index)+": "+str(canGoForward(POS_ESTE, index+ESQUERDA))+" " + str(
                    canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_ESTE, index+ESQUERDA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        if precisaIrEsquerda:
            # debug_print(range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1))
            for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1):
                debug_print(str(index)+": "+str(canGoForward(POS_OESTE, index+DIREITA))+" " + str(
                    canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_OESTE, index+DIREITA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        # else:
        # if precisaIrEsquerda and canGoForward(POS_OESTE):
        #     return ESQUERDA
        # if precisaIrDireita and canGoForward(POS_ESTE):
        #     return DIREITA
        if canGoForward(POS_NORTE, indexRobot):
            return indexRobot+CIMA
        for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO-1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, -1):
            debug_print(str(index)+": "+str(canGoForward(POS_OESTE, index+DIREITA))+" " + str(
                canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
            if index in quadradosDesconhecidos and canGoForward(POS_NORTE, index+BAIXO):
                return index
        # if (indexRobot+DIREITA) in quadradosDesconhecidos and indexRobot%6!=5:
        #     return indexRobot+DIREITA
        # elif (indexRobot+CIMA) in quadradosDesconhecidos and indexRobot%6==5:
        #     return indexRobot+CIMA
        # for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
        #     if index in quadradosDesconhecidos and list(tabuleiro[index])[4]!=OVELHA and canGoForward(POS_ESTE,index+DIREITA):
        #         return index
        # for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO-1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, -1):
        #     if index in quadradosDesconhecidos and canGoForward(POS_NORTE, index+BAIXO):
        #         return index
        # for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+3)*TAMANHO_LINHA_TABULEIRO):
        #     if index in quadradosDesconhecidos and list(tabuleiro[index])[4]!=OVELHA and canGoForward(POS_ESTE,index+DIREITA):
        #         return index
    else:
        if precisaIrEsquerda:
            for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1):
                debug_print(str(index)+": "+str(canGoForward(POS_OESTE, index+DIREITA))+" " + str(
                    canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_OESTE, index+DIREITA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        if precisaIrDireita:
            for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
                debug_print(str(index)+": "+str(canGoForward(POS_ESTE, index+ESQUERDA))+" " + str(
                    canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_ESTE, index+ESQUERDA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        if canGoForward(POS_NORTE, indexRobot):
            return indexRobot+CIMA
        for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO):
            debug_print(str(index)+": "+str(canGoForward(POS_ESTE, index+ESQUERDA))+" " + str(
                canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
            if index in quadradosDesconhecidos and canGoForward(POS_NORTE, index+BAIXO):
                return index
        # if precisaVoltarAtras:
        # if (indexRobot + BAIXO) in quadradosDesconhecidos and canGoForward(POS_SUL):
        #     return BAIXO
        # else:
        #     debug_print(canGoForward(POS_ESTE))
        #     debug_print(canGoForward(POS_OESTE))
        #     if precisaIrDireita and canGoForward(POS_ESTE):
        #         return DIREITA
        #     if precisaIrEsquerda and canGoForward(POS_OESTE):
        #         return ESQUERDA
        # # else:
        # if precisaIrDireita and canGoForward(POS_ESTE):
        #     return DIREITA
        # if precisaIrEsquerda and canGoForward(POS_OESTE):
        #     return ESQUERDA
        # return CIMA
        # if (indexRobot+ESQUERDA) in quadradosDesconhecidos and indexRobot%6!=0:
        #     return indexRobot+ESQUERDA
        # elif (indexRobot+CIMA) in quadradosDesconhecidos and indexRobot%6==0:
        #     return indexRobot+CIMA
        # for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1):
        #     if index in quadradosDesconhecidos and list(tabuleiro[index])[4]!=OVELHA and canGoForward(POS_OESTE,index+ESQUERDA):
        #         return index
        # for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO):
        #     if index in quadradosDesconhecidos and canGoForward(POS_NORTE, index+BAIXO):
        #         return index
        # for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+3)*TAMANHO_LINHA_TABULEIRO-1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO-1, -1):
        #     if index in quadradosDesconhecidos and list(tabuleiro[index])[4]!=OVELHA and canGoForward(POS_OESTE,index+ESQUERDA):
        #         return index


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


def checkRowInUnknownSquares():
    global indexRobot, quadradosDesconhecidos
    for index in range((indexRobot)//TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO, ((indexRobot)//TAMANHO_LINHA_TABULEIRO+1)*TAMANHO_LINHA_TABULEIRO):
        if index in quadradosDesconhecidos:
            return True
    return False


def moveTo(indexDestino, paraRecon, numeroOvelhas):
    global indexRobot, tabuleiro, ultimoIndexRobot, quadradosDesconhecidos, numeroParedes
    orientacaoDestino = -1
    # debug_print("Index Destino:"+str(indexDestino))
    # debug_print("Index Robot:"+str(indexRobot))
    # debug_print(isBeco())
    # debug_print("Ultimo Index Robot:"+str(ultimoIndexRobot))
    percurso = []
    indexDestinoIntermediario = indexDestino
    percursoPeloAEstrela = False
    haParede = False
    if paraRecon:
        while indexRobot != indexDestino:
            if ((indexRobot+DIREITA) == indexDestino or (indexRobot+ESQUERDA) == indexDestino or (indexRobot+CIMA) == indexDestino or (indexRobot+BAIXO) == indexDestino) or len(percurso) > 1:
                hasMove = False
                if len(percurso) > 0:
                    indexDestinoIntermediario = percurso.pop(0)
                    debug_print(indexDestinoIntermediario)
                else:
                    percursoPeloAEstrela = False
                if indexRobot in quadradosDesconhecidos:
                    haParede = checkSides()
                debug_print("MOVETO " + str(haParede) +
                            " " + str(percursoPeloAEstrela))
                if haParede and percursoPeloAEstrela:
                    debug_print("RECALCULAR")
                    percurso = []
                debug_print("Ovelhas e Paredes " +
                            str(numeroParedes)+" "+str(numeroOvelhas))
                if paraRecon and ((numeroParedes == 6 and numeroOvelhas == 2) or len(quadradosDesconhecidos) == 0 or (len(quadradosDesconhecidos) == 2 and not ((indexOvelha1+DIREITA) == indexOvelha2 or (indexOvelha1+ESQUERDA) == indexOvelha2 or (indexOvelha1+CIMA) == indexOvelha2 or (indexOvelha1+BAIXO) == indexOvelha2))):
                    return True
                if haParede and percursoPeloAEstrela:
                    debug_print("RECALCULAR")
                    percurso = AEstrela(indexRobot,indexDestino)
                haParede = False
                if indexDestinoIntermediario % TAMANHO_LINHA_TABULEIRO < indexRobot % TAMANHO_LINHA_TABULEIRO:
                    if canGoForward(POS_OESTE, indexRobot):
                        orientacaoDestino = POS_OESTE
                        hasMove = True
                if indexDestinoIntermediario % TAMANHO_LINHA_TABULEIRO > indexRobot % TAMANHO_LINHA_TABULEIRO and not hasMove:
                    if canGoForward(POS_ESTE, indexRobot):
                        orientacaoDestino = POS_ESTE
                        hasMove = True
                if indexRobot//TAMANHO_LINHA_TABULEIRO < indexDestinoIntermediario//TAMANHO_LINHA_TABULEIRO and not hasMove:
                    if canGoForward(POS_NORTE, indexRobot):
                        orientacaoDestino = POS_NORTE
                        hasMove = True
                if indexRobot//TAMANHO_LINHA_TABULEIRO > indexDestinoIntermediario//TAMANHO_LINHA_TABULEIRO and not hasMove:
                    if canGoForward(POS_SUL, indexRobot):
                        orientacaoDestino = POS_SUL
                        hasMove = True
                if not hasMove:
                    percursoPeloAEstrela = True
                    percurso = AEstrela(indexRobot,indexDestino)
                    continue
                numeroRotacoes = 0
                ultimoIndexRobot = indexRobot
                debug_print("OrientacaoDestino:"+str(orientacaoDestino))
                while numeroRotacoes < 4:
                    if indexRobotOrientacoes == orientacaoDestino and canGoForward(indexRobotOrientacoes, indexRobot):
                        break
                    indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
                    if(list(tabuleiro[indexRobot])[indexToLeft] == SEM_PAREDE and indexToLeft == orientacaoDestino):
                        turnLeft()
                    elif(orientacaoDestino % 2 == indexRobotOrientacoes % 2):
                        turn180()
                    else:
                        turnRight()
                    numeroRotacoes += 1
                goForward()
            else:
                percursoPeloAEstrela = True
                percurso = AEstrela(indexRobot,indexDestino)
    else:
        percurso = AEstrela(indexRobot,indexDestino)
        while indexRobot != indexDestino:
            indexDestinoIntermediario = percurso.pop(0)
            if (indexDestinoIntermediario + CIMA) == indexRobot:
                orientacaoDestino = POS_SUL
            elif (indexDestinoIntermediario + DIREITA) == indexRobot:
                orientacaoDestino = POS_OESTE
            elif (indexDestinoIntermediario + ESQUERDA) == indexRobot:
                orientacaoDestino = POS_ESTE
            elif (indexDestinoIntermediario + BAIXO) == indexRobot:
                orientacaoDestino = POS_NORTE
            numeroRotacoes = 0
            while numeroRotacoes < 4:
                if indexRobotOrientacoes == orientacaoDestino and canGoForward(indexRobotOrientacoes, indexRobot):
                    break
                indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
                if(list(tabuleiro[indexRobot])[indexToLeft] == SEM_PAREDE and indexToLeft == orientacaoDestino):
                    turnLeft()
                elif(orientacaoDestino % 2 == indexRobotOrientacoes % 2):
                    turn180()
                else:
                    turnRight()
                numeroRotacoes += 1
            goForward()


"""
                    BOARD RECON FUNCTION
"""
# Função que trata do reconhecimento inicial do tabuleiro


def recon():
    global indexRobot, indexRobotOrientacoes, indexOvelha1, indexOvelha2
    numeroOvelhas = 0
    indexRobot = 0
    quadradosDesconhecidos = list(range(len(tabuleiro)))
    onlyOnce = True
    while True:
        checkSides()
        numeroOvelhas = 0
        for index in range(len(tabuleiro)):  # Contar ovelhas
            aux = list(tabuleiro[index])
            if aux[4] == "1":
                numeroOvelhas += 1
                if indexOvelha1 == -15:
                    indexOvelha1 = index
                elif index != indexOvelha1 and indexOvelha2 == -15:
                    indexOvelha2 = index
        if onlyOnce and (indexOvelha1+DIREITA) == indexOvelha2 or (indexOvelha1+ESQUERDA) == indexOvelha2 or (indexOvelha1+CIMA) == indexOvelha2 or (indexOvelha1+BAIXO) == indexOvelha2:
            debug_print("HERE")
            onlyOnce = False
            auxList = list(tabuleiro[indexOvelha1])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = PAREDE
            tabuleiro[indexOvelha1] = "".join(auxList)
            auxList = list(tabuleiro[indexOvelha2])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = PAREDE
            tabuleiro[indexOvelha2] = "".join(auxList)
            removeKnownSquares()
        if (numeroParedes == 6 and numeroOvelhas == 2) or len(quadradosDesconhecidos) == 0 or (len(quadradosDesconhecidos) == 2 and not ((indexOvelha1+DIREITA) == indexOvelha2 or (indexOvelha1+ESQUERDA) == indexOvelha2 or (indexOvelha1+CIMA) == indexOvelha2 or (indexOvelha1+BAIXO) == indexOvelha2)):
            break
        indexDestino = nextSquareToCheck()
        fimRecon = moveTo(indexDestino, True, numeroOvelhas)
        if fimRecon:
            break
    debug_print(quadradosDesconhecidos)
    if numeroParedes == 6:
        if (indexOvelha1+DIREITA) == indexOvelha2 or (indexOvelha1+ESQUERDA) == indexOvelha2 or (indexOvelha1+CIMA) == indexOvelha2 or (indexOvelha1+BAIXO) == indexOvelha2:
            debug_print("Ovelha 1: "+str(indexOvelha1))
            debug_print("Ovelha 2: "+str(indexOvelha2))
            auxList = list(tabuleiro[indexOvelha1])
            for index in range(4):
                if(auxList[index] == PAREDE):
                    auxList[index] = SEM_PAREDE
            tabuleiro[indexOvelha1] = "".join(auxList)
            auxList = list(tabuleiro[indexOvelha2])
            for index in range(4):
                if(auxList[index] == PAREDE):
                    auxList[index] = SEM_PAREDE
            tabuleiro[indexOvelha2] = "".join(auxList)

        for quadrado in quadradosDesconhecidos:
            auxList = list(tabuleiro[quadrado])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = SEM_PAREDE
            tabuleiro[quadrado] = "".join(auxList)
        # numeroOvelhas = 0
        # for index in range(len(tabuleiro)):  # Contar ovelhas
        #     aux = list(tabuleiro[index])
        #     if aux[4] == "1":
        #         numeroOvelhas += 1
        #         if indexOvelha1 == -1:
        #             indexOvelha1 = index
        #         else:
        #             indexOvelha2 = index
        # if numeroOvelhas == 1:
        #     aux = list(tabuleiro[indexOvelha1])
        #     aux[4] = "2"
        #     tabuleiro[indexOvelha1] = "".join(aux)
    # else:
    #     for quadrado in quadradosDesconhecidos:
    #         auxList = list(tabuleiro[quadrado])
    #         for index in range(4):
    #             if(auxList[index] == DESCONHECIDO):
    #                 auxList[index] = PAREDE
    #         tabuleiro[quadrado] = "".join(auxList)
    printTabuleiro()


def printMatrizCusto(matrizCusto):
    index = 30
    while index > -1:
        debug_print(str(matrizCusto[index])+" "+str(matrizCusto[index+1])+" "+str(matrizCusto[index+2])+" "+str(
            matrizCusto[index+3])+" "+str(matrizCusto[index+4])+" "+str(matrizCusto[index+5]))
        index -= TAMANHO_LINHA_TABULEIRO


def AEstrela(indexStart,indexDestino):
    global tabuleiro
    custoMovimentoTabuleiro = [0] * \
        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexStart] = 1
    num = 1
    printMatrizCusto(custoMovimentoTabuleiro)
    while not stepAEstrela(num, custoMovimentoTabuleiro, indexDestino):
        # printMatrizCusto(custoMovimentoTabuleiro)
        # debug_print(" ")
        num += 1
    percurso = [indexDestino]
    index = indexDestino
    num = custoMovimentoTabuleiro[indexDestino]
    while num > 1:
        # debug_print(index)
        # debug_print(percurso)
        if (index+ESQUERDA) > -1 and custoMovimentoTabuleiro[index+ESQUERDA] == num-1:
            # debug_print("ESQUERDA")
            index += ESQUERDA
            percurso.append(index)
            num -= 1
        elif (index+BAIXO) > -1 and custoMovimentoTabuleiro[index+BAIXO] == num-1:
            # debug_print("BAIXO")
            index += BAIXO
            percurso.append(index)
            num -= 1
        elif (index+DIREITA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+DIREITA] == num-1:
            # debug_print("DIREITA")
            index += DIREITA
            percurso.append(index)
            num -= 1
        elif (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == num-1:
            # debug_print("CIMA")
            index += CIMA
            percurso.append(index)
            num -= 1
    percurso.reverse()
    percurso.pop(0)
    # debug_print(percurso)
    return percurso


def stepAEstrela(num, custoMovimentoTabuleiro, objetivo):
    chegouObjetivo = False
    for index in range(len(custoMovimentoTabuleiro)):
        if chegouObjetivo:
            break
        if custoMovimentoTabuleiro[index] == num:
            chegouObjetivo = index == objetivo
            if canGoForward(POS_SUL, index) and (index+BAIXO) > 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
            if canGoForward(POS_OESTE, index) and (index+ESQUERDA) > 0 and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
            if canGoForward(POS_NORTE, index) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
            if canGoForward(POS_ESTE, index) and (index+DIREITA) > 0 and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
    return chegouObjetivo


def sheepMove(indexRobot, indexOvelha):
    # debug_print("Index Ovelha "+str(indexOvelha))
    if indexRobot+DIREITA == indexOvelha:
        if sheepCanGoForward(POS_ESTE, indexOvelha):
            indexOvelha += DIREITA
        elif sheepCanGoForward(POS_SUL, indexOvelha):
            indexOvelha += BAIXO
        elif sheepCanGoForward(POS_OESTE, indexOvelha):
            indexOvelha += ESQUERDA
        else:
            indexOvelha += CIMA
    elif indexRobot+BAIXO == indexOvelha:
        if sheepCanGoForward(POS_SUL, indexOvelha):
            indexOvelha += BAIXO
        elif sheepCanGoForward(POS_OESTE, indexOvelha):
            indexOvelha += ESQUERDA
        elif sheepCanGoForward(POS_NORTE, indexOvelha):
            indexOvelha += CIMA
        else:
            indexOvelha += DIREITA
    elif indexRobot+ESQUERDA == indexOvelha:
        if sheepCanGoForward(POS_OESTE, indexOvelha):
            indexOvelha += ESQUERDA
        elif sheepCanGoForward(POS_NORTE, indexOvelha):
            indexOvelha += CIMA
        elif sheepCanGoForward(POS_ESTE, indexOvelha):
            indexOvelha += DIREITA
        else:
            indexOvelha += BAIXO
    else:
        if sheepCanGoForward(POS_NORTE, indexOvelha):
            indexOvelha += CIMA
        elif sheepCanGoForward(POS_ESTE, indexOvelha):
            indexOvelha += DIREITA
        elif sheepCanGoForward(POS_SUL, indexOvelha):
            indexOvelha += BAIXO
        else:
            indexOvelha += ESQUERDA
    return indexOvelha


def calculateSheepMovement(tipoAcao, indexOvelha):
    global tabuleiro, indexRobot
    # ultimoIndexOvelha = indexOvelha
    if tipoAcao == "S":  # S de scream,grito
        indexOvelha = sheepMove(indexRobot, indexOvelha)
    else:  # tocou na ovelha
        movimentos = 0
        while movimentos < 2:
            indexOvelha = sheepMove(indexRobot, indexOvelha)
            movimentos += 1
    return indexOvelha


def relocateSheep(indicePrevio, indiceNovo):
    global tabuleiro
    # printTabuleiro()
    debug_print("Index Previo "+str(indicePrevio))
    debug_print("Index Novo "+str(indiceNovo))
    aux = list(tabuleiro[indicePrevio])
    aux[4] = str(int(aux[4])-1)
    tabuleiro[indicePrevio] = "".join(aux)
    aux = list(tabuleiro[indiceNovo])
    aux[4] = str(int(aux[4])+1)
    tabuleiro[indiceNovo] = "".join(aux)
    # printTabuleiro()


def connectSheep():
    global indexOvelha1, indexOvelha2, indexRobot
    # determinar ovelha mais perto
    ovelhaMaisPertoE1 = -1
    distanciaOvelha1 = abs(indexRobot % TAMANHO_LINHA_TABULEIRO-indexOvelha1 % TAMANHO_LINHA_TABULEIRO) + \
        abs(indexRobot//TAMANHO_LINHA_TABULEIRO -
            indexOvelha1//TAMANHO_LINHA_TABULEIRO)
    distanciaOvelha2 = abs(indexRobot % TAMANHO_LINHA_TABULEIRO-indexOvelha2 % TAMANHO_LINHA_TABULEIRO) + \
        abs(indexRobot//TAMANHO_LINHA_TABULEIRO -
            indexOvelha2//TAMANHO_LINHA_TABULEIRO)
    if distanciaOvelha1 > distanciaOvelha2:
        ovelhaMaisPertoE1 = False
    else:
        ovelhaMaisPertoE1 = True
    debug_print(ovelhaMaisPertoE1)
    if ovelhaMaisPertoE1:
        if indexOvelha2 % TAMANHO_LINHA_TABULEIRO > indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
            moveTo(indexOvelha1+ESQUERDA, False, 2)
        elif indexOvelha2 % TAMANHO_LINHA_TABULEIRO < indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
            moveTo(indexOvelha1+DIREITA, False, 2)
        else:
            if indexOvelha2//TAMANHO_LINHA_TABULEIRO > indexOvelha1//TAMANHO_LINHA_TABULEIRO:
                moveTo(indexOvelha1+BAIXO, False, 2)
            elif indexOvelha2//TAMANHO_LINHA_TABULEIRO < indexOvelha1//TAMANHO_LINHA_TABULEIRO:
                moveTo(indexOvelha1+CIMA, False, 2)
        while indexOvelha1 != indexOvelha2:
            indexFuturo = calculateSheepMovement("S", indexOvelha1)
            if indexFuturo == indexOvelha2:
                debug_print()
                debug_print(indexFuturo)
                debug_print(indexOvelha1)
                movement.scream()
                relocateSheep(indexOvelha1, indexFuturo)
                indexOvelha1 = indexFuturo
                debug_print()
                debug_print(indexOvelha1)
                debug_print(indexOvelha2)
            indexFuturo = calculateSheepMovement("T", indexOvelha1)
            if indexFuturo == indexOvelha2:
                debug_print()
                debug_print(indexFuturo)
                debug_print(indexOvelha1)
                movement.touchSheep()
                relocateSheep(indexOvelha1, indexFuturo)
                indexOvelha1 = indexFuturo
                debug_print()
                debug_print(indexOvelha1)
                debug_print(indexOvelha2)
    else:
        if indexOvelha2 % TAMANHO_LINHA_TABULEIRO > indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
            moveTo(indexOvelha2+DIREITA, False, 2)
        elif indexOvelha2 % TAMANHO_LINHA_TABULEIRO < indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
            moveTo(indexOvelha2+ESQUERDA, False, 2)
        else:
            if indexOvelha2//TAMANHO_LINHA_TABULEIRO > indexOvelha1//TAMANHO_LINHA_TABULEIRO:
                moveTo(indexOvelha2+CIMA, False, 2)
            elif indexOvelha2//TAMANHO_LINHA_TABULEIRO < indexOvelha1//TAMANHO_LINHA_TABULEIRO:
                moveTo(indexOvelha2+BAIXO, False, 2)
        while indexOvelha1 != indexOvelha2:
            indexFuturo = calculateSheepMovement("S", indexOvelha2)
            if indexFuturo == indexOvelha1:
                debug_print()
                debug_print(indexFuturo)
                debug_print(indexOvelha2)
                movement.scream()
                relocateSheep(indexOvelha2, indexFuturo)
                indexOvelha2 = indexFuturo
                debug_print()
                debug_print(indexOvelha1)
                debug_print(indexOvelha2)
            indexFuturo = calculateSheepMovement("T", indexOvelha2)
            if indexFuturo == indexOvelha1:
                debug_print()
                debug_print(indexFuturo)
                debug_print(indexOvelha2)
                movement.touchSheep()
                relocateSheep(indexOvelha2, indexFuturo)
                indexOvelha2 = indexFuturo
                debug_print()
                debug_print(indexOvelha1)
                debug_print(indexOvelha2)


def AEstrelaOvelhas():
    # as ovelhas estão juntas, os indíces são iguais
    global tabuleiro, indexRobot, indexOvelha1,numeroMovimentosRobot
    custoMovimentoTabuleiro = [0] * TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    while True:
        for index in range(len(tabuleiro)):
            if index==indexOvelha1:
                aux = list(tabuleiro[index])
                aux[4] = str(2)
                tabuleiro[index] = "".join(aux)
            else:
                aux = list(tabuleiro[index])
                aux[4] = str(0)
                tabuleiro[index] = "".join(aux)
        indexStart = indexOvelha1
        custoMovimentoTabuleiro[indexStart] = 1
        num = 1
        indexDestino = 35
        printMatrizCusto(custoMovimentoTabuleiro)
        while not stepAEstrelaOvelhas(num, custoMovimentoTabuleiro, indexDestino):
            printMatrizCusto(custoMovimentoTabuleiro)
            debug_print(" ")
            num += 1
        percurso = [indexDestino]
        index = indexDestino
        num = custoMovimentoTabuleiro[indexDestino]
        while num > 1:
            # debug_print(index)
            # debug_print(percurso)
            if (index+ESQUERDA) > -1 and custoMovimentoTabuleiro[index+ESQUERDA] == num-1:
                # debug_print("ESQUERDA")
                index += ESQUERDA
                percurso.append(index)
                num -= 1
            elif (index+BAIXO) > -1 and custoMovimentoTabuleiro[index+BAIXO] == num-1:
                # debug_print("BAIXO")
                index += BAIXO
                percurso.append(index)
                num -= 1
            elif (index+DIREITA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+DIREITA] == num-1:
                # debug_print("DIREITA")
                index += DIREITA
                percurso.append(index)
                num -= 1
            elif (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == num-1:
                # debug_print("CIMA")
                index += CIMA
                percurso.append(index)
                num -= 1
        percurso.reverse()
        # percurso.pop(0)
        debug_print(percurso)
        percursoValido=True
        possivelIndexRobot=indexRobot
        proximoIndexRobot=-1
        for index in range(len(percurso)):
            if percurso[index+1]-percurso[index]==CIMA:
                proximoIndexRobot=percurso[index]+BAIXO
            elif percurso[index+1]-percurso[index]==BAIXO:
                proximoIndexRobot=percurso[index]+CIMA
            elif percurso[index+1]-percurso[index]==DIREITA:
                proximoIndexRobot=percurso[index]+ESQUERDA
            elif percurso[index+1]-percurso[index]==ESQUERDA:
                proximoIndexRobot=percurso[index]+DIREITA
            if len(AEstrela(possivelIndexRobot,proximoIndexRobot))>numeroMovimentosRobot:
                for indexCost in range(len(custoMovimentoTabuleiro)):
                    if custoMovimentoTabuleiro[indexCost]!=-1:
                        custoMovimentoTabuleiro[indexCost]=0
                # custoMovimentoTabuleiro=[0]*TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
                custoMovimentoTabuleiro[percurso[index+1]]=-1
                percursoValido=False
                break
            else:
                debug_print("INDEX "+ str(index))
                relocateSheep(percurso[index],percurso[index+1])
                relocateSheep(percurso[index],percurso[index+1])
                # indexOvelha1=percurso[index+1]
                aux=AEstrela(possivelIndexRobot,proximoIndexRobot)
                possivelIndexRobot=aux[len(aux)-1]
                debug_print("Proximo index Robot: "+str(possivelIndexRobot))
            numeroMovimentosRobot=2

        if percursoValido:
            break
        debug_print(" ")
    return percurso


def stepAEstrelaOvelhas(num, custoMovimentoTabuleiro, objetivo):
    chegouObjetivo = False
    for index in range(len(custoMovimentoTabuleiro)):
        if chegouObjetivo:
            break
        if custoMovimentoTabuleiro[index] == num:
            chegouObjetivo = index == objetivo
            if sheepCanGoForward(POS_SUL, index) and (index+BAIXO) > 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
            if sheepCanGoForward(POS_OESTE, index) and (index+ESQUERDA) > 0 and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
            if sheepCanGoForward(POS_NORTE, index) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
            if sheepCanGoForward(POS_ESTE, index) and (index+DIREITA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
    return chegouObjetivo


def playGame():
    global indexOvelha1, indexOvelha2, tabuleiro,numeroMovimentosRobot
    connectSheep()
    numeroMovimentosRobot-=1
    percurso=AEstrelaOvelhas()
    debug_print(percurso)
    # debug_print(tabuleiro)
    # moveTo(indexOvelha1+DIREITA,False,2)
    # indexOvelha1=calculateSheepMovement("S",indexOvelha1)
    # movement.scream()
    # debug_print("HERE0")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # moveTo(indexOvelha1+DIREITA,False,2)
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE1")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # movement.touchSheep()
    # moveTo(indexOvelha1+BAIXO,False,2)
    # turnRight()
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE2")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # movement.touchSheep()
    # moveTo(indexOvelha1+BAIXO,False,2)
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE3")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # movement.touchSheep()
    # moveTo(indexOvelha1+ESQUERDA,False,2)
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE4")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # movement.touchSheep()
    # moveTo(indexOvelha1+ESQUERDA,False,2)
    # # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # # debug_print("HERE5")
    # # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # # moveTo(indexOvelha1+ESQUERDA,False,2)
    # debug_print("HERE6")
    # indexOvelha1=calculateSheepMovement("S",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("S",indexOvelha2)
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # movement.scream()


# movement.backup()
# movement.scream()
fillStartingBoard()
# recon()
# movement.scream()
indexOvelha1 = 14
indexOvelha2 = 13
aux = list(tabuleiro[indexOvelha1])
aux[4] = "1"
tabuleiro[indexOvelha1] = "".join(aux)
aux = list(tabuleiro[indexOvelha2])
aux[4] = "1"
tabuleiro[indexOvelha2] = "".join(aux)
aux = list(tabuleiro[16])
aux[POS_ESTE] = PAREDE
aux[POS_SUL] = PAREDE
tabuleiro[16] = "".join(aux)
aux = list(tabuleiro[22])
aux[POS_ESTE] = PAREDE
tabuleiro[22] = "".join(aux)
aux = list(tabuleiro[28])
aux[POS_ESTE] = PAREDE
tabuleiro[28] = "".join(aux)
# debug_print(indexOvelha1+DIREITA)
playGame()
# movement.turnLeft()
# time.sleep(1)
# movement.turnRight()
# movement.touchSheep()
# while True:
#     checkSheep()
