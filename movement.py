import time
from ev3dev2.motor import OUTPUT_B, OUTPUT_C,OUTPUT_D, SpeedPercent, MoveTank,MediumMotor
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.sound import Sound

ROTACAO = 181
VELOCIDADE=30
VELOCIDADEBRACO=30
DISTANCIA_FRENTE = 1.45
DISTANCIA_RECUAR=0.42
ANGULO_RODAR=175
SLEEP_TIME=0.25
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
braco=MediumMotor(OUTPUT_D)
touchSensor=TouchSensor()
sound=Sound()
sonic = UltrasonicSensor()
sonic.mode = UltrasonicSensor.MODE_US_DIST_CM

#Função que vira o robot para a esquerda
def turnLeft():
    tank_drive.on_for_degrees(-VELOCIDADE, VELOCIDADE, ANGULO_RODAR)

#Função que vira o robot para a direita
def turnRight():
    tank_drive.on_for_degrees(VELOCIDADE, -VELOCIDADE, ANGULO_RODAR)

#Função que faz o robot fazer um 180, virando-se para trás
def do180():
    tank_drive.on_for_degrees(VELOCIDADE, -VELOCIDADE, (ANGULO_RODAR*2))

#Função que faz o robot andar um quadrado para a frente
def forwardOneSquare():
    tank_drive.on_for_rotations(VELOCIDADE, VELOCIDADE, DISTANCIA_FRENTE)
    time.sleep(SLEEP_TIME)

#Função que faz o robot recuar um pouco, usado após ele detetar se um lado do quadrado é uma parede ou não
def backup():
    tank_drive.off()
    tank_drive.on_for_rotations(-VELOCIDADE, -VELOCIDADE, DISTANCIA_RECUAR)
    tank_drive.off()

#Função que faz o robot andar para a frente "para sempre", este para quando encontra um dos lados do quadrado
def moveForwardForever():
    tank_drive.on(VELOCIDADE, VELOCIDADE)

#Função que para o robot
def stopRobot():
    tank_drive.off(brake=True)
    time.sleep(SLEEP_TIME)

#Função que manda o braço do robot para baixo, após este estiver perto o suficiente da ovelha, para tocar na ovelha e a seguir eleva o braço para cima, após tocar na ovelha
def touchSheep():
    moveForwardForever()
    while not (sonic.value() // 10)<14:
        pass
    tank_drive.stop()
    braco.on(-VELOCIDADEBRACO)
    touchSensor.wait_for_pressed()
    braco.on_for_degrees(VELOCIDADEBRACO,80)

#Função que faz um beep, o robot faz um beep quando encontra uma ovelha
def beep():
    sound.beep()

#Função que faz o robot gritar
def scream():
    sound.play_file('/home/robot/sounds/scream.wav')

#Função que faz o robot dizer que é um falhanço, usada para admitir que este não consegue ganhar
def admitDefeat():
    sound.speak("Sou um falhanco",espeak_opts='-a 200 -s 130 -v pt')