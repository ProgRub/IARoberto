import time
from ev3dev2.motor import OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank,MediumMotor
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.sound import Sound

ROTACAO = 181
VELOCIDADE=30
VELOCIDADEBRACO=30
TAMANHO_QUADRADO = 26
DISTANCIA_FRENTE = 2.4
DISTANCIA_RECUAR=0.78
ANGULO_RODAR=175
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
braco=MediumMotor(OUTPUT_D)
touchSensor=TouchSensor()
sound=Sound()
sonic = UltrasonicSensor()
sonic.mode = UltrasonicSensor.MODE_US_DIST_CM


def turnLeft():
    tank_drive.on_for_degrees(-VELOCIDADE, VELOCIDADE, ANGULO_RODAR)
    # tank_drive.turn_degrees(VELOCIDADE,-ANGULO_RODAR)

def turnRight():
    tank_drive.on_for_degrees(VELOCIDADE, -VELOCIDADE, ANGULO_RODAR)
    # tank_drive.turn_degrees(VELOCIDADE,ANGULO_RODAR)

def do180():
    tank_drive.on_for_degrees(VELOCIDADE, -VELOCIDADE, (ANGULO_RODAR*2))
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
    moveForwardForever()
    while not (sonic.value() // 10)<14:
        # print(sonic.value())
        pass
    tank_drive.stop()
    braco.on(-VELOCIDADEBRACO)
    touchSensor.wait_for_pressed()
    braco.on_for_degrees(VELOCIDADEBRACO,70)
    backup()

def beep():
    sound.beep()

def scream():
    sound.play_file('/home/robot/sounds/scream.wav')

def admitDefeat():
    sound.speak("Sou um falhanço",espeak_opts='-a 200 -s 130 -v pt')