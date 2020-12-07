from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1,INPUT_3,INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor

ROTACAO = 181
VELOCIDADE=25
TAMANHO_QUADRADO = 26
DISTANCIA_FRENTE = 2.2
DISTANCIA_RECUAR=0.7
ANGULO_RODAR=90
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
tank_drive.gyro = GyroSensor()
tank_drive.gyro.calibrate()


def turnLeft():
    # tank_drive.on_for_degrees(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO)
    tank_drive.turn_degrees(speed=SpeedPercent(VELOCIDADE),target_angle=-ANGULO_RODAR)

def turnRight():
    # tank_drive.on_for_degrees(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), ROTACAO)
    tank_drive.turn_degrees(speed=SpeedPercent(VELOCIDADE),target_angle=ANGULO_RODAR)

def forwardOneSquare():
    tank_drive.on_for_rotations(SpeedPercent(VELOCIDADE), SpeedPercent(VELOCIDADE), DISTANCIA_FRENTE)

def backOneSquare():
    tank_drive.on_for_rotations(SpeedPercent(-VELOCIDADE), SpeedPercent(-VELOCIDADE), DISTANCIA_FRENTE)

def leftOneSquare():
    turnLeft()
    forwardOneSquare()

def rightOneSquare():
    turnRight()
    forwardOneSquare()

def backup():
    tank_drive.stop()
    tank_drive.on_for_rotations(
        SpeedPercent(-VELOCIDADE), SpeedPercent(-VELOCIDADE), DISTANCIA_RECUAR)
    tank_drive.stop()

def moveForwardForever():
    tank_drive.on(SpeedPercent(VELOCIDADE), SpeedPercent(VELOCIDADE))
