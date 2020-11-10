#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1,INPUT_3,INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor

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
OVELHA=15

tabuleiro = []

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(75), 10)
tank_drive.on_for_settings(SpeedPercent(60),SpeedPercent(30),3)

# from ev3dev.ev3 import *
# import os
# os.system('setfont Lat15-TerminusBold14')
# mL = LargeMotor('outB'); mL.stop_action = 'hold'
# mR = LargeMotor('outC'); mR.stop_action = 'hold'
# print('Hello, my name is ROBERTO!')
# Sound.speak('Hello, my name is ROBERTO!').wait()
# mL.run_to_rel_pos(position_sp= 840, speed_sp = 250)
# mR.run_to_rel_pos(position_sp=-840, speed_sp = 250)
# mL.wait_while('running')
# mR.wait_while('running')