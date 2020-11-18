#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1,INPUT_3,INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from movement import *
import os
import time
os.system('setfont Lat15-TerminusBold14')

TAMANHO_TABULEIRO = 6
DIREITA = 1
ESQUERDA = -1
CIMA = TAMANHO_TABULEIRO
BAIXO = -TAMANHO_TABULEIRO
NORTE="N"
ESTE="E"
OESTE="W"
SUL="S"
OVELHA = "O"
ROBOT_ORIENTACOES = NORTE + ESTE + OESTE + SUL
indexRobotOrientacoes=0
indexRobot=0

tabuleiro = []
for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    tabuleiro.append("")

for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    if (index % TAMANHO_TABULEIRO == 0):
        tabuleiro[index]+=OESTE #Parede a oeste
    if (index >= 30):
        tabuleiro[index] += NORTE #Parede a norte
    if ((index - 5) % TAMANHO_TABULEIRO == 0):
        tabuleiro[index] += ESTE #Parede a este
    if (index < 6):
        tabuleiro[index]+=SUL #Parede a sul

def foundWall():
    if indexRobotOrientacoes == 0: #Virado para norte
        tabuleiro[index] += NORTE  #Parede a norte
        # try:
        #     tabuleiro[index + CIMA] += SUL  #A célula acima da atual do robot tem uma parede a sul
        #except:
        #    pass
    elif indexRobotOrientacoes == 1: #Virado para este
        tabuleiro[index] += ESTE  #Parede a este
        # if (index+DIREITA)%TAMANHO_TABULEIRO!=0:
        #     tabuleiro[
        #         index +
        #         DIREITA] += OESTE  #A célula à direita do robot tem uma parede a oeste
    elif indexRobotOrientacoes == 2: #Virado para oeste
        tabuleiro[index] += OESTE  #Parede a oeste
        # if index % TAMANHO_TABULEIRO != 0:
        #     tabuleiro[
        #         index +
        #         ESQUERDA] += ESTE  #A célula à esquerda do robot tem uma parede a este
    else: #indexRobotOrientacoes==3 // Virado para sul
        tabuleiro[index] += SUL  #Parede a sul
        # try:
        #     tabuleiro[index + BAIXO] += NORTE  #A célula abaixo da atual do robot tem uma parede a norte
        # except:
        #     pass

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
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
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



# """ ULTRASONIC"""
# sonic = UltrasonicSensor()
# sonic.mode = UltrasonicSensor.MODE_US_DIST_CM
# units = sonic.units
# while True:
#     print(str(sonic.value()//10))


"""COLOR"""
tank_drive.on(SpeedPercent(15),SpeedPercent(15))
colorSensor = ColorSensor()
colorSensor.mode = 'COL-REFLECT'
colorSensor.calibrate_white()
while True:
    if (colorSensor.rgb[0] > 240 and colorSensor.rgb[1] < 50 and colorSensor.rgb[2] < 50):
        tank_drive.stop()
        tank_drive.on_for_rotations(SpeedPercent(-15), SpeedPercent(-15), 0.36)
        tank_drive.stop()
        turnRight()
        tank_drive.on(SpeedPercent(15),SpeedPercent(15))
    #elif (colorSensor.rgb[0]<50 and colorSensor.rgb[1]<50 and colorSensor.rgb[2]<50):
        #tank_drive.stop()
        #break
    print(colorSensor.rgb)

# from ev3dev.ev3 import *
# import os
# mL = LargeMotor('outB'); mL.stop_action = 'hold'
# mR = LargeMotor('outC'); mR.stop_action = 'hold'
# print('Hello, my name is ROBERTO!')
# Sound.speak('Hello, my name is ROBERTO!').wait()
# mL.run_to_rel_pos(position_sp= 840, speed_sp = 250)
# mR.run_to_rel_pos(position_sp=-840, speed_sp = 250)
# mL.wait_while('running')
# mR.wait_while('running')