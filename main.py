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
ROBOT_NORTE = -10
ROBOT_ESTE = -9
ROBOT_OESTE = -8
ROBOT_SUL = -7
PAREDE_NORTE = 10
PAREDE_SUL = 11
PAREDE_ESTE = 12
PAREDE_OESTE = 13
OVELHA = 15
indexRobot=0

tabuleiro = []
for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    tabuleiro.append(0)

for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    if (index % TAMANHO_TABULEIRO == 0):
        tabuleiro[index]+=PAREDE_OESTE
    if (index >= 30):
        tabuleiro[index] += PAREDE_NORTE
    if ((index - 5) % TAMANHO_TABULEIRO == 0):
        tabuleiro[index] += PAREDE_ESTE
    if (index < 6):
        tabuleiro[index]+=PAREDE_SUL
    else:
        tabuleiro.append(0)

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

for index in range(TAMANHO_TABULEIRO * TAMANHO_TABULEIRO):
    print(str(tabuleiro[index]) + ", ")

while True:
    time.sleep(5)
# tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
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
# colorSensor = ColorSensor()
# colorSensor.mode = 'COL-COLOR'
# while True:
#     print(colorSensor.value())

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