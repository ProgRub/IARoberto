#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1,INPUT_3,INPUT_4
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
TBD = "0"
POS_NORTE = 0
POS_SUL = 2
POS_ESTE = 1
POS_OESTE=3
POS_OVELHA=4
NORTE="N"
ESTE="E"
OESTE="W"
SUL="S"
OVELHA = "1"
ROBOT_ORIENTACOES = NORTE + ESTE + SUL+ OESTE
indexRobotOrientacoes=0
indexRobot=0
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
    tabuleiro.append("00000")

for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    if (index % TAMANHO_TABULEIRO == 0):
        tabuleiro[index]=list(tabuleiro[index])
        tabuleiro[index][POS_OESTE]=PAREDE #Parede a oeste
        tabuleiro[index]="".join(tabuleiro[index])
    if (index >= 30):
        tabuleiro[index]=list(tabuleiro[index])
        tabuleiro[index] [POS_NORTE]= PAREDE #Parede a norte
        tabuleiro[index]="".join(tabuleiro[index])
    if ((index - 5) % TAMANHO_TABULEIRO == 0):
        tabuleiro[index]=list(tabuleiro[index])
        tabuleiro[index] [POS_ESTE]= PAREDE #Parede a este
        tabuleiro[index]="".join(tabuleiro[index])
    if (index < 6):
        tabuleiro[index]=list(tabuleiro[index])
        tabuleiro[index][POS_SUL]=PAREDE #Parede a sul
        tabuleiro[index]="".join(tabuleiro[index])

def updateBoard(foundWall: bool, foundSheep: bool):
    if indexRobotOrientacoes == 0: #Virado para norte
        tabuleiro[indexRobot]=list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_NORTE]= (PAREDE if foundWall else SEM_PAREDE) #Parede a norte
        tabuleiro[indexRobot]="".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + CIMA]=list(tabuleiro[indexRobot + CIMA])
        tabuleiro[indexRobot + CIMA][POS_SUL] = (PAREDE if foundWall else SEM_PAREDE)  #A célula acima da atual do robot tem uma parede a sul
        if foundSheep:
            tabuleiro[indexRobot+CIMA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + CIMA] = "".join(tabuleiro[indexRobot + CIMA])
    elif indexRobotOrientacoes == 1: #Virado para este
        tabuleiro[indexRobot]=list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_ESTE]= (PAREDE if foundWall else SEM_PAREDE)  #Parede a este
        tabuleiro[indexRobot]="".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot+
            DIREITA]=list(tabuleiro[indexRobot+
            DIREITA])
        tabuleiro[
            indexRobot +
            DIREITA] [POS_OESTE]= (PAREDE if foundWall else SEM_PAREDE)  #A célula à direita do robot tem uma parede a oeste
        if foundSheep:
            tabuleiro[indexRobot+DIREITA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot+
            DIREITA]="".join(tabuleiro[indexRobot+
            DIREITA])
    elif indexRobotOrientacoes == 2: #Virado para oeste
        tabuleiro[indexRobot]=list(tabuleiro[indexRobot])
        tabuleiro[indexRobot] [POS_OESTE]= (PAREDE if foundWall else SEM_PAREDE)  #Parede a oeste
        tabuleiro[indexRobot]="".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot +ESQUERDA]=list(tabuleiro[indexRobot +ESQUERDA])
        # A célula à esquerda do robot tem uma parede a este
        tabuleiro[indexRobot +
                  ESQUERDA][POS_ESTE] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep:
            tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + ESQUERDA] = "".join(tabuleiro[indexRobot +
            ESQUERDA])
    else: #indexRobotOrientacoes==3 // Virado para sul
        tabuleiro[indexRobot]=list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_SUL] = (PAREDE if foundWall else SEM_PAREDE)  #Parede a sul
        tabuleiro[indexRobot]="".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + BAIXO]=list(tabuleiro[indexRobot + BAIXO])
        tabuleiro[indexRobot + BAIXO] [POS_NORTE]= (PAREDE if foundWall else SEM_PAREDE)  #A célula acima da atual do robot tem uma parede a norte
        if foundSheep:
            tabuleiro[indexRobot+BAIXO][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + BAIXO] = "".join(tabuleiro[indexRobot + BAIXO])

def turnRight():
    global indexRobotOrientacoes
    movement.turnRight()
    indexRobotOrientacoes= (indexRobotOrientacoes+1)%4

def turnLeft():
    global indexRobotOrientacoes
    movement.turnLeft()
    indexRobotOrientacoes = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1

def goForward():
    global indexRobot, indexRobotOrientacoes
    if indexRobotOrientacoes == 0:
        indexRobot+=CIMA
    elif indexRobotOrientacoes == 1:
        indexRobot+=DIREITA
    elif indexRobotOrientacoes == 2:
        indexRobot+=BAIXO
    else:
        indexRobot+=ESQUERDA
    movement.forwardOneSquare()

def sidesToCheck():
    global indexRobot
    currentSquare = list(tabuleiro[indexRobot])
    sides = []
    for index in range(len(currentSquare) - 1):
        if currentSquare[index] == TBD:
            sides.append(index)
    return sides

# forwardOneSquare()
# indexRobot += CIMA
# print(indexRobot)
# backOneSquare()
# indexRobot+=BAIXO
# print(indexRobot)
# turnLeft()
# indexRobot+=ESQUERDA
# print(indexRobot)
# turnRight()
# indexRobot+=DIREITA
# print(indexRobot)

# print(", ".join(tabuleiro))

# while True:
#     time.sleep(5)
# tank_drive.on_for_rotations(SpeedPercent(-VELOCIDADE), SpeedPercent(-VELOCIDADE), 1.45*5)
# tank_drive.on_for_degrees(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), 182)
# time.sleep(2)
# tank_drive.on_for_degrees(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), 180)
# time.sleep(2)
# tank_drive.on_for_degrees(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), ROTACAO)
# time.sleep(2)
# tank_drive.on_for_degrees(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), ROTACAO)
# time.sleep(2)
# tank_drive.on_for_degrees(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO)
# time.sleep(2)
# tank_drive.on_for_degrees(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO)
# time.sleep(2)
# tank_drive.on_for_degrees(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO)
# time.sleep(2)
# tank_drive.on_for_degrees(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO)

# tank_drive.gyro = GyroSensor()
# tank_drive.gyro.calibrate()
# time.sleep(10)
# tank_drive.turn_right(SpeedPercent(VELOCIDADE), 90)
# time.sleep(2)
# tank_drive.turn_right(SpeedPercent(VELOCIDADE), 90)
# time.sleep(2)
# tank_drive.turn_right(SpeedPercent(VELOCIDADE), 90)
# time.sleep(2)
# tank_drive.turn_right(SpeedPercent(VELOCIDADE),90)
# time.sleep(2)
# tank_drive.turn_left(SpeedPercent(VELOCIDADE),90)
# time.sleep(2)
# tank_drive.turn_left(SpeedPercent(VELOCIDADE),90)
# time.sleep(2)
# tank_drive.turn_left(SpeedPercent(VELOCIDADE),90)
# time.sleep(2)
# tank_drive.turn_left(SpeedPercent(VELOCIDADE),90)

# tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
# # tank_drive.on_for_degrees(SpeedPercent(50), SpeedPercent(75), 90)
# # tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(-25), ROTACAO)
# tank_drive.on_for_rotations(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), ROTACAO,False)
# time.sleep(2)
# # tank_drive.on_for_rotations(SpeedPercent(-25), SpeedPercent(25), ROTACAO)
# tank_drive.on_for_rotations(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), ROTACAO,False)
# time.sleep(2)
# tank_drive.on_for_rotations(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO,False)
# time.sleep(2)
# tank_drive.on_for_rotations(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO,False)# Attach large motors to ports B and C
# mB = LargeMotor('outB')
# mC = LargeMotor('outC')

# Make the robot do a hard turn right (on the spot) with
# 685 deg wheel rotation (speed 40%, brake on).
# Assuming speed_sp=900 gives full speed then
# speed_sp=360 gives 40% speed
# mB.run_to_rel_pos(position_sp=685, speed_sp=360, stop_action="brake")
# mC.run_to_rel_pos(position_sp=-685, speed_sp=360, stop_action="brake")
# tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(-25),ROTACAO)
# time.sleep(2)
# tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(-25),ROTACAO)
# time.sleep(2)
# tank_drive.on_for_rotations(SpeedPercent(25), SpeedPercent(-25),ROTACAO)


def checkFrontWall():
    tank_drive.on(SpeedPercent(15),SpeedPercent(15))
    while True:
        if (colorSensor.rgb[0] > 230 and colorSensor.rgb[1] < 60 and colorSensor.rgb[2] < 60): #detetar laranja (parede)
            tank_drive.stop()
            tank_drive.on_for_rotations(SpeedPercent(-15), SpeedPercent(-15), 0.36)
            tank_drive.stop()
            return True
        elif (colorSensor.rgb[0]<50 and colorSensor.rgb[1]<50 and colorSensor.rgb[2]<50): #detetar preto (não é parede)
            tank_drive.stop()
            tank_drive.on_for_rotations(SpeedPercent(-15), SpeedPercent(-15), 0.36)
            tank_drive.stop()
            return False
        # print(colorSensor.rgb)

def checkSheep():
    return (sonic.value()//10) > 4 and (sonic.value()//10)<30

def recon():
    global indexRobot, indexRobotOrientacoes
    indexRobot=0
    while True:
        debug_print(index)
        debug_print(sidesToCheck())
        ladosVerificar=sidesToCheck()
        for lado in ladosVerificar:
            while (indexRobotOrientacoes != lado):
                turnRight()
            ovelha=checkSheep()
            parede = checkFrontWall()
            updateBoard(parede,ovelha)
        quadrado = list(tabuleiro[index])
        while (quadrado[index] == PAREDE):
            turnRight()
        goForward()
        # if (indexRobot == 5):
        #     debug_print(", ".join(tabuleiro))
        #     break
        # if(list(tabuleiro[indexRobot])[indexRobotOrientacoes]=="0"):
        #     ovelha = checkSheep()
        #     parede = checkFrontWall()
        #     updateBoard(parede,ovelha)
        #     movement.turnRight()
        #     indexRobotOrientacoes=(indexRobotOrientacoes+1)%4
        # if(list(tabuleiro[indexRobot])[indexRobotOrientacoes]=="0"):
        #     ovelha = checkSheep()
        #     parede = checkFrontWall()
        #     updateBoard(parede,ovelha)
        # movement.forwardOneSquare()
        # indexRobot += DIREITA
        # movement.turnLeft()
        # if indexRobotOrientacoes == 0:
        #     indexRobotOrientacoes = 3
        # else:
        #     indexRobotOrientacoes-=1

recon()