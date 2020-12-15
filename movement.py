import time
from ev3dev2.motor import OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank,MediumMotor
from ev3dev2.sensor.lego import  GyroSensor, TouchSensor
from ev3dev2.sound import Sound

ROTACAO = 181
VELOCIDADE=30
VELOCIDADEBRACO=30
TAMANHO_QUADRADO = 26
DISTANCIA_FRENTE = 2.2
DISTANCIA_RECUAR=0.75
ANGULO_RODAR=175
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
braco=MediumMotor(OUTPUT_D)
touchSensor=TouchSensor()


def turnLeft():
    tank_drive.on_for_degrees(-VELOCIDADE, VELOCIDADE, ANGULO_RODAR)
    # tank_drive.turn_degrees(VELOCIDADE,-ANGULO_RODAR)

def turnRight():
    tank_drive.on_for_degrees(VELOCIDADE, -VELOCIDADE, ANGULO_RODAR)
    # tank_drive.turn_degrees(VELOCIDADE,ANGULO_RODAR)

def forwardOneSquare():
    tank_drive.on_for_rotations(VELOCIDADE, VELOCIDADE, DISTANCIA_FRENTE)

def backOneSquare():
    tank_drive.on_for_rotations(VELOCIDADE, -VELOCIDADE, DISTANCIA_FRENTE)

def leftOneSquare():
    turnLeft()
    forwardOneSquare()

def rightOneSquare():
    turnRight()
    forwardOneSquare()

def backup():
    tank_drive.stop()
    tank_drive.on_for_rotations(-VELOCIDADE, -VELOCIDADE, DISTANCIA_RECUAR)
    tank_drive.stop()

def moveForwardForever():
    tank_drive.on(VELOCIDADE, VELOCIDADE)

def stopRobot():
    tank_drive.off(brake=True)
    time.sleep(0.2)

def swingArmDown():
    braco.on_for_seconds(-VELOCIDADE,1)

def swingArmUp():
    braco.on_for_seconds(VELOCIDADE,1)

def touchSheep():
    braco.on(-VELOCIDADEBRACO)
    touchSensor.wait_for_pressed()
    braco.on_for_degrees(VELOCIDADEBRACO,70)

def scream():
    sound=Sound()
    sound.play_file('/home/robot/IARoberto/sounds/scream.wav')
    sound.beep()
