#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor
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
colorSensor.mode = 'COL-REFLECT'
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
    tabuleiro.append("00000")                                                           # Preencher cada posição do array. Vai ser uma string do genero "00000" e cada caracter da string diz respeito a ter ovelha, parede etc. No inicio não se sabe de nada dai começar com 00000

for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):                              # O index vai ter todas as posições de 0 a 35
    if (index % TAMANHO_TABULEIRO == 0):                                                # Se o index for 0
        tabuleiro[index] = list(tabuleiro[index])                                       # Criar uma lista de listas em cada posição VERIFICAR RUBERN
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


#Após o tabuleriro já conter as paredes das bordas, agora são colocadas as paredes laranjas e as ovelhas.
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
    if orientacao == POS_NORTE:
        ovelhaFrente = list(tabuleiro[indexRobot+CIMA])[4] == "1"
    elif orientacao == POS_ESTE:
        ovelhaFrente = list(tabuleiro[indexRobot+DIREITA])[4] == "1"
    elif orientacao == POS_SUL:
        ovelhaFrente = list(tabuleiro[indexRobot+BAIXO])[4] == "1"
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
    tank_drive.on(SpeedPercent(15), SpeedPercent(15))
    while True:
        # detetar laranja (parede)
        if (colorSensor.rgb[0] > 230 and colorSensor.rgb[1] < 60 and colorSensor.rgb[2] < 60):
            tank_drive.stop()
            tank_drive.on_for_rotations(
                SpeedPercent(-15), SpeedPercent(-15), 0.36)
            tank_drive.stop()
            return True
        # detetar preto (não é parede)
        elif (colorSensor.rgb[0] < 50 and colorSensor.rgb[1] < 50 and colorSensor.rgb[2] < 50):
            tank_drive.stop()
            tank_drive.on_for_rotations(
                SpeedPercent(-15), SpeedPercent(-15), 0.36)
            tank_drive.stop()
            return False
        # print(colorSensor.rgb)


def checkSheep():
    global sonic
    return (sonic.value() // 10) > 4 and (sonic.value() // 10) < 30                                                 


def nextSquareToCheck(quadradosDesconhecidos):
    global indexRobot
    precisaVoltarAtras = False
    for index in range(((indexRobot // 6) - 1) * 6, (indexRobot // 6) * 6):
        if index in quadradosDesconhecidos:
            precisaVoltarAtras = True
            break
    # debug_print(precisaVoltarAtras)
    #TODO: fazer verificacoes relativamente as bordas
    if indexRobot % (TAMANHO_TABULEIRO * 2) > 5:  # está nas linhas 1, 3 ou 5
        if (not precisaVoltarAtras or (precisaVoltarAtras and (indexRobot+BAIXO) not in quadradosDesconhecidos)) and indexRobot+ESQUERDA not in quadradosDesconhecidos and canGoForward(indexRobotOrientacoes):
            return ESQUERDA
        elif (not precisaVoltarAtras or (precisaVoltarAtras and (indexRobot + BAIXO) not in quadradosDesconhecidos)) and not indexRobot + ESQUERDA not in quadradosDesconhecidos and canGoForward(indexRobotOrientacoes):
            return DIREITA
        elif canGoForward(indexRobotOrientacoes):
            return BAIXO
    else:  # está nas linhas 0, 2 ou 4
        if (not precisaVoltarAtras or (precisaVoltarAtras and (indexRobot+BAIXO) not in quadradosDesconhecidos)) and indexRobot+DIREITA not in quadradosDesconhecidos and canGoForward(indexRobotOrientacoes):
            return DIREITA
        elif (not precisaVoltarAtras or (precisaVoltarAtras and (indexRobot + BAIXO) not in quadradosDesconhecidos)) and not indexRobot + DIREITA not in quadradosDesconhecidos and canGoForward(indexRobotOrientacoes):
            return ESQUERDA
        elif canGoForward(indexRobotOrientacoes):
            return BAIXO


def recon():
    global indexRobot, indexRobotOrientacoes
    indexRobot = 0
    # proximoQuadrado =
    quadradosDesconhecidos = []
    for index in range(len(tabuleiro)):
        if (DESCONHECIDO in list(tabuleiro[index])[:4]):
            quadradosDesconhecidos.append(index)
    while True:
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
            updateBoard(parede, ovelha)
        try:
            quadradosDesconhecidos.remove(indexRobot)
        except:
            pass
        proximoIndex = nextSquareToCheck(quadradosDesconhecidos)
        debug_print(proximoIndex)
        orientacao = indexRobotOrientacoes
        if proximoIndex == BAIXO:
            orientacao = 2
        elif proximoIndex == DIREITA:
            orientacao = 1
        elif proximoIndex == ESQUERDA:
            orientacao = 3
        else:
            orientacao = 0
        while (not canGoForward(indexRobotOrientacoes)):
            indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
            if(indexToLeft == tabuleiro[indexRobot].index(SEM_PAREDE)):
                turnLeft()
            else:
                turnRight()
            if indexRobotOrientacoes == orientacao and canGoForward(orientacao):
                break
        # debug_print(indexRobotOrientacoes)
        goForward()


recon()
