from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1,INPUT_3,INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor

ROTACAO = 181
VELOCIDADE=15
TAMANHO_QUADRADO=26
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
tank_drive.gyro = GyroSensor()
tank_drive.gyro.calibrate()


def turnLeft():
    # tank_drive.on_for_degrees(SpeedPercent(-VELOCIDADE), SpeedPercent(VELOCIDADE), ROTACAO)
    tank_drive.turn_degrees(speed=SpeedPercent(VELOCIDADE),target_angle=-90)

def turnRight():
    # tank_drive.on_for_degrees(SpeedPercent(VELOCIDADE), SpeedPercent(-VELOCIDADE), ROTACAO)
    tank_drive.turn_degrees(speed=SpeedPercent(VELOCIDADE),target_angle=90)

def forwardOneSquare():
    tank_drive.on_for_rotations(SpeedPercent(VELOCIDADE), SpeedPercent(VELOCIDADE), 1.45)

def backOneSquare():
    tank_drive.on_for_rotations(SpeedPercent(-VELOCIDADE), SpeedPercent(-VELOCIDADE), 1.45)

def leftOneSquare():
    turnLeft()
    forwardOneSquare()

def rightOneSquare():
    turnRight()
    forwardOneSquare()
