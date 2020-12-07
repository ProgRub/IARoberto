#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2.button import Button
import movement
import os
import time
import sys
os.system('setfont Lat15-TerminusBold14')

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
colorSensor = ColorSensor()
colorSensor.mode = 'COL-AMBIENT'
colorSensor.calibrate_white()
sonic = UltrasonicSensor()
sonic.mode = UltrasonicSensor.MODE_US_DIST_CM
units = sonic.units
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


tabuleiro = []
for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    # Preencher cada posição do array. Vai ser uma string do genero "00000" e cada caracter da string diz respeito a ter ovelha, parede etc. No inicio não se sabe de nada dai começar com 00000
    tabuleiro.append("00000")

# O index vai ter todas as posições de 0 a 35
for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    # Se o index for 0
    if (index % TAMANHO_TABULEIRO == 0):
        # Criar uma lista de listas em cada posição VERIFICAR RUBERN
        tabuleiro[index] = list(tabuleiro[index])
        tabuleiro[index][POS_OESTE] = PAREDE  # Parede a oeste
        tabuleiro[index] = "".join(tabuleiro[index])
    if (index >= 30):
        tabuleiro[index] = list(tabuleiro[index])
        tabuleiro[index][POS_NORTE] = PAREDE  # Parede a norte
        tabuleiro[index] = "".join(tabuleiro[index])
    if ((index - 5) % TAMANHO_TABULEIRO == 0):
        tabuleiro[index] = list(tabuleiro[index])
        tabuleiro[index][POS_ESTE] = PAREDE  # Parede a este
        tabuleiro[index] = "".join(tabuleiro[index])
    if (index < 6):
        tabuleiro[index] = list(tabuleiro[index])
        tabuleiro[index][POS_SUL] = PAREDE  # Parede a sul
        tabuleiro[index] = "".join(tabuleiro[index])


# Após o tabuleriro já conter as paredes das bordas, agora são colocadas as paredes laranjas e as ovelhas.
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
        if foundSheep:
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
        if foundSheep:
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
        if foundSheep:
            tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + ESQUERDA] = "".join(tabuleiro[indexRobot +
                                                             ESQUERDA])
    else:  # indexRobotOrientacoes==3 // Virado para sul
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_SUL] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a sul
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + BAIXO] = list(tabuleiro[indexRobot + BAIXO])
        # A célula acima da atual do robot tem uma parede a norte
        tabuleiro[indexRobot +
                  BAIXO][POS_NORTE] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep:
            tabuleiro[indexRobot+BAIXO][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + BAIXO] = "".join(tabuleiro[indexRobot + BAIXO])


def turnRight():
    global indexRobotOrientacoes
    movement.turnRight()
    indexRobotOrientacoes = (indexRobotOrientacoes+1) % 4


def turnLeft():
    global indexRobotOrientacoes
    movement.turnLeft()
    indexRobotOrientacoes = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1


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


def canGoForward(orientacao):
    # TODO: fazer verificacoes relativamente as bordas
    if orientacao == POS_NORTE:
        try:
            ovelhaFrente = list(tabuleiro[indexRobot + CIMA])[4] == "1"
        except:
            pass
    elif orientacao == POS_ESTE:
        ovelhaFrente = list(tabuleiro[indexRobot+DIREITA])[4] == "1"
    elif orientacao == POS_SUL:
        try:
            ovelhaFrente = list(tabuleiro[indexRobot+BAIXO])[4] == "1"
        except:
            pass
    else:
        ovelhaFrente = list(tabuleiro[indexRobot+ESQUERDA])[4] == "1"
    return not(list(tabuleiro[indexRobot])[orientacao] == PAREDE or ovelhaFrente)


def sidesToCheck():
    global indexRobot
    currentSquare = list(tabuleiro[indexRobot])
    sides = []
    for index in range(len(currentSquare) - 1):
        if currentSquare[index] == DESCONHECIDO:
            sides.append(index)
    return sides


def checkFrontWall():
    movement.moveForwardForever()
    parede = False
    while True:
        # debug_print(colorSensor.rgb)
        # detetar verde escuro (parede)
        if (colorSensor.rgb[0] < 40 and colorSensor.rgb[1] < 90 and colorSensor.rgb[2] < 70):
            parede = True
            break
        # detetar branco (não é parede)
        elif (colorSensor.rgb[0] > 230 and colorSensor.rgb[1] > 230 and colorSensor.rgb[2] > 230):
            break
    movement.backup()
    return parede


def checkSheep():
    global sonic
    # debug_print("ULTRASONIC "+str(sonic.value()//10))
    return (sonic.value() // 10) > 15 and (sonic.value() // 10) < 40


def nextSquareToCheck(quadradosDesconhecidos):
    global indexRobot
    precisaVoltarAtras = False
    precisaIrEsquerda = False
    precisaIrDireita = False
    for index in range(((indexRobot // TAMANHO_TABULEIRO) - 1) * TAMANHO_TABULEIRO, (indexRobot // TAMANHO_TABULEIRO) * TAMANHO_TABULEIRO):
        if index in quadradosDesconhecidos:
            precisaVoltarAtras = True
            break
    for index in range((indexRobot//TAMANHO_TABULEIRO)*TAMANHO_TABULEIRO, indexRobot):
        if index in quadradosDesconhecidos:
            precisaIrEsquerda = True
            break
    if (indexRobot+1) % 6 != 0:
        for index in range(indexRobot+1, ((indexRobot//TAMANHO_TABULEIRO)+1)*TAMANHO_TABULEIRO):
            if index in quadradosDesconhecidos:
                precisaIrDireita = True
                break
    debug_print(str(precisaVoltarAtras)+" " +
                str(precisaIrEsquerda)+" "+str(precisaIrDireita))
    if indexRobot % (TAMANHO_TABULEIRO * 2) > 5:  # está nas linhas 1, 3 ou 5
        # debug_print("LINHA_IMPAR")
        if precisaVoltarAtras:
            if (indexRobot+BAIXO) in quadradosDesconhecidos and canGoForward(POS_SUL):
                return BAIXO
            else:
                debug_print(canGoForward(POS_ESTE))
                debug_print(canGoForward(POS_OESTE))
                if precisaIrDireita and (indexRobot + DIREITA) in quadradosDesconhecidos and canGoForward(POS_ESTE):
                    return DIREITA
                if precisaIrEsquerda and (indexRobot + ESQUERDA) in quadradosDesconhecidos and canGoForward(POS_OESTE):
                    return ESQUERDA
        else:
            if precisaIrDireita and (indexRobot + DIREITA) in quadradosDesconhecidos and canGoForward(POS_ESTE):
                return DIREITA
            if precisaIrEsquerda and (indexRobot + ESQUERDA) in quadradosDesconhecidos and canGoForward(POS_OESTE):
                return ESQUERDA
        if canGoForward(POS_NORTE):
            return CIMA
        else:
            if canGoForward(POS_ESTE):
                return DIREITA
            if canGoForward(POS_OESTE):
                return ESQUERDA
    else:  # está nas linhas 0, 2 ou 4
        # debug_print("LINHA PAR")
        if precisaVoltarAtras:
            if (indexRobot + BAIXO) in quadradosDesconhecidos and canGoForward(POS_SUL):
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
        if canGoForward(POS_NORTE):
            return CIMA
        else:
            if canGoForward(POS_ESTE):
                return DIREITA
            if canGoForward(POS_OESTE):
                return ESQUERDA


def removeKnownSquares(quadradosDesconhecidos):
    for index in range(len(tabuleiro)):
        if (DESCONHECIDO not in list(tabuleiro[index])[:4]):
            try:
                quadradosDesconhecidos.remove(index)
            except:
                pass


def printTabuleiro():
    aux = []
    toPrint = []
    for index in range(len(tabuleiro)):
        aux = list(tabuleiro[index])
        toPrint.append(str(index) + " N:" + aux[POS_NORTE] + " E:" + aux[POS_ESTE] +
                       " S:" + aux[POS_SUL] + " W:" + aux[POS_OESTE] + " Ovelha:" + aux[POS_OVELHA])
    debug_print(", ".join(toPrint))


def recon():
    global indexRobot, indexRobotOrientacoes
    numeroParedes = 0
    indexRobot = 0
    # proximoQuadrado =
    quadradosDesconhecidos = []
    for index in range(len(tabuleiro)):
        if (DESCONHECIDO in list(tabuleiro[index])[:4]):
            quadradosDesconhecidos.append(index)
    while True:
        printTabuleiro()
        debug_print(quadradosDesconhecidos)
        ladosVerificar = sidesToCheck()
        if indexRobotOrientacoes in ladosVerificar:
            aux = ladosVerificar[0]
            auxIndex = ladosVerificar.index(indexRobotOrientacoes)
            ladosVerificar[0] = indexRobotOrientacoes
            ladosVerificar[auxIndex] = aux
            # ladosVerificar=ladosVerificar[0]+ladosVerificar[1:].sort()
        debug_print(indexRobot)
        debug_print(ladosVerificar)
        for lado in ladosVerificar:
            while (indexRobotOrientacoes != lado):
                indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
                if(indexToLeft == lado):
                    turnLeft()
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
        if (len(quadradosDesconhecidos) == 0):
            break
        proximoIndex = nextSquareToCheck(quadradosDesconhecidos)
        debug_print(proximoIndex)
        orientacao = indexRobotOrientacoes
        if proximoIndex == BAIXO:
            orientacao = POS_SUL
        elif proximoIndex == DIREITA:
            orientacao = POS_ESTE
        elif proximoIndex == ESQUERDA:
            orientacao = POS_OESTE
        else:
            orientacao = POS_NORTE
        while True:
            if indexRobotOrientacoes == orientacao and canGoForward(indexRobotOrientacoes):
                break
            indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
            if(list(tabuleiro[indexRobot])[indexToLeft] == SEM_PAREDE and indexToLeft == orientacao):
                turnLeft()
            else:
                turnRight()
        # debug_print(indexRobotOrientacoes)
        goForward()
    # if numeroParedes == 5:

def stop():
    return 1/0

btn = Button()
btn.on_enter = stop
movement.backup()
recon()
# while True:
#     checkFrontWall()
# movement.moveForwardForever()
