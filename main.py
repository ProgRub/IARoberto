#!/usr/bin/env python3

from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
import movement
import os
import sys
import time
os.system('setfont Lat15-TerminusBold14')

TAMANHO_LINHA_TABULEIRO = 6
DIREITA = 1
ESQUERDA = -1
CIMA = TAMANHO_LINHA_TABULEIRO
BAIXO = -TAMANHO_LINHA_TABULEIRO
PAREDE = "2"
SEM_PAREDE = "1"
DESCONHECIDO = "0"
POS_NORTE = 0
POS_SUL = 2
POS_ESTE = 1
POS_OESTE = 3
POS_OVELHA = 4
OVELHA = "1"
ROBOT_ORIENTACOES ="NESW"
indexRobotOrientacoes = 0
indexRobot = 0
indexOvelha1 = -15
indexOvelha2 = -15
colorSensor = ColorSensor()
colorSensor.mode = 'COL-REFLECT'
colorSensor.calibrate_white()
sonic = UltrasonicSensor()
sonic.mode = UltrasonicSensor.MODE_US_DIST_CM
units = sonic.units
numeroParedes = 0
numeroMovimentosRobot=2
tabuleiro = []
quadradosDesconhecidos = list(
    range(TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO))

#Função que permite imprimir informação para debugging no VSCode
def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


"""
                    BOARD FUNCTIONS
"""

#Função que preenche o tabuleiro inicial, com as "paredes" nas bordas do tabuleiro
def fillStartingBoard():
    for index in range(TAMANHO_LINHA_TABULEIRO * TAMANHO_LINHA_TABULEIRO):
        # Preencher cada posição do array. Vai ser uma string do genero "00000" e cada caracter da string diz respeito a ter ovelha, parede etc. No inicio não se sabe de nada dai começar com 00000
        tabuleiro.append(DESCONHECIDO*5)

    # Definir as bordas do tabuleiro
    # O index vai ter todas as posições de 0 a TAMANHO_LINHA_TABULEIRO * TAMANHO_LINHA_TABULEIRO-1
    for index in range(TAMANHO_LINHA_TABULEIRO * TAMANHO_LINHA_TABULEIRO):
        # Se o index for 0
        if (index % TAMANHO_LINHA_TABULEIRO == 0):
            # passar string para lista para poder alterar carateres individuais
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_OESTE] = PAREDE  # Parede a oeste
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index >= TAMANHO_LINHA_TABULEIRO*(TAMANHO_LINHA_TABULEIRO-1)):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_NORTE] = PAREDE  # Parede a norte
            tabuleiro[index] = "".join(tabuleiro[index])
        if ((index - (TAMANHO_LINHA_TABULEIRO-1)) % TAMANHO_LINHA_TABULEIRO == 0):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_ESTE] = PAREDE  # Parede a este
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index < TAMANHO_LINHA_TABULEIRO):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][POS_SUL] = PAREDE  # Parede a sul
            tabuleiro[index] = "".join(tabuleiro[index])


# Função chamada no reconhecimento para atualizar os quadrados com os estados das paredes e das ovelhas
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
        if foundSheep and tabuleiro[indexRobot+CIMA][POS_OVELHA] != OVELHA:
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
        if foundSheep and tabuleiro[indexRobot+DIREITA][POS_OVELHA] != OVELHA:
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
        if foundSheep and tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] != OVELHA:
            tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + ESQUERDA] = "".join(tabuleiro[indexRobot +
                                                             ESQUERDA])
    else:  # Virado para sul
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][POS_SUL] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a sul
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + BAIXO] = list(tabuleiro[indexRobot + BAIXO])
        # A célula acima da atual do robot tem uma parede a norte
        tabuleiro[indexRobot +
                  BAIXO][POS_NORTE] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep and tabuleiro[indexRobot+BAIXO][POS_OVELHA] != OVELHA:
            tabuleiro[indexRobot+BAIXO][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + BAIXO] = "".join(tabuleiro[indexRobot + BAIXO])


# Função que simplesmente imprime o tabuleiro para facilitar debugging
def printTabuleiro():
    aux = []
    toPrint = []
    for index in range(len(tabuleiro)):
        aux = list(tabuleiro[index])
        toPrint.append(str(index) + " N:" + aux[POS_NORTE] + " E:" + aux[POS_ESTE] +
                       " S:" + aux[POS_SUL] + " W:" + aux[POS_OESTE] + " Ovelha:" + aux[POS_OVELHA])
    debug_print("\n".join(toPrint))

# Função que remove da lista de quadrados desconhecidos todos os quadrados cujo robot já conhece o estado de todos os lados, se tem parede ou não
def removeKnownSquares():
    global quadradosDesconhecidos
    for index in range(len(tabuleiro)):
        if (DESCONHECIDO not in list(tabuleiro[index])[:4]):
            try:
                quadradosDesconhecidos.remove(index)
            except:
                pass


"""
                    CHECKING FUNCTIONS
"""
# Função que verifica se existe parede ou ovelha à sua frente
def canGoForward(orientacao, index):
    if orientacao == POS_NORTE:
        try:
            ovelhaFrente = list(tabuleiro[index + CIMA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == POS_ESTE:
        try:
            ovelhaFrente = list(tabuleiro[index+DIREITA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == POS_SUL:
        try:
            ovelhaFrente = list(tabuleiro[index+BAIXO])[4] == "1"
        except:
            ovelhaFrente = False
    else:
        try:
            ovelhaFrente = list(tabuleiro[index+ESQUERDA])[4] == "1"
        except:
            ovelhaFrente = False
    return not(list(tabuleiro[index])[orientacao] == PAREDE or ovelhaFrente)


# Função que obtém os lados que é necessário verificar na posição atual, isso é, ainda são DESCONHECIDAS do robot
def sidesToCheck():
    global indexRobot
    currentSquare = list(tabuleiro[indexRobot])
    sides = []
    for index in range(len(currentSquare) - 1):
        if currentSquare[index] == DESCONHECIDO:
            sides.append(index)
    return sides

#Função que verifica os lados do quadrado onde o robot está para determinar se há paredes ou não e se há uma ovelha nos arredores
def checkSides():
    global indexRobot, indexRobotOrientacoes, quadradosDesconhecidos, numeroParedes,indexOvelha2,indexOvelha1
    ladosVerificar = sidesToCheck()
    if indexRobotOrientacoes in ladosVerificar:
        aux = ladosVerificar[0]
        auxIndex = ladosVerificar.index(indexRobotOrientacoes)
        ladosVerificar[0] = indexRobotOrientacoes
        ladosVerificar[auxIndex] = aux
        # ladosVerificar=ladosVerificar[0]+ladosVerificar[1:].sort()
    # debug_print(indexRobot)
    # debug_print(ladosVerificar)
    parede = False
    recalcularPercurso=False
    for lado in ladosVerificar:
        while (indexRobotOrientacoes != lado):
            indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
            if(indexToLeft == lado):
                turnLeft()
            elif(lado % 2 == indexRobotOrientacoes % 2):
                turn180()
            else:
                turnRight()
        ovelha = checkSheep()
        if numeroParedes<6:
            parede = checkFrontWall()
        else:
            aux=list(tabuleiro[indexRobot])
            for index in range(len(aux)-1):
                if aux[index]==DESCONHECIDO:
                    aux[index]=SEM_PAREDE
            tabuleiro[indexRobot]="".join(aux)
        if not ovelha:
            ovelha = checkSheep()
        if parede:
            numeroParedes += 1
            # debug_print("PAREDE "+str(numeroParedes))
        if parede or (ovelha and (indexOvelha1==-15 or indexOvelha2==-15)):
            recalcularPercurso=True
        updateBoard(parede, ovelha)
    removeKnownSquares()
    return recalcularPercurso

# Função que verifica se tem parede à frente ou não
def checkFrontWall():
    movement.moveForwardForever()
    parede = False
    while True:
        # debug_print(colorSensor.rgb)
        try:
            # detetar azul claro (parede)
            if (colorSensor.rgb[0] < 70 and colorSensor.rgb[1] > 200 and colorSensor.rgb[2] > 200):
                parede = True
                break
            # detetar preto (não é parede)
            elif (colorSensor.rgb[0] < 80 and colorSensor.rgb[1] < 80 and colorSensor.rgb[2] < 80):
                break
        except:
            # detetar azul claro (parede)
            if (colorSensor.rgb[0] < 70 and colorSensor.rgb[1] > 200 and colorSensor.rgb[2] > 200):
                parede = True
                break
            # detetar preto (não é parede)
            elif (colorSensor.rgb[0] < 80 and colorSensor.rgb[1] < 80 and colorSensor.rgb[2] < 80):
                break
    movement.stopRobot()
    movement.backup()
    return parede

# Função que verifica se há uma ovelha à sua frente
def checkSheep():
    global sonic
    # debug_print("ULTRASONIC "+str(sonic.value()//10))
    if (sonic.value() // 10) > 15 and (sonic.value() // 10) < 40:
        movement.beep()
        return True
    return False

#Função que determina e retorna o próximo quadrado a verificar, usado no reconhecimento do tabuleiro
def nextSquareToCheck():
    global indexRobot, tabuleiro, quadradosDesconhecidos
    precisaIrEsquerda = False
    precisaIrDireita = False
    for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, indexRobot):
        if index in quadradosDesconhecidos:
            precisaIrEsquerda = True
            break
    if (indexRobot+1) % 6 != 0:
        for index in range(indexRobot+1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
            if index in quadradosDesconhecidos:
                precisaIrDireita = True
                break
    if indexRobot % (TAMANHO_LINHA_TABULEIRO * 2) <= 5:  # está nas linhas 0,2 ou 4
        if precisaIrDireita:
            for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
                # debug_print(str(index)+": "+str(canGoForward(POS_ESTE, index+ESQUERDA))+" " + str(
                #     canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_ESTE, index+ESQUERDA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        if precisaIrEsquerda:
            # debug_print(range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1))
            for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1):
                # debug_print(str(index)+": "+str(canGoForward(POS_OESTE, index+DIREITA))+" " + str(
                #     canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_OESTE, index+DIREITA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        if canGoForward(POS_NORTE, indexRobot):
            return indexRobot+CIMA
        for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO-1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, -1):
            # debug_print(str(index)+": "+str(canGoForward(POS_OESTE, index+DIREITA))+" " + str(
            #     canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
            if index in quadradosDesconhecidos and canGoForward(POS_NORTE, index+BAIXO):
                return index
    else:
        if precisaIrEsquerda:
            for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1):
                # debug_print(str(index)+": "+str(canGoForward(POS_OESTE, index+DIREITA))+" " + str(
                #     canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_OESTE, index+DIREITA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        if precisaIrDireita:
            for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
                # debug_print(str(index)+": "+str(canGoForward(POS_ESTE, index+ESQUERDA))+" " + str(
                #     canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
                if index in quadradosDesconhecidos and list(tabuleiro[index])[4] != OVELHA and (canGoForward(POS_ESTE, index+ESQUERDA) or canGoForward(POS_NORTE, index+BAIXO) or canGoForward(POS_SUL, index+CIMA)):
                    return index
        if canGoForward(POS_NORTE, indexRobot):
            return indexRobot+CIMA
        for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO):
            # debug_print(str(index)+": "+str(canGoForward(POS_ESTE, index+ESQUERDA))+" " + str(
            #     canGoForward(POS_NORTE, index+BAIXO)) + " " + str(canGoForward(POS_SUL, index+CIMA)))
            if index in quadradosDesconhecidos and canGoForward(POS_NORTE, index+BAIXO):
                return index


"""
                    MOVEMENT FUNCTIONS
"""

# Função que vira o robot para a direita e atualiza a orientação do robot
def turnRight():
    global indexRobotOrientacoes
    movement.turnRight()
    indexRobotOrientacoes = (indexRobotOrientacoes+1) % 4

# Função que vira o robot para trás e atualiza a orientação do robot
def turn180():
    global indexRobotOrientacoes
    movement.do180()
    indexRobotOrientacoes = (indexRobotOrientacoes+2) % 4

# Função que vira o robot para a esquerda e atualiza a orientação do robot
def turnLeft():
    global indexRobotOrientacoes
    movement.turnLeft()
    indexRobotOrientacoes = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1

# Função que movimenta o robot um quadrado para a frente e atualiza indexRobot(varivel global da posicao atual do robot) que é a posicao para que vai se mover no tabuleiro
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

#Função que roda o robot para a orientação destino passada como parâmetro
def turnTowardsOrientation(orientacaoDestino):
    global indexRobotOrientacoes,indexRobot
    while True:
        # debug_print(str(orientacaoDestino)+"\n"+str(indexRobotOrientacoes))
        if indexRobotOrientacoes == orientacaoDestino:
            break
        indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
        if indexToLeft == orientacaoDestino:
            turnLeft()
        elif orientacaoDestino % 2 == indexRobotOrientacoes % 2:
            turn180()
        else:
            turnRight()

#Função que move o robot para o indexDestino passado como parâmetro. Se paraRecon é true, ele verifica os quadrados desconhecidos que tiverem no seu percurso. Número de ovelhas só é utilizado se paraRecon é true, para verificar se o reconhecimento terminou
def moveTo(indexDestino, paraRecon, numeroOvelhas):
    global indexRobot, tabuleiro,  quadradosDesconhecidos, numeroParedes
    orientacaoDestino = -1
    debug_print("Index Robot:"+str(indexRobot))
    indexDestinoIntermediario = indexDestino
    debug_print("Index Destino:"+str(indexDestinoIntermediario))
    percurso = AEstrela(indexRobot,indexDestino,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
    while indexRobot != indexDestino:
        haParede = False
        if paraRecon:
            if indexRobot in quadradosDesconhecidos:
                haParede = checkSides()
            if numeroOvelhas == 2 and (numeroParedes == 6   or len(quadradosDesconhecidos) == 0):
                return True
            if haParede:
                debug_print("RECALCULAR PERCURSO")
                percurso = AEstrela(indexRobot,indexDestino,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
        if not haParede:
            indexDestinoIntermediario = percurso.pop(0)
            if (indexDestinoIntermediario + CIMA) == indexRobot:
                orientacaoDestino = POS_SUL
            elif (indexDestinoIntermediario + DIREITA) == indexRobot:
                orientacaoDestino = POS_OESTE
            elif (indexDestinoIntermediario + ESQUERDA) == indexRobot:
                orientacaoDestino = POS_ESTE
            elif (indexDestinoIntermediario + BAIXO) == indexRobot:
                orientacaoDestino = POS_NORTE
            turnTowardsOrientation(orientacaoDestino)
            goForward()

"""
                    AUXILIARY FUNCTIONS

"""

#Função que verifica se dois quadrados, passados como parâmetros, estão adjacentes
def squaresAreAdjacent(index1,index2):
    return (index1+DIREITA) == index2 or (index1+ESQUERDA) == index2 or (index1+CIMA) == index2 or (index1+BAIXO) == index2


"""
                    BOARD RECON FUNCTION
"""

# Função que trata do reconhecimento inicial do tabuleiro
def recon():
    global indexRobot, indexRobotOrientacoes, indexOvelha1, indexOvelha2
    numeroOvelhas = 0
    indexRobot = 0
    quadradosDesconhecidos = list(range(len(tabuleiro)))
    onlyOnce = True
    while True:
        checkSides()
        numeroOvelhas = 0
        for index in range(len(tabuleiro)):  # Contar ovelhas
            aux = list(tabuleiro[index])
            if aux[4] == "1":
                numeroOvelhas += 1
                if indexOvelha1 == -15:
                    indexOvelha1 = index
                elif index != indexOvelha1 and indexOvelha2 == -15:
                    indexOvelha2 = index
        if onlyOnce and squaresAreAdjacent(indexOvelha1,indexOvelha2):
            debug_print("HERE")
            onlyOnce = False
            auxList = list(tabuleiro[indexOvelha1])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = PAREDE
            tabuleiro[indexOvelha1] = "".join(auxList)
            auxList = list(tabuleiro[indexOvelha2])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = PAREDE
            tabuleiro[indexOvelha2] = "".join(auxList)
            removeKnownSquares()
        if numeroOvelhas == 2 and (numeroParedes == 6   or len(quadradosDesconhecidos) == 0):
            break
        indexDestino = nextSquareToCheck()
        fimRecon = moveTo(indexDestino, True, numeroOvelhas)
        if fimRecon:
            break
    # debug_print(quadradosDesconhecidos)
    if numeroParedes == 6:
        if squaresAreAdjacent(indexOvelha1,indexOvelha2):
            # debug_print("Ovelha 1: "+str(indexOvelha1))
            # debug_print("Ovelha 2: "+str(indexOvelha2))
            auxList = list(tabuleiro[indexOvelha1])
            index=-15
            index2=-15
            if(indexOvelha1+ESQUERDA)==indexOvelha2:#ovelha 1 está à direita da ovelha 2
                index=POS_OESTE
                index2=POS_ESTE
            elif(indexOvelha1+DIREITA)==indexOvelha2:#ovelha 1 está à esquerda da ovelha 2
                index=POS_ESTE
                index2=POS_OESTE
            elif(indexOvelha1+CIMA)==indexOvelha2:#ovelha 1 está abaixo da ovelha 2
                index=POS_NORTE
                index2=POS_SUL
            else:#ovelha 1 está acima da ovelha 2
                index=POS_SUL
                index2=POS_NORTE
            if(auxList[index] == PAREDE):
                auxList[index] = SEM_PAREDE
            tabuleiro[indexOvelha1] = "".join(auxList)
            auxList = list(tabuleiro[indexOvelha2])
            if(auxList[index2] == PAREDE):
                auxList[index2] = SEM_PAREDE
            tabuleiro[indexOvelha2] = "".join(auxList)
        for indexQuadrado in quadradosDesconhecidos:
            auxList = list(tabuleiro[indexQuadrado])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = SEM_PAREDE
            tabuleiro[indexQuadrado] = "".join(auxList)
        # numeroOvelhas = 0
        # for index in range(len(tabuleiro)):  # Contar ovelhas
        #     aux = list(tabuleiro[index])
        #     if aux[4] == "1":
        #         numeroOvelhas += 1
        #         if indexOvelha1 == -1:
        #             indexOvelha1 = index
        #         else:
        #             indexOvelha2 = index
        # if numeroOvelhas == 1:
        #     aux = list(tabuleiro[indexOvelha1])
        #     aux[4] = "2"
        #     tabuleiro[indexOvelha1] = "".join(aux)
    # else:
    #     for quadrado in quadradosDesconhecidos:
    #         auxList = list(tabuleiro[quadrado])
    #         for index in range(4):
    #             if(auxList[index] == DESCONHECIDO):
    #                 auxList[index] = PAREDE
    #         tabuleiro[quadrado] = "".join(auxList)
    printTabuleiro()


"""
                    ROBOT'S A* SEARCH
"""

#Função que imprime a matriz de custo gerada durante o A*, para debugging
def printMatrizCusto(matrizCusto):
    index = 30
    while index > -1:
        debug_print(str(matrizCusto[index])+" "+str(matrizCusto[index+1])+" "+str(matrizCusto[index+2])+" "+str(
            matrizCusto[index+3])+" "+str(matrizCusto[index+4])+" "+str(matrizCusto[index+5]))
        index -= TAMANHO_LINHA_TABULEIRO
    debug_print(" ")

#Função que faz a busca A* do indexStart para indexDestino e retorna o percurso gerado. Se não for possível chegar ao indexDestino num número de movimentos menor a numeroMaximoMovimentos, retorna-se uma lista vazia
def AEstrela(indexStart,indexDestino,numeroMaximoMovimentos):
    global tabuleiro
    custoMovimentoTabuleiro = [0] * \
        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexStart] = 1
    num = 1
    percursoEncontrado=False
    while not percursoEncontrado and num<(numeroMaximoMovimentos+1):
        # printMatrizCusto(custoMovimentoTabuleiro)
        percursoEncontrado=stepAEstrela(num, custoMovimentoTabuleiro, indexDestino)
        num += 1
    printMatrizCusto(custoMovimentoTabuleiro)
    if not percursoEncontrado:
        return []
    percurso = [indexDestino]
    index = indexDestino
    num = custoMovimentoTabuleiro[indexDestino]
    while num > 1:
        # debug_print(index)
        # debug_print(percurso)
        if custoMovimentoTabuleiro[index+ESQUERDA] == num-1 and canGoForward(POS_OESTE,index):
            index += ESQUERDA
            percurso.append(index)
            num -= 1
        elif custoMovimentoTabuleiro[index+BAIXO] == num-1 and canGoForward(POS_SUL,index):
            index += BAIXO
            percurso.append(index)
            num -= 1
        elif custoMovimentoTabuleiro[index+DIREITA] == num-1 and canGoForward(POS_ESTE,index):
            index += DIREITA
            percurso.append(index)
            num -= 1
        elif custoMovimentoTabuleiro[index+CIMA] == num-1 and canGoForward(POS_NORTE,index):
            index += CIMA
            percurso.append(index)
            num -= 1
    percurso.reverse()
    percurso.pop(0)
    # debug_print(percurso)
    return percurso

#Função que faz um "step" da busca A*, preenchendo a matriz do custo com os custos para chegar aos quadrados em questão
def stepAEstrela(num, custoMovimentoTabuleiro, objetivo):
    chegouObjetivo = False
    for index in range(len(custoMovimentoTabuleiro)):
        if custoMovimentoTabuleiro[index] == num:
            if canGoForward(POS_SUL, index) and (index+BAIXO) >= 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
                chegouObjetivo = chegouObjetivo or (index+BAIXO) == objetivo
            if canGoForward(POS_OESTE, index) and (index+ESQUERDA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
                chegouObjetivo = chegouObjetivo or (index+ESQUERDA) == objetivo
            if canGoForward(POS_NORTE, index) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
                chegouObjetivo = chegouObjetivo or (index+CIMA) == objetivo
            if canGoForward(POS_ESTE, index) and (index+DIREITA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
                chegouObjetivo = chegouObjetivo or (index+DIREITA) == objetivo
        if chegouObjetivo:
            break
    return chegouObjetivo


"""
                    AUXILIARY SHEEP MOVEMENT FUNCTIONS
"""

#Função que verifica se a ovelha pode ir para a frente
def sheepCanGoForward(orientacao, indexOvelha):
    # if orientacao == POS_NORTE:
    #     robotAFrente = (indexOvelha + CIMA)==indexRobot
    # elif orientacao == POS_ESTE:
    #     robotAFrente = (indexOvelha + DIREITA)==indexRobot
    # elif orientacao == POS_SUL:
    #     robotAFrente = (indexOvelha + BAIXO)==indexRobot
    # else:
    #     robotAFrente = (indexOvelha + ESQUERDA)==indexRobot
    return not list(tabuleiro[indexOvelha])[orientacao] == PAREDE

#Função que determina o próximo index da ovelha, cujo index é o indexOvelha passado em parâmetro, com base na regra dos ponteiros do relógio: se não pode ir para a frente "vira-se para a direita" e tenta outra vez e assim sucessivamente
def sheepNextIndex(indexRobot, indexOvelha):
    # debug_print("Index Ovelha "+str(indexOvelha))
    if indexRobot+DIREITA == indexOvelha:#robot está à esquerda da ovelha
        if sheepCanGoForward(POS_ESTE, indexOvelha) and indexOvelha+DIREITA!=indexRobot:
            indexOvelha += DIREITA
        elif sheepCanGoForward(POS_SUL, indexOvelha) and indexOvelha+BAIXO!=indexRobot:
            indexOvelha += BAIXO
        elif sheepCanGoForward(POS_OESTE, indexOvelha)and indexOvelha+ESQUERDA!=indexRobot:
            indexOvelha += ESQUERDA
        elif sheepCanGoForward(POS_NORTE, indexOvelha)and indexOvelha+CIMA!=indexRobot:
            indexOvelha += CIMA
    elif indexRobot+BAIXO == indexOvelha: #robot está acima da ovelha
        if sheepCanGoForward(POS_SUL, indexOvelha) and indexOvelha+BAIXO!=indexRobot:
            indexOvelha += BAIXO
        elif sheepCanGoForward(POS_OESTE, indexOvelha)and indexOvelha+ESQUERDA!=indexRobot:
            indexOvelha += ESQUERDA
        elif sheepCanGoForward(POS_NORTE, indexOvelha)and indexOvelha+CIMA!=indexRobot:
            indexOvelha += CIMA
        elif sheepCanGoForward(POS_ESTE, indexOvelha) and indexOvelha+DIREITA!=indexRobot:
            indexOvelha += DIREITA
    elif indexRobot+ESQUERDA == indexOvelha: #robot está à direita da ovelha
        if sheepCanGoForward(POS_OESTE, indexOvelha)and indexOvelha+ESQUERDA!=indexRobot:
            indexOvelha += ESQUERDA
        elif sheepCanGoForward(POS_NORTE, indexOvelha)and indexOvelha+CIMA!=indexRobot:
            indexOvelha += CIMA
        elif sheepCanGoForward(POS_ESTE, indexOvelha)and indexOvelha+DIREITA!=indexRobot:
            indexOvelha += DIREITA
        elif sheepCanGoForward(POS_SUL, indexOvelha) and indexOvelha+BAIXO!=indexRobot:
            indexOvelha += BAIXO
    else: #robot está abaixo da ovelha
        if sheepCanGoForward(POS_NORTE, indexOvelha)and indexOvelha+CIMA!=indexRobot:
            indexOvelha += CIMA
        elif sheepCanGoForward(POS_ESTE, indexOvelha)and indexOvelha+DIREITA!=indexRobot:
            indexOvelha += DIREITA
        elif sheepCanGoForward(POS_SUL, indexOvelha)and indexOvelha+BAIXO!=indexRobot:
            indexOvelha += BAIXO
        elif sheepCanGoForward(POS_OESTE, indexOvelha)and indexOvelha+ESQUERDA!=indexRobot:
            indexOvelha += ESQUERDA
    return indexOvelha

#Função que calcula o próximo index da Ovelha com base no tipo de ação que o robot efetua, se é grito a ovelha mexe-se um quadrado, se o robot tocar na ovelha esta mexe-se dois quadrados
def calculateSheepMovement(tipoAcao, indexOvelha,indexRobot):
    global tabuleiro
    if squaresAreAdjacent(indexRobot,indexOvelha):
        if tipoAcao == "S":  # S de scream,grita para a ovelha
            indexOvelha = sheepNextIndex(indexRobot, indexOvelha)
        else:  # tocou na ovelha
            movimentos = 0
            while movimentos < 2:
                indexAnteriorOvelha=indexRobot
                indexOvelha = sheepNextIndex(indexRobot, indexOvelha)
                indexRobot=indexAnteriorOvelha
                movimentos += 1
            # indexAnteriorOvelha=indexOvelha
            # indexOvelha = sheepNextIndex(indexRobot, indexOvelha)
            # if indexAnteriorOvelha+BAIXO==indexOvelha and sheepCanGoForward(POS_SUL,indexOvelha,indexAnteriorOvelha):
            #     indexOvelha+=BAIXO
            # elif indexAnteriorOvelha+DIREITA==indexOvelha and sheepCanGoForward(POS_ESTE,indexOvelha,indexAnteriorOvelha):
            #     indexOvelha+=DIREITA
            # elif indexAnteriorOvelha+ESQUERDA==indexOvelha and sheepCanGoForward(POS_OESTE,indexOvelha,indexAnteriorOvelha):
            #     indexOvelha+=ESQUERDA
            # elif  sheepCanGoForward(POS_NORTE,indexOvelha,indexAnteriorOvelha):
            #     indexOvelha+=CIMA
    return indexOvelha

#Função que atualiza o tabuleiro com o movimento que a ovelha fez, diminui-se no indice prévio o número de ovelhas passado como parâmetro e aumenta-se no indice novo
def relocateSheep(indicePrevio, indiceNovo,numeroOvelhas):
    global tabuleiro
    aux = list(tabuleiro[indicePrevio])
    aux[4] = str(int(aux[4])-numeroOvelhas)
    tabuleiro[indicePrevio] = "".join(aux)
    if indiceNovo<(TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1):
        aux = list(tabuleiro[indiceNovo])
        aux[4] = str(int(aux[4])+numeroOvelhas)
        tabuleiro[indiceNovo] = "".join(aux)

#Função que movimenta a(s) ovelha(s) do indexStart para o indexDestino, com o robot a segui-la e fazendo as ações necessárias
def moveSheepTo(indexStart,indexDestino,numeroOvelhas):
    global tabuleiro,numeroMovimentosRobot
    copiaTabuleiro=tabuleiro.copy()
    resultadoRaciocinio=AEstrelaOvelhas(indexStart,indexDestino,numeroOvelhas)
    tabuleiro=copiaTabuleiro.copy()
    if resultadoRaciocinio==[]:
        return False
    percursoOvelha=resultadoRaciocinio[0]
    percursoRobot=resultadoRaciocinio[1]
    proximoIndexRobot=resultadoRaciocinio[2]
    debug_print("Percurso Ovelha: "+str(percursoOvelha))
    debug_print("Percurso Robot: "+str(percursoRobot))
    indexPercursoOvelha=0
    for index in range(len(percursoRobot)):
        # debug_print("IndexRobot: "+str(percursoRobot[index])+"\nIndexOvelha: "+str(percursoOvelha[indexPercursoOvelha])+"\nProximoIndexOvelha: "+str(calculateSheepMovement("S",percursoOvelha[indexPercursoOvelha],percursoRobot[index])))
        # debug_print("QuadradosAdjacentes: "+str(squaresAreAdjacent))
        # if squaresAreAdjacent(percursoRobot[index],percursoOvelha[indexPercursoOvelha]) and calculateSheepMovement("S",percursoOvelha[indexPercursoOvelha],percursoRobot[index]) in percursoOvelha and AEstrela(percursoRobot[index],):
        if proximoIndexRobot==percursoRobot[index]:
            # printTabuleiro()
            moveTo(percursoRobot[index],False,2)
            # debug_print(calculateSheepMovement("T",percursoOvelha[indexPercursoOvelha],percursoRobot[index]))
            if calculateSheepMovement("T",percursoOvelha[indexPercursoOvelha],percursoRobot[index]) in percursoOvelha:
                if percursoRobot[index]+CIMA==percursoOvelha[indexPercursoOvelha]:
                    # debug_print("CIMA")
                    turnTowardsOrientation(POS_NORTE)
                elif percursoRobot[index]+DIREITA==percursoOvelha[indexPercursoOvelha]:
                    # debug_print("DIREITA")
                    turnTowardsOrientation(POS_ESTE)
                elif percursoRobot[index]+ESQUERDA==percursoOvelha[indexPercursoOvelha]:
                    # debug_print("ESQUERDA")
                    turnTowardsOrientation(POS_OESTE)
                else:
                    # debug_print("BAIXO")
                    turnTowardsOrientation(POS_SUL)
                movement.touchSheep()
                relocateSheep(percursoOvelha[indexPercursoOvelha],percursoOvelha[indexPercursoOvelha+2],numeroOvelhas)
                indexPercursoOvelha+=2
                try:
                    proximoIndexRobot=percursoRobot[index+2]
                except:
                    index=100
            else:
                movement.scream()
                relocateSheep(percursoOvelha[indexPercursoOvelha],percursoOvelha[indexPercursoOvelha+1],numeroOvelhas)
                indexPercursoOvelha+=1
                try:
                    proximoIndexRobot=percursoRobot[index+1]
                except:
                    index=100
    printTabuleiro()
    return True


"""
                    SHEEP'S A* SEARCH
"""
def percursoValido(percursoOvelha,custoMovimentoTabuleiro,numeroOvelhas,indexRobotPar):
    global numeroMovimentosRobot,tabuleiro
    chegouSolucao=False
    possivelIndexRobot=indexRobotPar
    proximoIndexRobot=possivelIndexRobot
    percursoRobot=[possivelIndexRobot]
    copiaTabuleiro=tabuleiro.copy()
    for index in range(len(percursoOvelha)-1):
        chegouSolucao=False
        # printTabuleiro()
        possiveisProximosIndexesRobot=[]
        debug_print("Index Ovelha: "+str(percursoOvelha[index]))
        debug_print("Proximo index da ovelha se robot estiver a esquerda: "+str(calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+ESQUERDA)))
        debug_print("Proximo index da ovelha se robot estiver a direita: "+str(calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+DIREITA)))
        debug_print("Proximo index da ovelha se robot estiver abaixo: "+str(calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+BAIXO)))
        debug_print("Proximo index da ovelha se robot estiver acima: "+str(calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+CIMA)))
        debug_print("Index (Possivel) do Robot: "+str(possivelIndexRobot))
        if percursoOvelha[index]//TAMANHO_LINHA_TABULEIRO== (percursoOvelha[index]+ESQUERDA)//TAMANHO_LINHA_TABULEIRO and calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+ESQUERDA)==percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percursoOvelha[index]+ESQUERDA,numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado)!=0 or possivelIndexRobot==percursoOvelha[index]+ESQUERDA:
                proximoIndexRobot=percursoOvelha[index]+ESQUERDA
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        if percursoOvelha[index]//TAMANHO_LINHA_TABULEIRO== (percursoOvelha[index]+DIREITA)//TAMANHO_LINHA_TABULEIRO and calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+DIREITA)==percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percursoOvelha[index]+DIREITA,numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado)!=0 or possivelIndexRobot==percursoOvelha[index]+DIREITA:
                proximoIndexRobot=percursoOvelha[index]+DIREITA
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        if calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+BAIXO)==percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percursoOvelha[index]+BAIXO,numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado)!=0 or possivelIndexRobot==percursoOvelha[index]+BAIXO:
                proximoIndexRobot=percursoOvelha[index]+BAIXO
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        if calculateSheepMovement("S",percursoOvelha[index],percursoOvelha[index]+CIMA)==percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,percursoOvelha[index]+CIMA,numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado)!=0 or possivelIndexRobot==percursoOvelha[index]+CIMA:
                proximoIndexRobot=percursoOvelha[index]+CIMA
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        debug_print("Proximo index Robot: "+str(proximoIndexRobot))
        debug_print("Posições válidas? "+str(len(possiveisProximosIndexesRobot)))
        if len(possiveisProximosIndexesRobot)==1:
            percursoRobotAteQuadradoDesejado=AEstrela(possivelIndexRobot,proximoIndexRobot,numeroMovimentosRobot)
            possivelIndexRobot=percursoRobotAteQuadradoDesejado[len(percursoRobotAteQuadradoDesejado)-1]
            relocateSheep(percursoOvelha[index],percursoOvelha[index+1],numeroOvelhas)
            # printTabuleiro()
            percursoRobot.append(possivelIndexRobot)
            numeroMovimentosRobot=2
        elif len(possiveisProximosIndexesRobot)>1:
            copiaCustoTabuleiro=custoMovimentoTabuleiro.copy()
            resultado=[]
            for possivelIndex in possiveisProximosIndexesRobot:
                relocateSheep(percursoOvelha[index],percursoOvelha[index+1],numeroOvelhas)
                # printTabuleiro()
                numeroMovimentosRobot=2
                resultado = percursoValido(percursoOvelha[index+1:],custoMovimentoTabuleiro,numeroOvelhas,possivelIndex)
                if resultado[0]:
                    # debug_print("HERE: "+str(resultado[1]))
                    percursoRobot+=resultado[1]
                    chegouSolucao=True
                    break
                else:
                    # debug_print("HERE")
                    # printMatrizCusto(resultado[1])
                    custoMovimentoTabuleiro=copiaCustoTabuleiro.copy()
                    custoMovimentoTabuleiro[resultado[1].index(-1)]=-1
                    # printMatrizCusto(custoMovimentoTabuleiro)
                    tabuleiro=copiaTabuleiro.copy()
            if not chegouSolucao:
                tabuleiro=copiaTabuleiro.copy()
                # custoMovimentoTabuleiro=resultado[1].copy()
                for indexCost in range(len(custoMovimentoTabuleiro)):
                    if custoMovimentoTabuleiro[indexCost]!=-1:
                        custoMovimentoTabuleiro[indexCost]=0
                # custoMovimentoTabuleiro[percursoOvelha[index+1]]=-1
                # printMatrizCusto(custoMovimentoTabuleiro)
                return [False,custoMovimentoTabuleiro]
        else:
            tabuleiro=copiaTabuleiro.copy()
            for indexCost in range(len(custoMovimentoTabuleiro)):
                if custoMovimentoTabuleiro[indexCost]!=-1:
                    custoMovimentoTabuleiro[indexCost]=0
            custoMovimentoTabuleiro[percursoOvelha[index+1]]=-1
            return [False,custoMovimentoTabuleiro]
        if chegouSolucao:
            break
    return [True,percursoRobot]


#Função que faz a busca A* do indexOvelha para indexDestino e retorna o percurso gerado. Este percurso está definido de modo a que o robot nunca "perca as ovelhas",isto é, as ovelhas não fazem movimentos aleatórios
def AEstrelaOvelhas(indexStart,indexDestino,numeroOvelhas):
    global tabuleiro, indexRobot, indexOvelha1,indexOvelha2,numeroMovimentosRobot
    custoMovimentoTabuleiro = [0] * TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    while True:
        custoMovimentoTabuleiro[indexStart] = 1
        num = 1
        percursoEncontrado=False
        while not percursoEncontrado and num<TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO:
            # printMatrizCusto(custoMovimentoTabuleiro)
            percursoEncontrado=stepAEstrelaOvelhas(num, custoMovimentoTabuleiro, indexDestino)
            num += 1
        printMatrizCusto(custoMovimentoTabuleiro)
        if not percursoEncontrado:
            return []
        percurso = [indexDestino]
        index = indexDestino
        num = custoMovimentoTabuleiro[indexDestino]
        while num > 1:
            # debug_print(index)
            # debug_print(percurso)
            if (index+ESQUERDA) > -1 and custoMovimentoTabuleiro[index+ESQUERDA] == num-1  and sheepCanGoForward(POS_OESTE,index):
                index += ESQUERDA
                percurso.append(index)
                num -= 1
            elif (index+BAIXO) > -1 and custoMovimentoTabuleiro[index+BAIXO] == num-1 and sheepCanGoForward(POS_SUL,index):
                index += BAIXO
                percurso.append(index)
                num -= 1
            elif (index+DIREITA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+DIREITA] == num-1 and sheepCanGoForward(POS_ESTE,index):
                index += DIREITA
                percurso.append(index)
                num -= 1
            elif (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == num-1 and sheepCanGoForward(POS_NORTE,index):
                index += CIMA
                percurso.append(index)
                num -= 1
        percurso.reverse()
        # percurso.pop(0)
        debug_print(percurso)
        numeroMovimentosRobot=TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
        resultado=percursoValido(percurso,custoMovimentoTabuleiro,numeroOvelhas,indexRobot)
        if resultado[0]:
            percursoRobot=resultado[1][1:]
            break
        else:
            custoMovimentoTabuleiro=resultado[1]
    return percurso,percursoRobot,percursoRobot[0]


#Função que faz um "step" da busca A*, preenchendo a matriz do custo com os custos para chegar aos quadrados em questão
def stepAEstrelaOvelhas(num, custoMovimentoTabuleiro, objetivo):
    chegouObjetivo = False
    for index in range(len(custoMovimentoTabuleiro)):
        if custoMovimentoTabuleiro[index] == num:
            if sheepCanGoForward(POS_SUL, index) and (index+BAIXO) >= 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
                chegouObjetivo = chegouObjetivo or (index+BAIXO) == objetivo
            if sheepCanGoForward(POS_OESTE, index) and (index+ESQUERDA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
                chegouObjetivo = chegouObjetivo or (index+ESQUERDA) == objetivo
            if sheepCanGoForward(POS_NORTE, index) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
                chegouObjetivo = chegouObjetivo or (index+CIMA) == objetivo
            if sheepCanGoForward(POS_ESTE, index) and (index+DIREITA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
                chegouObjetivo = chegouObjetivo or (index+DIREITA) == objetivo
        if chegouObjetivo:
            break
    return chegouObjetivo

"""
                    GAME FUNCTIONS
"""

def whichSheepEstaMaisLongeDoCurral():
    global indexOvelha1, indexOvelha2
    distanciaOvelha1ParaCurral = 1
    distanciaOvelha2ParaCurral = 1
    percursoEncontrado=False
    custoMovimentoTabuleiro = [0] * TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexOvelha1]=1
    while not percursoEncontrado and distanciaOvelha1ParaCurral<TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO:
        # printMatrizCusto(custoMovimentoTabuleiro)
        percursoEncontrado=stepAEstrelaOvelhas(distanciaOvelha1ParaCurral, custoMovimentoTabuleiro, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1)
        distanciaOvelha1ParaCurral += 1
    percursoEncontrado=False
    custoMovimentoTabuleiro = [0] * TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexOvelha2]=1
    while not percursoEncontrado and distanciaOvelha2ParaCurral<TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO:
        # printMatrizCusto(custoMovimentoTabuleiro)
        percursoEncontrado=stepAEstrelaOvelhas(distanciaOvelha2ParaCurral, custoMovimentoTabuleiro, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1)
        distanciaOvelha2ParaCurral += 1
    # debug_print("Distancia Ovelha 1: "+str(distanciaOvelha1ParaCurral)+"\nIndex Ovelha 1: "+str(indexOvelha1))
    # debug_print("Distancia Ovelha 2: "+str(distanciaOvelha2ParaCurral)+"\nIndex Ovelha 2: "+str(indexOvelha2))
    if distanciaOvelha1ParaCurral > distanciaOvelha2ParaCurral:
        return 1
    return 2

#Função que trata de juntar as ovelhas no mesmo quadrado, para levar as duas para o curral ao mesmo tempo
def connectSheep():
    global indexOvelha1, indexOvelha2, indexRobot,numeroMovimentosRobot
    # determinar ovelha mais perto
    ovelhaMaisLongeDoCurralE1 = whichSheepEstaMaisLongeDoCurral()==1 #True se a ovelha mais longe é aquela em indexOvelha1
    # debug_print("Distancia Ovelha 1: "+str(distanciaOvelha1ParaCurral)+"\nIndex Ovelha 1: "+str(indexOvelha1))
    # debug_print("Distancia Ovelha 2: "+str(distanciaOvelha2ParaCurral)+"\nIndex Ovelha 2: "+str(indexOvelha2))
    # debug_print(ovelhaMaisLongeDoCurralE1)
    canConnectSheep=True
    if ovelhaMaisLongeDoCurralE1:
        canConnectSheep=moveSheepTo(indexOvelha1,indexOvelha2,1)
        indexOvelha1=indexOvelha2
    else:
        canConnectSheep=moveSheepTo(indexOvelha2,indexOvelha1,1)
        indexOvelha2=indexOvelha1
    return canConnectSheep

#Função chamada após o reconhecimento para o robot começar a jogar, junta as ovelhas no mesmo quadrado e depois leva-lhes juntas para o curral
def playGame():
    global indexOvelha1, indexOvelha2, tabuleiro,numeroMovimentosRobot,indexRobot
    numeroMovimentosRobot=TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    conetouOvelhas=connectSheep()
    debug_print("Conetou Ovelhas: "+str(conetouOvelhas))
    if conetouOvelhas:
        numeroMovimentosRobot=2
        moveSheepTo(indexOvelha1,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1,2)
    else:
        numeroMovimentosRobot=TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
        if whichSheepEstaMaisLongeDoCurral()==2:
            moveSheepTo(indexOvelha1,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1,1)
            numeroMovimentosRobot=TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
            moveSheepTo(indexOvelha2,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1,1)
        else:
            moveSheepTo(indexOvelha2,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1,1)
            numeroMovimentosRobot=TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
            moveSheepTo(indexOvelha1,TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1,1)

fillStartingBoard()
# recon()
indexRobot=0
indexOvelha1 = 6
indexOvelha2 = 30
aux = list(tabuleiro[indexOvelha1])
aux[4] = "1"
tabuleiro[indexOvelha1] = "".join(aux)
aux = list(tabuleiro[indexOvelha2])
aux[4] = "1"
tabuleiro[indexOvelha2] = "".join(aux)
aux = list(tabuleiro[32])
aux[POS_OESTE] = PAREDE
tabuleiro[32] = "".join(aux)
aux = list(tabuleiro[26])
aux[POS_OESTE] = PAREDE
tabuleiro[26] = "".join(aux)
aux = list(tabuleiro[20])
aux[POS_OESTE] = PAREDE
tabuleiro[20] = "".join(aux)
aux = list(tabuleiro[31])
aux[POS_ESTE] = PAREDE
tabuleiro[31] = "".join(aux)
aux = list(tabuleiro[25])
aux[POS_ESTE] = PAREDE
tabuleiro[25] = "".join(aux)
aux = list(tabuleiro[19])
aux[POS_SUL] = PAREDE
aux[POS_ESTE] = PAREDE
tabuleiro[19] = "".join(aux)
aux = list(tabuleiro[29])
aux[POS_SUL] = PAREDE
tabuleiro[29] = "".join(aux)
aux = list(tabuleiro[28])
aux[POS_SUL] = PAREDE
tabuleiro[28] = "".join(aux)
aux = list(tabuleiro[13])
aux[POS_NORTE] = PAREDE
tabuleiro[13] = "".join(aux)
aux = list(tabuleiro[23])
aux[POS_NORTE] = PAREDE
tabuleiro[23] = "".join(aux)
aux = list(tabuleiro[22])
aux[POS_NORTE] = PAREDE
tabuleiro[22] = "".join(aux)
# for index in range(len(tabuleiro)):
#     aux=list(tabuleiro[index])
#     for index in range(len(aux)-1):
#         if aux[index]==DESCONHECIDO:
#             aux[index]=SEM_PAREDE
#     tabuleiro[index]="".join(aux)
# movement.scream()
curral=list(tabuleiro[len(tabuleiro)-1])
if curral[POS_ESTE]==PAREDE and curral[POS_NORTE]==PAREDE and curral[POS_SUL]==PAREDE and curral[POS_OESTE]==PAREDE:
    # movement.admitDefeat()
    pass
else:
    playGame()
# movement.turnLeft()
# time.sleep(1)
# movement.turnRight()
# movement.touchSheep()
# while True:
#     checkSheep()
