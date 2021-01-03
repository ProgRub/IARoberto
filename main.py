#!/usr/bin/env python3

# from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
# import movement
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
OVELHA = "1"
ROBOT_ORIENTACOES ="NESW"
indexRobotOrientacoes = 0
indexRobot = 0
ultimoIndexRobot = -15
indexOvelha1 = -15
indexOvelha2 = -15
# colorSensor = ColorSensor()
# colorSensor.mode = 'COL-REFLECT'
# colorSensor.calibrate_white()
# sonic = UltrasonicSensor()
# sonic.mode = UltrasonicSensor.MODE_US_DIST_CM
# units = sonic.units
numeroParedes = 0
numeroMovimentosRobot=2
tabuleiro = []
quadradosDesconhecidos = list(
    range(TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO))


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


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


def sheepCanGoForward(orientacao, indexOvelha,indexRobot):
    if orientacao == POS_NORTE:
        robotAFrente = (indexOvelha + CIMA)==indexRobot
    elif orientacao == POS_ESTE:
        robotAFrente = (indexOvelha + DIREITA)==indexRobot
    elif orientacao == POS_SUL:
        robotAFrente = (indexOvelha + BAIXO)==indexRobot
    else:
        robotAFrente = (indexOvelha + ESQUERDA)==indexRobot
    return not(list(tabuleiro[indexOvelha])[orientacao] == PAREDE or robotAFrente)


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
    # movement.moveForwardForever()
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
    # movement.stopRobot()
    # movement.backup()
    return parede

# Função que verifica se há uma ovelha à sua frente


def checkSheep():
    global sonic
    # debug_print("ULTRASONIC "+str(sonic.value()//10))
    if (sonic.value() // 10) > 15 and (sonic.value() // 10) < 40:
        # movement.beep()
        return True
    return False




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
    # movement.turnRight()
    indexRobotOrientacoes = (indexRobotOrientacoes+1) % 4

# Função que vira o robot para trás e atualiza a orientação do robot


def turn180():
    global indexRobotOrientacoes
    # movement.do180()
    indexRobotOrientacoes = (indexRobotOrientacoes+2) % 4

# Função que vira o robot para a esquerda e atualiza a orientação do robot


def turnLeft():
    global indexRobotOrientacoes
    # movement.turnLeft()
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
    # movement.forwardOneSquare()

def turnTowardsOrientation(orientacaoDestino):
    global indexRobotOrientacoes,indexRobot
    numeroRotacoes = 0
    while numeroRotacoes < 4:
        if indexRobotOrientacoes == orientacaoDestino and canGoForward(indexRobotOrientacoes, indexRobot):
            break
        indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
        if indexToLeft == orientacaoDestino:
            turnLeft()
        elif orientacaoDestino % 2 == indexRobotOrientacoes % 2:
            turn180()
        else:
            turnRight()
        numeroRotacoes += 1

def moveTo(indexDestino, paraRecon, numeroOvelhas):
    global indexRobot, tabuleiro, ultimoIndexRobot, quadradosDesconhecidos, numeroParedes
    orientacaoDestino = -1
    # debug_print("Index Destino:"+str(indexDestino))
    # debug_print("Index Robot:"+str(indexRobot))
    # debug_print(isBeco())
    # debug_print("Ultimo Index Robot:"+str(ultimoIndexRobot))
    percurso = []
    indexDestinoIntermediario = indexDestino
    # percursoPeloAEstrela = False
    haParede = False
    # if paraRecon:
    #     while indexRobot != indexDestino:
    #         if ((indexRobot+DIREITA) == indexDestino or (indexRobot+ESQUERDA) == indexDestino or (indexRobot+CIMA) == indexDestino or (indexRobot+BAIXO) == indexDestino) or len(percurso) > 1:
    #             hasMove = False
    #             if len(percurso) > 0:
    #                 indexDestinoIntermediario = percurso.pop(0)
    #                 debug_print(indexDestinoIntermediario)
    #             else:
    #                 percursoPeloAEstrela = False
    #             if indexRobot in quadradosDesconhecidos:
    #                 haParede = checkSides()
    #             debug_print("MOVETO " + str(haParede) +
    #                         " " + str(percursoPeloAEstrela))
    #             if haParede and percursoPeloAEstrela:
    #                 debug_print("RECALCULAR")
    #                 percurso = []
    #             debug_print("Ovelhas e Paredes " +
    #                         str(numeroParedes)+" "+str(numeroOvelhas))
    #             if (numeroParedes == 6 and numeroOvelhas == 2) or len(quadradosDesconhecidos) == 0 or (len(quadradosDesconhecidos) == 2 and not squaresAreAdjacent(indexOvelha1,indexOvelha2)):
    #                 return True
    #             if haParede and percursoPeloAEstrela:
    #                 debug_print("RECALCULAR")
    #                 percurso = AEstrela(indexRobot,indexDestino,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
    #             haParede = False
    #             if indexDestinoIntermediario % TAMANHO_LINHA_TABULEIRO < indexRobot % TAMANHO_LINHA_TABULEIRO:
    #                 if canGoForward(POS_OESTE, indexRobot):
    #                     orientacaoDestino = POS_OESTE
    #                     hasMove = True
    #             if indexDestinoIntermediario % TAMANHO_LINHA_TABULEIRO > indexRobot % TAMANHO_LINHA_TABULEIRO and not hasMove:
    #                 if canGoForward(POS_ESTE, indexRobot):
    #                     orientacaoDestino = POS_ESTE
    #                     hasMove = True
    #             if indexRobot//TAMANHO_LINHA_TABULEIRO < indexDestinoIntermediario//TAMANHO_LINHA_TABULEIRO and not hasMove:
    #                 if canGoForward(POS_NORTE, indexRobot):
    #                     orientacaoDestino = POS_NORTE
    #                     hasMove = True
    #             if indexRobot//TAMANHO_LINHA_TABULEIRO > indexDestinoIntermediario//TAMANHO_LINHA_TABULEIRO and not hasMove:
    #                 if canGoForward(POS_SUL, indexRobot):
    #                     orientacaoDestino = POS_SUL
    #                     hasMove = True
    #             if not hasMove:
    #                 percursoPeloAEstrela = True
    #                 percurso = AEstrela(indexRobot,indexDestino,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
    #                 continue
    #             ultimoIndexRobot = indexRobot
    #             debug_print("OrientacaoDestino:"+str(orientacaoDestino))
    #             turnTowardsOrientation(orientacaoDestino)
    #             goForward()
    #         else:
    #             percursoPeloAEstrela = True
    #             percurso = AEstrela(indexRobot,indexDestino,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
    # else:
    percurso = AEstrela(indexRobot,indexDestino,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
    while indexRobot != indexDestino:
        if paraRecon:
            if indexRobot in quadradosDesconhecidos:
                haParede = checkSides()
            if (numeroParedes == 6 and numeroOvelhas == 2) or len(quadradosDesconhecidos) == 0 or (len(quadradosDesconhecidos) == 2 and squaresAreAdjacent(indexOvelha1,indexOvelha2)):
                return True
            if haParede:
                debug_print("RECALCULAR PERCURSO")
                percurso = AEstrela(indexRobot,indexDestino,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
        indexDestinoIntermediario = percurso.pop(0)
        if (indexDestinoIntermediario + CIMA) == indexRobot:
            orientacaoDestino = POS_SUL
        elif (indexDestinoIntermediario + DIREITA) == indexRobot:
            orientacaoDestino = POS_OESTE
        elif (indexDestinoIntermediario + ESQUERDA) == indexRobot:
            orientacaoDestino = POS_ESTE
        elif (indexDestinoIntermediario + BAIXO) == indexRobot:
            orientacaoDestino = POS_NORTE
        turnTowardsOrientation(orientacaoDestino)
        goForward()

"""
                    AUXILIARY FUNCTIONS

"""

def squaresAreAdjacent(index1,index2):
    return (index1+DIREITA) == index2 or (index1+ESQUERDA) == index2 or (index1+CIMA) == index2 or (index1+BAIXO) == index2



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
        if onlyOnce and squaresAreAdjacent(indexOvelha1,indexOvelha2):
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
        if (numeroParedes == 6 and numeroOvelhas == 2) or len(quadradosDesconhecidos) == 0 or (len(quadradosDesconhecidos) == 2 and not (squaresAreAdjacent(indexOvelha1,indexOvelha2))):
            break
        indexDestino = nextSquareToCheck()
        fimRecon = moveTo(indexDestino, True, numeroOvelhas)
        if fimRecon:
            break
    debug_print(quadradosDesconhecidos)
    if numeroParedes == 6:
        if squaresAreAdjacent(indexOvelha1,indexOvelha2):
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
    debug_print(" ")


def AEstrela(indexStart,indexDestino,numeroMaximoMovimentos):
    global tabuleiro
    custoMovimentoTabuleiro = [0] * \
        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexStart] = 1
    num = 1
    percursoEncontrado=False
    while not percursoEncontrado and num<(numeroMaximoMovimentos+1):
        # printMatrizCusto(custoMovimentoTabuleiro)
        percursoEncontrado=stepAEstrela(num, custoMovimentoTabuleiro, indexDestino)
        num += 1
    # printMatrizCusto(custoMovimentoTabuleiro)
    if not percursoEncontrado:
        return []
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
            if canGoForward(POS_SUL, index) and (index+BAIXO) > 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
                chegouObjetivo = (index+BAIXO) == objetivo
            if canGoForward(POS_OESTE, index) and (index+ESQUERDA) > 0 and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
                chegouObjetivo = (index+ESQUERDA) == objetivo
            if canGoForward(POS_NORTE, index) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
                chegouObjetivo = (index+CIMA) == objetivo
            if canGoForward(POS_ESTE, index) and (index+DIREITA) > 0 and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
                chegouObjetivo = (index+DIREITA) == objetivo
    return chegouObjetivo


def sheepMove(indexRobot, indexOvelha):
    # debug_print("Index Ovelha "+str(indexOvelha))
    if indexRobot+DIREITA == indexOvelha:#robot está à esquerda da ovelha
        if sheepCanGoForward(POS_ESTE, indexOvelha,indexRobot):
            indexOvelha += DIREITA
        elif sheepCanGoForward(POS_SUL, indexOvelha,indexRobot):
            indexOvelha += BAIXO
        elif sheepCanGoForward(POS_OESTE, indexOvelha,indexRobot):
            indexOvelha += ESQUERDA
        else:
            indexOvelha += CIMA
    elif indexRobot+BAIXO == indexOvelha: #robot está acima da ovelha
        if sheepCanGoForward(POS_SUL, indexOvelha,indexRobot):
            indexOvelha += BAIXO
        elif sheepCanGoForward(POS_OESTE, indexOvelha,indexRobot):
            indexOvelha += ESQUERDA
        elif sheepCanGoForward(POS_NORTE, indexOvelha,indexRobot):
            indexOvelha += CIMA
        else:
            indexOvelha += DIREITA
    elif indexRobot+ESQUERDA == indexOvelha: #robot está à direita da ovelha
        if sheepCanGoForward(POS_OESTE, indexOvelha,indexRobot):
            indexOvelha += ESQUERDA
        elif sheepCanGoForward(POS_NORTE, indexOvelha,indexRobot):
            indexOvelha += CIMA
        elif sheepCanGoForward(POS_ESTE, indexOvelha,indexRobot):
            indexOvelha += DIREITA
        else:
            indexOvelha += BAIXO
    else: #robot está abaixo da ovelha
        # if indexOvelha==35:
        #     # debug_print("HERE")
        #     debug_print(indexRobot)
        if sheepCanGoForward(POS_NORTE, indexOvelha,indexRobot):
            indexOvelha += CIMA
        elif sheepCanGoForward(POS_ESTE, indexOvelha,indexRobot):
            indexOvelha += DIREITA
        elif sheepCanGoForward(POS_SUL, indexOvelha,indexRobot):
            indexOvelha += BAIXO
        else:
            indexOvelha += ESQUERDA
    return indexOvelha


def calculateSheepMovement(tipoAcao, indexOvelha,indexRobot):
    global tabuleiro
    # ultimoIndexOvelha = indexOvelha
    # if indexOvelha==35:
    #     debug_print("HERE")
    #     debug_print(sheepMove(indexRobot,indexOvelha))
    if squaresAreAdjacent(indexRobot,indexOvelha):
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
    # debug_print("Index Previo "+str(indicePrevio))
    # debug_print("Index Novo "+str(indiceNovo))
    aux = list(tabuleiro[indicePrevio])
    aux[4] = str(int(aux[4])-1)
    tabuleiro[indicePrevio] = "".join(aux)
    aux = list(tabuleiro[indiceNovo])
    aux[4] = str(int(aux[4])+1)
    tabuleiro[indiceNovo] = "".join(aux)
    # printTabuleiro()


def connectSheep():
    global indexOvelha1, indexOvelha2, indexRobot,numeroMovimentosRobot
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
    # debug_print(ovelhaMaisPertoE1)
    if ovelhaMaisPertoE1:
        resultadoRaciocinio=AEstrelaOvelhas(indexOvelha2,indexOvelha1)
        percursoOvelha=resultadoRaciocinio[0]
        percursoRobot=resultadoRaciocinio[1]
        # debug_print("Percurso Robot: "+str(percursoRobot))
        moveTo(percursoRobot,False,2)
        # if indexOvelha2 % TAMANHO_LINHA_TABULEIRO > indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
        #     moveTo(indexOvelha1+ESQUERDA, False, 2)
        # elif indexOvelha2 % TAMANHO_LINHA_TABULEIRO < indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
        #     moveTo(indexOvelha1+DIREITA, False, 2)
        # else:
        #     if indexOvelha2//TAMANHO_LINHA_TABULEIRO > indexOvelha1//TAMANHO_LINHA_TABULEIRO:
        #         moveTo(indexOvelha1+BAIXO, False, 2)
        #     elif indexOvelha2//TAMANHO_LINHA_TABULEIRO < indexOvelha1//TAMANHO_LINHA_TABULEIRO:
        #         moveTo(indexOvelha1+CIMA, False, 2)
        # while indexOvelha1 != indexOvelha2:
        #     indexFuturo = calculateSheepMovement("S", indexOvelha1,indexRobot)
        #     if indexFuturo == indexOvelha2:
        #         # debug_print()
        #         # debug_print(indexFuturo)
        #         # debug_print(indexOvelha1)
        #         # movement.scream()
        #         relocateSheep(indexOvelha1, indexFuturo)
        #         indexOvelha1 = indexFuturo
        #         # debug_print()
        #         # debug_print(indexOvelha1)
        #         # debug_print(indexOvelha2)
        #     indexFuturo = calculateSheepMovement("T", indexOvelha1,indexRobot)
        #     if indexFuturo == indexOvelha2:
        #         # debug_print()
        #         # debug_print(indexFuturo)
        #         # debug_print(indexOvelha1)
        #         # movement.touchSheep()
        #         relocateSheep(indexOvelha1, indexFuturo)
        #         indexOvelha1 = indexFuturo
        #         # debug_print()
        #         # debug_print(indexOvelha1)
        #         # debug_print(indexOvelha2)
    else:
        resultadoRaciocinio=AEstrelaOvelhas(indexOvelha1,indexOvelha2)
        percursoOvelha=resultadoRaciocinio[0]
        percursoRobot=resultadoRaciocinio[1]
        # debug_print("Percurso Robot: "+str(percursoRobot))
        moveTo(percursoRobot[len(percursoRobot)-1],False,2)
        # if indexOvelha2 % TAMANHO_LINHA_TABULEIRO > indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
        #     moveTo(indexOvelha2+DIREITA, False, 2)
        # elif indexOvelha2 % TAMANHO_LINHA_TABULEIRO < indexOvelha1 % TAMANHO_LINHA_TABULEIRO:
        #     moveTo(indexOvelha2+ESQUERDA, False, 2)
        # else:
        #     if indexOvelha2//TAMANHO_LINHA_TABULEIRO > indexOvelha1//TAMANHO_LINHA_TABULEIRO:
        #         moveTo(indexOvelha2+CIMA, False, 2)
        #     elif indexOvelha2//TAMANHO_LINHA_TABULEIRO < indexOvelha1//TAMANHO_LINHA_TABULEIRO:
        #         moveTo(indexOvelha2+BAIXO, False, 2)
        # while indexOvelha1 != indexOvelha2:
        #     indexFuturo = calculateSheepMovement("S", indexOvelha2,indexRobot)
        #     if indexFuturo == indexOvelha1:
        #         # debug_print()
        #         # debug_print(indexFuturo)
        #         # debug_print(indexOvelha2)
        #         # movement.scream()
        #         relocateSheep(indexOvelha2, indexFuturo)
        #         indexOvelha2 = indexFuturo
        #         # debug_print()
        #         # debug_print(indexOvelha1)
        #         # debug_print(indexOvelha2)
        #     indexFuturo = calculateSheepMovement("T", indexOvelha2,indexRobot)
        #     if indexFuturo == indexOvelha1:
        #         # debug_print()
        #         # debug_print(indexFuturo)
        #         # debug_print(indexOvelha2)
        #         # movement.touchSheep()
        #         relocateSheep(indexOvelha2, indexFuturo)
        #         indexOvelha2 = indexFuturo
        #         # debug_print()
        #         # debug_print(indexOvelha1)
        #         # debug_print(indexOvelha2)


def AEstrelaOvelhas(indexDestino,indexOvelha):
    # as ovelhas estão juntas, os indíces são iguais
    global tabuleiro, indexRobot, indexOvelha1,indexOvelha2,numeroMovimentosRobot
    custoMovimentoTabuleiro = [0] * TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    while True:
        indexStart = indexOvelha
        custoMovimentoTabuleiro[indexStart] = 1
        num = 1
        while not stepAEstrelaOvelhas(num, custoMovimentoTabuleiro, indexDestino):
            # printMatrizCusto(custoMovimentoTabuleiro)
            num += 1
        # printMatrizCusto(custoMovimentoTabuleiro)
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
        percursoValido=False
        possivelIndexRobot=indexRobot
        proximoIndexRobot=possivelIndexRobot
        percursoRobot=[possivelIndexRobot]
        for index in range(len(percurso)-1):
            percursoValido=False
            if calculateSheepMovement("S",percurso[index],percurso[index]+ESQUERDA)==percurso[index+1]:
                percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percurso[index]+ESQUERDA,numeroMovimentosRobot)
                if len(percursoRobotAteQuadradoDesejado)!=0:
                    percursoValido=True
                    proximoIndexRobot=percurso[index]+ESQUERDA
            if calculateSheepMovement("S",percurso[index],percurso[index]+DIREITA)==percurso[index+1] and not percursoValido:
                percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percurso[index]+DIREITA,numeroMovimentosRobot)
                if len(percursoRobotAteQuadradoDesejado)!=0:
                    percursoValido=True
                    proximoIndexRobot=percurso[index]+DIREITA
            if calculateSheepMovement("S",percurso[index],percurso[index]+BAIXO)==percurso[index+1] and not percursoValido:
                percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percurso[index]+BAIXO,numeroMovimentosRobot)
                if len(percursoRobotAteQuadradoDesejado)!=0:
                    percursoValido=True
                    proximoIndexRobot=percurso[index]+BAIXO
            if calculateSheepMovement("S",percurso[index],percurso[index]+CIMA)==percurso[index+1] and not percursoValido:
                percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percurso[index]+CIMA,numeroMovimentosRobot)
                if len(percursoRobotAteQuadradoDesejado)!=0:
                    percursoValido=True
                    proximoIndexRobot=percurso[index]+CIMA
            if percursoValido:
                percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,proximoIndexRobot,numeroMovimentosRobot)
                relocateSheep(percurso[index],percurso[index+1])
                if indexOvelha1==indexOvelha2:
                    relocateSheep(percurso[index],percurso[index+1])
                for index in range(len(percursoRobotAteQuadradoDesejado)):
                    percursoRobot.append(possivelIndexRobot)
                possivelIndexRobot=percursoRobotAteQuadradoDesejado[len(percursoRobotAteQuadradoDesejado)-1]
                numeroMovimentosRobot=2
            else:
                for indexCost in range(len(custoMovimentoTabuleiro)):
                    if custoMovimentoTabuleiro[indexCost]!=-1:
                        custoMovimentoTabuleiro[indexCost]=0
                # custoMovimentoTabuleiro=[0]*TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
                custoMovimentoTabuleiro[percurso[index+1]]=-1
                break
            # if percurso[index+1]-percurso[index]==CIMA: #se a ovelha tem que ir para cima
            #     if calculateSheepMovement("S",percurso[index],percurso[index]+ESQUERDA)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+ESQUERDA
            #     elif calculateSheepMovement("S",percurso[index],percurso[index]+DIREITA)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+ESQUERDA
            #     else:
            #         proximoIndexRobot=percurso[index]+BAIXO
            # elif percurso[index+1]-percurso[index]==BAIXO: #se a ovelha tem que ir para baixo
            #     if calculateSheepMovement("S",percurso[index],percurso[index]+ESQUERDA)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+ESQUERDA
            #     elif calculateSheepMovement("S",percurso[index],percurso[index]+DIREITA)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+ESQUERDA
            #     else:
            #         proximoIndexRobot=percurso[index]+CIMA
            # elif percurso[index+1]-percurso[index]==DIREITA: #se a ovelha tem que ir para direita
            #     if calculateSheepMovement("S",percurso[index],percurso[index]+BAIXO)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+BAIXO
            #     elif calculateSheepMovement("S",percurso[index],percurso[index]+CIMA)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+CIMA
            #     else:
            #         proximoIndexRobot=percurso[index]+ESQUERDA
            # elif percurso[index+1]-percurso[index]==ESQUERDA: #se a ovelha tem que ir para esquerda
            #     if calculateSheepMovement("S",percurso[index],percurso[index]+BAIXO)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+BAIXO
            #     elif calculateSheepMovement("S",percurso[index],percurso[index]+CIMA)==percurso[index+1]:
            #         proximoIndexRobot=percurso[index]+CIMA
            #     else:
            #         proximoIndexRobot=percurso[index]+DIREITA
            debug_print("Próximo index da ovelha se robot estiver à esquerda: "+str(calculateSheepMovement("S",percurso[index],percurso[index]+ESQUERDA)))
            debug_print("Próximo index da ovelha se robot estiver à direita: "+str(calculateSheepMovement("S",percurso[index],percurso[index]+DIREITA)))
            debug_print("Próximo index da ovelha se robot estiver abaixo: "+str(calculateSheepMovement("S",percurso[index],percurso[index]+BAIXO)))
            debug_print("Próximo index da ovelha se robot estiver acima: "+str(calculateSheepMovement("S",percurso[index],percurso[index]+CIMA)))
            debug_print("Proximo index Robot: "+str(proximoIndexRobot))
            debug_print("Index (Possivel) do Robot: "+str(possivelIndexRobot))
            # percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,proximoIndexRobot,15)
            # if len(percursoRobotAteQuadradoDesejado)>numeroMovimentosRobot:
            #     for indexCost in range(len(custoMovimentoTabuleiro)):
            #         if custoMovimentoTabuleiro[indexCost]!=-1:
            #             custoMovimentoTabuleiro[indexCost]=0
            #     # custoMovimentoTabuleiro=[0]*TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
            #     custoMovimentoTabuleiro[percurso[index+1]]=-1
            #     percursoValido=False
            #     break
            # else:
            #     # debug_print("INDEX "+ str(index))
            #     relocateSheep(percurso[index],percurso[index+1])
            #     relocateSheep(percurso[index],percurso[index+1])
            #     # indexOvelha1=percurso[index+1]
            #     possivelIndexRobot=percursoRobotAteQuadradoDesejado[len(percursoRobotAteQuadradoDesejado)-1]
            #     percursoRobot.append(possivelIndexRobot)
            # numeroMovimentosRobot=2
        if percursoValido:
            break
        debug_print(" ")
        if indexOvelha2==indexOvelha1:
            for index in range(len(tabuleiro)):
                if index==indexOvelha1:
                    aux = list(tabuleiro[index])
                    aux[4] = str(2)
                    tabuleiro[index] = "".join(aux)
                else:
                    aux = list(tabuleiro[index])
                    aux[4] = str(0)
                    tabuleiro[index] = "".join(aux)
        else:
            for index in range(len(tabuleiro)):
                if index==indexOvelha:
                    aux = list(tabuleiro[index])
                    aux[4] = str(1)
                    tabuleiro[index] = "".join(aux)
                elif index!=indexOvelha1 and index!=indexOvelha2:
                    aux = list(tabuleiro[index])
                    aux[4] = str(0)
                    tabuleiro[index] = "".join(aux)
    return percurso,percursoRobot


def stepAEstrelaOvelhas(num, custoMovimentoTabuleiro, objetivo):
    global indexRobot
    chegouObjetivo = False
    for index in range(len(custoMovimentoTabuleiro)):
        if chegouObjetivo:
            break
        if custoMovimentoTabuleiro[index] == num:
            chegouObjetivo = index == objetivo
            if sheepCanGoForward(POS_SUL, index,indexRobot) and (index+BAIXO) > 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
            if sheepCanGoForward(POS_OESTE, index,indexRobot) and (index+ESQUERDA) > 0 and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
            if sheepCanGoForward(POS_NORTE, index,indexRobot) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
            if sheepCanGoForward(POS_ESTE, index,indexRobot) and (index+DIREITA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
    return chegouObjetivo


def playGame():
    global indexOvelha1, indexOvelha2, tabuleiro,numeroMovimentosRobot,indexRobot
    numeroMovimentosRobot=36
    connectSheep()
    indexRobot=12
    numeroMovimentosRobot=1
    resultadoRaciocinio=AEstrelaOvelhas(35,indexOvelha1)
    percurso=resultadoRaciocinio[0]
    percursoRobot=resultadoRaciocinio[1]
    debug_print("Percurso Valido: "+str(percurso))
    debug_print("Percurso Robot: "+str(percursoRobot))
    # debug_print(tabuleiro)
    # moveTo(indexOvelha1+DIREITA,False,2)
    # indexOvelha1=calculateSheepMovement("S",indexOvelha1)
    # # movement.scream()
    # debug_print("HERE0")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # moveTo(indexOvelha1+DIREITA,False,2)
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE1")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # # movement.touchSheep()
    # moveTo(indexOvelha1+BAIXO,False,2)
    # turnRight()
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE2")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # # movement.touchSheep()
    # moveTo(indexOvelha1+BAIXO,False,2)
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE3")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # # movement.touchSheep()
    # moveTo(indexOvelha1+ESQUERDA,False,2)
    # indexOvelha1=calculateSheepMovement("T",indexOvelha1)
    # indexOvelha2=calculateSheepMovement("T",indexOvelha2)
    # debug_print("HERE4")
    # debug_print("Index Ovelha 1 "+str(indexOvelha1))
    # debug_print("Index Ovelha 2 "+str(indexOvelha2))
    # # movement.touchSheep()
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
    # # movement.scream()


# # movement.backup()
# # movement.scream()
fillStartingBoard()
# recon()
# # movement.scream()
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
# # movement.turnLeft()
# time.sleep(1)
# # movement.turnRight()
# # movement.touchSheep()
# while True:
#     checkSheep()
