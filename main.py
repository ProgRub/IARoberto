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
NORTE = 0
SUL = 2
ESTE = 1
OESTE = 3
POS_OVELHA = 4
OVELHA = "1"
ROBOT_ORIENTACOES = "NESW"
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
numeroOvelhas = 0
numeroMovimentosRobot = 2
tabuleiro = []
quadradosDesconhecidos = list(
    range(TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO))


"""
                    BOARD FUNCTIONS
"""

# Função que preenche o tabuleiro inicial, com as "paredes" nas bordas do tabuleiro


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
            tabuleiro[index][OESTE] = PAREDE  # Parede a oeste
            # juntar carateres com um espaço vazio para ficar uma só "palavra"
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index >= TAMANHO_LINHA_TABULEIRO*(TAMANHO_LINHA_TABULEIRO-1)):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][NORTE] = PAREDE  # Parede a norte
            tabuleiro[index] = "".join(tabuleiro[index])
        if ((index - (TAMANHO_LINHA_TABULEIRO-1)) % TAMANHO_LINHA_TABULEIRO == 0):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][ESTE] = PAREDE  # Parede a este
            tabuleiro[index] = "".join(tabuleiro[index])
        if (index < TAMANHO_LINHA_TABULEIRO):
            tabuleiro[index] = list(tabuleiro[index])
            tabuleiro[index][SUL] = PAREDE  # Parede a sul
            tabuleiro[index] = "".join(tabuleiro[index])


# Função chamada no reconhecimento para atualizar os quadrados com os estados das paredes e das ovelhas
def updateBoard(foundWall: bool, foundSheep: bool):
    global indexOvelha1, indexOvelha2, numeroOvelhas
    if indexRobotOrientacoes == NORTE:  # Virado para norte
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][NORTE] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a norte
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + CIMA] = list(tabuleiro[indexRobot + CIMA])
        # A célula acima da atual do robot tem uma parede a sul
        tabuleiro[indexRobot +
                  CIMA][SUL] = (PAREDE if foundWall else SEM_PAREDE)
        # se encontrou ovelha e no quadrado acima do robot não há uma ovelha
        if foundSheep and tabuleiro[indexRobot+CIMA][POS_OVELHA] != OVELHA:
            if indexOvelha1 == -15:  # se é a primeira ovelha a ser descoberta
                indexOvelha1 = indexRobot+CIMA
                numeroOvelhas += 1
            elif indexRobot+CIMA != indexOvelha1 and indexOvelha2 == -15:  # se é a segunda ovelha a ser descoberta
                indexOvelha2 = indexRobot+CIMA
                numeroOvelhas += 1
            tabuleiro[indexRobot+CIMA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + CIMA] = "".join(tabuleiro[indexRobot + CIMA])
    elif indexRobotOrientacoes == ESTE:  # Virado para este
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][ESTE] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a este
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot +
                  DIREITA] = list(tabuleiro[indexRobot +
                                            DIREITA])
        tabuleiro[
            indexRobot +
            DIREITA][OESTE] = (PAREDE if foundWall else SEM_PAREDE)  # A célula à direita do robot tem uma parede a oeste
        if foundSheep and tabuleiro[indexRobot+DIREITA][POS_OVELHA] != OVELHA:
            if indexOvelha1 == -15:
                indexOvelha1 = indexRobot+DIREITA
                numeroOvelhas += 1
            elif indexRobot+DIREITA != indexOvelha1 and indexOvelha2 == -15:
                indexOvelha2 = indexRobot+DIREITA
                numeroOvelhas += 1
            tabuleiro[indexRobot+DIREITA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot +
                  DIREITA] = "".join(tabuleiro[indexRobot +
                                               DIREITA])
    elif indexRobotOrientacoes == OESTE:  # Virado para oeste
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][OESTE] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a oeste
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot +
                  ESQUERDA] = list(tabuleiro[indexRobot + ESQUERDA])
        # A célula à esquerda do robot tem uma parede a este
        tabuleiro[indexRobot +
                  ESQUERDA][ESTE] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep and tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] != OVELHA:
            if indexOvelha1 == -15:
                indexOvelha1 = indexRobot+ESQUERDA
                numeroOvelhas += 1
            elif indexRobot+ESQUERDA != indexOvelha1 and indexOvelha2 == -15:
                indexOvelha2 = indexRobot+ESQUERDA
                numeroOvelhas += 1
            tabuleiro[indexRobot+ESQUERDA][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + ESQUERDA] = "".join(tabuleiro[indexRobot +
                                                             ESQUERDA])
    else:  # Virado para sul
        tabuleiro[indexRobot] = list(tabuleiro[indexRobot])
        tabuleiro[indexRobot][SUL] = (
            PAREDE if foundWall else SEM_PAREDE)  # Parede a sul
        tabuleiro[indexRobot] = "".join(tabuleiro[indexRobot])
        tabuleiro[indexRobot + BAIXO] = list(tabuleiro[indexRobot + BAIXO])
        # A célula acima da atual do robot tem uma parede a norte
        tabuleiro[indexRobot +
                  BAIXO][NORTE] = (PAREDE if foundWall else SEM_PAREDE)
        if foundSheep and tabuleiro[indexRobot+BAIXO][POS_OVELHA] != OVELHA:
            if indexOvelha1 == -15:
                indexOvelha1 = indexRobot+BAIXO
                numeroOvelhas += 1
            elif indexRobot+BAIXO != indexOvelha1 and indexOvelha2 == -15:
                indexOvelha2 = indexRobot+BAIXO
                numeroOvelhas += 1
            tabuleiro[indexRobot+BAIXO][POS_OVELHA] = OVELHA
        tabuleiro[indexRobot + BAIXO] = "".join(tabuleiro[indexRobot + BAIXO])


# Função que remove da lista de quadrados desconhecidos todos os quadrados cujo robot já conhece o estado de todos os lados, se tem parede ou não
def removeKnownSquares():
    global quadradosDesconhecidos
    for index in range(len(tabuleiro)):
        # se conhece-se todos os lados do quadrado retira-se este da lista de quadrados desconhecidos
        if (DESCONHECIDO not in list(tabuleiro[index])[:4]):
            try:
                quadradosDesconhecidos.remove(index)
            except:
                pass


"""
                    CHECKING FUNCTIONS
"""
# Função que verifica se existe parede ou ovelha à sua frente, indica se o robot pode ir para a frente


def canGoForward(orientacao, index):
    if orientacao == NORTE:
        try:
            ovelhaFrente = list(tabuleiro[index + CIMA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == ESTE:
        try:
            ovelhaFrente = list(tabuleiro[index+DIREITA])[4] == "1"
        except:
            ovelhaFrente = False
    elif orientacao == SUL:
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

# Função que verifica os lados do quadrado onde o robot está para determinar se há paredes ou não e se há uma ovelha nos arredores


def checkSides():
    global indexRobot, indexRobotOrientacoes, quadradosDesconhecidos, numeroParedes, indexOvelha2, indexOvelha1
    ladosVerificar = sidesToCheck()
    # assegura que o lado para onde o robot está virado é o primeiro a ser verificado, por questões de eficiência
    if indexRobotOrientacoes in ladosVerificar:
        aux = ladosVerificar[0]
        auxIndex = ladosVerificar.index(indexRobotOrientacoes)
        ladosVerificar[0] = indexRobotOrientacoes
        ladosVerificar[auxIndex] = aux
    recalcularPercurso = False
    for lado in ladosVerificar:
        parede = False
        ovelha = False
        # virar o robot até estar virado para o lado pretendido
        while (indexRobotOrientacoes != lado):
            indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
            if(indexToLeft == lado):
                turnLeft()
            elif(lado % 2 == indexRobotOrientacoes % 2):
                turn180()
            else:
                turnRight()
        # só se verifica se há ovelha se ainda não se descobriu as 2 ovelhas
        if indexOvelha1 == -15 or indexOvelha2 == -15:
            ovelha = checkSheep()
        if numeroParedes < 6:  # só se verifica as paredes se ainda não descobrimos as 6 paredes
            parede = checkFrontWall()
        else:
            aux = list(tabuleiro[indexRobot])
            # preenche os lados desconhecidos com o SEM_PAREDE
            for index in range(len(aux)-1):
                if aux[index] == DESCONHECIDO:
                    aux[index] = SEM_PAREDE
            tabuleiro[indexRobot] = "".join(aux)
        # verifica-se outra vez a ovelha porque por vezes o robot não apanhava à primeira vez
        if not ovelha and (indexOvelha1 == -15 or indexOvelha2 == -15):
            ovelha = checkSheep()
        if parede:
            numeroParedes += 1
        # se o robot encontrou uma parede ou uma ovelha então terá que recalcular o percurso
        if parede or (ovelha and (indexOvelha1 == -15 or indexOvelha2 == -15)):
            recalcularPercurso = True
        updateBoard(parede, ovelha)
    removeKnownSquares()
    return recalcularPercurso

# Função que verifica se tem parede à frente ou não


def checkFrontWall():
    movement.moveForwardForever()
    parede = False
    while True:
        try:
            # detetar azul claro (parede)
            if (colorSensor.rgb[0] < 30 and colorSensor.rgb[1] > 90 and colorSensor.rgb[2] > 155):
                parede = True
                break
            # detetar preto (não é parede)
            elif (colorSensor.rgb[0] < 80 and colorSensor.rgb[1] < 80 and colorSensor.rgb[2] < 80):
                break
        except:
            # detetar azul claro (parede)
            if (colorSensor.rgb[0] < 30 and colorSensor.rgb[1] > 90 and colorSensor.rgb[2] > 155):
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
    if (sonic.value() // 10) > 4 and (sonic.value() // 10) < 30:
        movement.beep()
        return True
    return False

# Função que determina e retorna o próximo quadrado a verificar, usado no reconhecimento do tabuleiro


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
    # Retorna o primeiro quadrado desconhecido cujo robot consegue gerar um percurso desde a sua posição atual até dito quadrado
    if indexRobot % (TAMANHO_LINHA_TABULEIRO * 2) <= 5:  # está nas linhas 0,2 ou 4
        if precisaIrDireita:
            for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
                if index in quadradosDesconhecidos and AEstrela(indexRobot, index, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO) != []:
                    return index
        if precisaIrEsquerda:
            for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1):
                if index in quadradosDesconhecidos and AEstrela(indexRobot, index, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO) != []:
                    return index
        if canGoForward(NORTE, indexRobot):
            return indexRobot+CIMA
        for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO-1, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, -1):
            if index in quadradosDesconhecidos and AEstrela(indexRobot, index, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO) != []:
                return index
    else:
        if precisaIrEsquerda:
            for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO-1, (indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO-1, -1):
                if index in quadradosDesconhecidos and AEstrela(indexRobot, index, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO) != []:
                    return index
        if precisaIrDireita:
            for index in range((indexRobot//TAMANHO_LINHA_TABULEIRO)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO):
                if index in quadradosDesconhecidos and AEstrela(indexRobot, index, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO) != []:
                    return index
        if canGoForward(NORTE, indexRobot):
            return indexRobot+CIMA
        for index in range(((indexRobot//TAMANHO_LINHA_TABULEIRO)+1)*TAMANHO_LINHA_TABULEIRO, ((indexRobot//TAMANHO_LINHA_TABULEIRO)+2)*TAMANHO_LINHA_TABULEIRO):
            if index in quadradosDesconhecidos and AEstrela(indexRobot, index, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO) != []:
                return index
    for index in quadradosDesconhecidos:
        if AEstrela(indexRobot, index, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO) != []:
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
    if indexRobotOrientacoes == NORTE:
        indexRobot += CIMA
    elif indexRobotOrientacoes == ESTE:
        indexRobot += DIREITA
    elif indexRobotOrientacoes == SUL:
        indexRobot += BAIXO
    else:
        indexRobot += ESQUERDA
    movement.forwardOneSquare()

# Função que roda o robot para a orientação destino passada como parâmetro


def turnTowardsOrientation(orientacaoDestino):
    global indexRobotOrientacoes, indexRobot
    while True:
        if indexRobotOrientacoes == orientacaoDestino:
            break
        indexToLeft = 3 if indexRobotOrientacoes == 0 else indexRobotOrientacoes - 1
        if indexToLeft == orientacaoDestino:
            turnLeft()
        elif orientacaoDestino % 2 == indexRobotOrientacoes % 2:
            turn180()
        else:
            turnRight()

# Função que move o robot para o indexDestino passado como parâmetro. Se paraRecon é true, ele verifica os quadrados desconhecidos que tiverem no seu percurso.


def moveTo(indexDestino, paraRecon):
    global indexRobot, tabuleiro,  quadradosDesconhecidos, numeroParedes, numeroOvelhas
    orientacaoDestino = -1
    indexDestinoIntermediario = indexDestino
    percurso = AEstrela(indexRobot, indexDestino,
                        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
    while indexRobot != indexDestino:  # enquanto o robot ainda não chegou ao seu destino
        haParede = False
        if paraRecon:
            if indexDestino == None:  # isto verifica-se se não há mais quadrados desconhecidos aos quais o robot pode chegar então acabou o reconhecimento
                return True
            if indexRobot in quadradosDesconhecidos:  # se o quadrado é desconhecido verifica-se os seus lados
                haParede = checkSides()
            # se encontrou-se as 2 ovelhas e as 6 paredes ou não há mais quadrados desconhecidos então acabou o reconhecimento
            if numeroOvelhas == 2 and (numeroParedes == 6 or len(quadradosDesconhecidos) == 0):
                return True
            # Recalcular o percurso pois encontrou uma parede (ou ovelha)
            if haParede:
                percurso = AEstrela(
                    indexRobot, indexDestino, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)
        if not haParede:  # se não encontrou parede e não precisou recalcular o percurso move-se o robot para o próximo quadrado no percurso
            try:
                indexDestinoIntermediario = percurso.pop(0)
                if (indexDestinoIntermediario + CIMA) == indexRobot:
                    orientacaoDestino = SUL
                elif (indexDestinoIntermediario + DIREITA) == indexRobot:
                    orientacaoDestino = OESTE
                elif (indexDestinoIntermediario + ESQUERDA) == indexRobot:
                    orientacaoDestino = ESTE
                elif (indexDestinoIntermediario + BAIXO) == indexRobot:
                    orientacaoDestino = NORTE
                turnTowardsOrientation(orientacaoDestino)
                goForward()
            except:  # se o percurso está vazio, o robot não encontrou um percurso para chegar ao índice destino e vai ver se há outro quadrado desconhecido ao qual pode chegar
                aux = nextSquareToCheck()
                if aux == indexDestino:  # se o próximo quadrado para verificar é o mesmo que o index destino então o robot está "trancado" e falha o reconhecimento e perde o jogo
                    return False
                else:  # caso contrário, gera-se o percurso para este novo quadrado desconhecido
                    indexDestino = aux
                    percurso = AEstrela(
                        indexRobot, indexDestino, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO)


"""
                    AUXILIARY FUNCTIONS

"""

# Função que verifica se dois quadrados, passados como parâmetros, estão adjacentes


def squaresAreAdjacent(index1, index2):
    return (index1+DIREITA) == index2 or (index1+ESQUERDA) == index2 or (index1+CIMA) == index2 or (index1+BAIXO) == index2


"""
                    BOARD RECON FUNCTION
"""

# Função que trata do reconhecimento inicial do tabuleiro


def recon():
    global indexRobot, indexRobotOrientacoes, indexOvelha1, indexOvelha2, numeroOvelhas
    indexRobot = 0
    quadradosDesconhecidos = list(range(len(tabuleiro)))
    onlyOnce = True
    while True:
        checkSides()
        # se as ovelhas estão adjacentes mete-se (temporariamente) uma parede entre elas pois não se pode verificar se realmente há. Se não houver após acabar o reconhecimento apaga-se esta parede do tabuleiro
        if onlyOnce and squaresAreAdjacent(indexOvelha1, indexOvelha2):
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
        # mesma verificação que em moveTo, indica que o reconhecimento terminou
        if numeroOvelhas == 2 and (numeroParedes == 6 or len(quadradosDesconhecidos) == 0):
            break
        indexDestino = nextSquareToCheck()
        fimRecon = moveTo(indexDestino, True)
        if fimRecon:
            break
        elif fimRecon != None and not fimRecon:  # está trancado
            return False
    if numeroParedes == 6:
        # se encontrou-se 6 paredes e as ovelhas estão adjacentes então temos que apagar a parede temporária inserida anteriormente
        if squaresAreAdjacent(indexOvelha1, indexOvelha2):
            auxList = list(tabuleiro[indexOvelha1])
            index = -15
            index2 = -15
            if(indexOvelha1+ESQUERDA) == indexOvelha2:  # ovelha 1 está à direita da ovelha 2
                index = OESTE
                index2 = ESTE
            elif(indexOvelha1+DIREITA) == indexOvelha2:  # ovelha 1 está à esquerda da ovelha 2
                index = ESTE
                index2 = OESTE
            elif(indexOvelha1+CIMA) == indexOvelha2:  # ovelha 1 está abaixo da ovelha 2
                index = NORTE
                index2 = SUL
            else:  # ovelha 1 está acima da ovelha 2
                index = SUL
                index2 = NORTE
            if(auxList[index] == PAREDE):
                auxList[index] = SEM_PAREDE
            tabuleiro[indexOvelha1] = "".join(auxList)
            auxList = list(tabuleiro[indexOvelha2])
            if(auxList[index2] == PAREDE):
                auxList[index2] = SEM_PAREDE
            tabuleiro[indexOvelha2] = "".join(auxList)
        # para todos os quadrados desconhecidos vamos mudar os lados desconhecidos para indicar que não tem parede
        for indexQuadrado in quadradosDesconhecidos:
            auxList = list(tabuleiro[indexQuadrado])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = SEM_PAREDE
            tabuleiro[indexQuadrado] = "".join(auxList)
    else:  # se não encontramos as 6 paredes então nos quadrados desconhecidos, que serão poucos, vamos mudar os desconhecidos para indicar que há paredes
        for indexQuadrado in quadradosDesconhecidos:
            auxList = list(tabuleiro[indexQuadrado])
            for index in range(4):
                if(auxList[index] == DESCONHECIDO):
                    auxList[index] = PAREDE
            tabuleiro[indexQuadrado] = "".join(auxList)
    return True


"""
                    ROBOT'S A* SEARCH
"""

# Função que faz a busca A* do indexStart para indexDestino e retorna o percurso gerado. Se não for possível chegar ao indexDestino num número de movimentos menor a numeroMaximoMovimentos, retorna-se uma lista vazia


def AEstrela(indexStart, indexDestino, numeroMaximoMovimentos):
    global tabuleiro
    custoMovimentoTabuleiro = [0] * \
        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexStart] = 1
    num = 1
    percursoEncontrado = False
    # enquanto não se fez o número máximo de movimentos expande-se a busca
    while not percursoEncontrado and num < (numeroMaximoMovimentos+1):
        percursoEncontrado = stepAEstrela(
            num, custoMovimentoTabuleiro, indexDestino)
        num += 1
    if not percursoEncontrado:  # se não encontramos percurso retorna-se uma lista vazia por questões de verificação
        return []
    percurso = [indexDestino]
    index = indexDestino
    num = custoMovimentoTabuleiro[indexDestino]
    while num > 1:  # faz-se backtracking desde o destino para o início encontrando o quadrado adjacente com valor igual a num-1 de modo a encontrar o percurso mais curto
        if custoMovimentoTabuleiro[index+ESQUERDA] == num-1 and canGoForward(OESTE, index):
            index += ESQUERDA
            percurso.append(index)
            num -= 1
        elif custoMovimentoTabuleiro[index+BAIXO] == num-1 and canGoForward(SUL, index):
            index += BAIXO
            percurso.append(index)
            num -= 1
        elif custoMovimentoTabuleiro[index+DIREITA] == num-1 and canGoForward(ESTE, index):
            index += DIREITA
            percurso.append(index)
            num -= 1
        elif custoMovimentoTabuleiro[index+CIMA] == num-1 and canGoForward(NORTE, index):
            index += CIMA
            percurso.append(index)
            num -= 1
    percurso.reverse()
    percurso.pop(0)
    return percurso

# Função que faz um "step" da busca A*, preenchendo a matriz do custo com os custos para chegar aos quadrados em questão


def stepAEstrela(num, custoMovimentoTabuleiro, objetivo):
    chegouObjetivo = False
    for index in range(len(custoMovimentoTabuleiro)):
        if custoMovimentoTabuleiro[index] == num:
            if canGoForward(SUL, index) and (index+BAIXO) >= 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
                chegouObjetivo = chegouObjetivo or (index+BAIXO) == objetivo
            if canGoForward(OESTE, index) and (index+ESQUERDA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
                chegouObjetivo = chegouObjetivo or (index+ESQUERDA) == objetivo
            if canGoForward(NORTE, index) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
                chegouObjetivo = chegouObjetivo or (index+CIMA) == objetivo
            if canGoForward(ESTE, index) and (index+DIREITA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
                chegouObjetivo = chegouObjetivo or (index+DIREITA) == objetivo
        if chegouObjetivo:
            break
    return chegouObjetivo


"""
                    AUXILIARY SHEEP MOVEMENT FUNCTIONS
"""

# Função que verifica se a ovelha pode ir para a frente


def sheepCanGoForward(orientacao, indexOvelha):
    return not list(tabuleiro[indexOvelha])[orientacao] == PAREDE


# Função que calcula o próximo index da Ovelha com base no tipo de ação que o robot efetua, se é grito a ovelha mexe-se um quadrado, se o robot tocar na ovelha esta mexe-se dois quadrados
def calculateSheepMovement(tipoAcao, indexOvelha, indexRobot):
    global tabuleiro
    if squaresAreAdjacent(indexRobot, indexOvelha):
        numeroMovimentos = 0
        movimentos = 0
        if tipoAcao == "S":  # S de scream,grita para a ovelha
            numeroMovimentos = 1
        else:  # tocou na ovelha
            numeroMovimentos = 2
        indexAnteriorOvelha = indexOvelha
        tentarOutraVez = True
        posicaoRobotRelativoOvelha = -1
        if indexRobot+DIREITA == indexOvelha:  # robot está à esquerda da ovelha
            posicaoRobotRelativoOvelha = 0
        elif indexRobot+BAIXO == indexOvelha:  # robot está acima da ovelha
            posicaoRobotRelativoOvelha = 1
        elif indexRobot+ESQUERDA == indexOvelha:  # robot está acima da ovelha
            posicaoRobotRelativoOvelha = 2
        else:  # robot está acima da ovelha
            posicaoRobotRelativoOvelha = 3
        while movimentos < numeroMovimentos:
            if indexAnteriorOvelha != indexOvelha:  # se este é o segundo movimento da ovelha vamos ver se ela pode continuar a mover-se em linha reta
                if indexAnteriorOvelha+BAIXO == indexOvelha and sheepCanGoForward(SUL, indexOvelha):
                    indexOvelha += BAIXO
                    tentarOutraVez = False
                elif indexAnteriorOvelha+DIREITA == indexOvelha and sheepCanGoForward(ESTE, indexOvelha):
                    indexOvelha += DIREITA
                    tentarOutraVez = False
                elif indexAnteriorOvelha+ESQUERDA == indexOvelha and sheepCanGoForward(OESTE, indexOvelha):
                    indexOvelha += ESQUERDA
                    tentarOutraVez = False
                elif indexAnteriorOvelha+CIMA == indexOvelha and sheepCanGoForward(NORTE, indexOvelha):
                    indexOvelha += CIMA
                    tentarOutraVez = False
            # se é o primeiro movimento da ovelha ou é o segundo mas esta não conseguia continuar em linha reta, calcula-se a próxima posição da ovelha de acordo com as regras do jogo
            if indexAnteriorOvelha == indexOvelha or tentarOutraVez:
                if posicaoRobotRelativoOvelha == 0:  # robot está à esquerda da ovelha
                    if sheepCanGoForward(ESTE, indexOvelha) and indexOvelha+DIREITA != indexRobot:
                        indexOvelha += DIREITA
                    elif sheepCanGoForward(SUL, indexOvelha) and indexOvelha+BAIXO != indexRobot:
                        indexOvelha += BAIXO
                    elif sheepCanGoForward(OESTE, indexOvelha) and indexOvelha+ESQUERDA != indexRobot:
                        indexOvelha += ESQUERDA
                    elif sheepCanGoForward(NORTE, indexOvelha) and indexOvelha+CIMA != indexRobot:
                        indexOvelha += CIMA
                elif posicaoRobotRelativoOvelha == 1:  # robot está acima da ovelha
                    if sheepCanGoForward(SUL, indexOvelha) and indexOvelha+BAIXO != indexRobot:
                        indexOvelha += BAIXO
                    elif sheepCanGoForward(OESTE, indexOvelha) and indexOvelha+ESQUERDA != indexRobot:
                        indexOvelha += ESQUERDA
                    elif sheepCanGoForward(NORTE, indexOvelha) and indexOvelha+CIMA != indexRobot:
                        indexOvelha += CIMA
                    elif sheepCanGoForward(ESTE, indexOvelha) and indexOvelha+DIREITA != indexRobot:
                        indexOvelha += DIREITA
                elif posicaoRobotRelativoOvelha == 2:  # robot está à direita da ovelha
                    if sheepCanGoForward(OESTE, indexOvelha) and indexOvelha+ESQUERDA != indexRobot:
                        indexOvelha += ESQUERDA
                    elif sheepCanGoForward(NORTE, indexOvelha) and indexOvelha+CIMA != indexRobot:
                        indexOvelha += CIMA
                    elif sheepCanGoForward(ESTE, indexOvelha) and indexOvelha+DIREITA != indexRobot:
                        indexOvelha += DIREITA
                    elif sheepCanGoForward(SUL, indexOvelha) and indexOvelha+BAIXO != indexRobot:
                        indexOvelha += BAIXO
                else:  # robot está abaixo da ovelha
                    if sheepCanGoForward(NORTE, indexOvelha) and indexOvelha+CIMA != indexRobot:
                        indexOvelha += CIMA
                    elif sheepCanGoForward(ESTE, indexOvelha) and indexOvelha+DIREITA != indexRobot:
                        indexOvelha += DIREITA
                    elif sheepCanGoForward(SUL, indexOvelha) and indexOvelha+BAIXO != indexRobot:
                        indexOvelha += BAIXO
                    elif sheepCanGoForward(OESTE, indexOvelha) and indexOvelha+ESQUERDA != indexRobot:
                        indexOvelha += ESQUERDA
            movimentos += 1
    return indexOvelha

# Função que atualiza o tabuleiro com o movimento que a ovelha fez, diminui-se no indice prévio o número de ovelhas passado como parâmetro e aumenta-se no indice novo o número de ovelhas passadas como parâmetro


def relocateSheep(indicePrevio, indiceNovo, numeroOvelhas):
    global tabuleiro
    aux = list(tabuleiro[indicePrevio])
    aux[4] = str(int(aux[4])-numeroOvelhas)
    tabuleiro[indicePrevio] = "".join(aux)
    if indiceNovo < (TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1):
        aux = list(tabuleiro[indiceNovo])
        aux[4] = str(int(aux[4])+numeroOvelhas)
        tabuleiro[indiceNovo] = "".join(aux)

# Função que movimenta a(s) ovelha(s) do indexStart para o indexDestino, com o robot a segui-la e fazendo as ações necessárias


def moveSheepTo(indexStart, indexDestino, numeroOvelhas):
    global tabuleiro, numeroMovimentosRobot
    # cópia do tabuleiro porque o AEstrelaOvelhas muda o tabuleiro durante a sua execução
    copiaTabuleiro = tabuleiro.copy()
    # obter o resultado do raciocínio do robot
    resultadoRaciocinio = AEstrelaOvelhas(
        indexStart, indexDestino, numeroOvelhas, numeroMovimentosRobot)
    tabuleiro = copiaTabuleiro.copy()  # reset do tabuleiro
    if resultadoRaciocinio == []:
        return False
    percursoOvelha = resultadoRaciocinio[0]
    percursoRobot = resultadoRaciocinio[1]
    proximoIndexRobot = resultadoRaciocinio[2]
    indexPercursoOvelha = 0
    for index in range(len(percursoRobot)):
        if proximoIndexRobot == percursoRobot[index]:
            moveTo(percursoRobot[index], False)
            # robot calcula se se ele tocar na ovelha se esta manter-se-à no percurso. Se sim então toca na ovelha
            if calculateSheepMovement("T", percursoOvelha[indexPercursoOvelha], percursoRobot[index]) in percursoOvelha:
                if percursoRobot[index]+CIMA == percursoOvelha[indexPercursoOvelha]:
                    turnTowardsOrientation(NORTE)
                elif percursoRobot[index]+DIREITA == percursoOvelha[indexPercursoOvelha]:
                    turnTowardsOrientation(ESTE)
                elif percursoRobot[index]+ESQUERDA == percursoOvelha[indexPercursoOvelha]:
                    turnTowardsOrientation(OESTE)
                else:
                    turnTowardsOrientation(SUL)
                movement.touchSheep()
                try:
                    relocateSheep(
                        percursoOvelha[indexPercursoOvelha], percursoOvelha[indexPercursoOvelha+2], numeroOvelhas)
                    indexPercursoOvelha += 2
                    proximoIndexRobot = percursoRobot[index+2]
                except:
                    index = 100
            else:  # caso contrário grita para ovelha
                movement.scream()
                try:
                    relocateSheep(
                        percursoOvelha[indexPercursoOvelha], percursoOvelha[indexPercursoOvelha+1], numeroOvelhas)
                    indexPercursoOvelha += 1
                    proximoIndexRobot = percursoRobot[index+1]
                except:
                    index = 100
                    relocateSheep(percursoOvelha[indexPercursoOvelha], percursoOvelha[len(
                        percursoOvelha)-1], numeroOvelhas)
    return True


"""
                    SHEEP'S A* SEARCH
"""

# Função que verifica se o percursoOvelha gerado pela primeira parte do AEstrelaOvelhas é válido, isto é, o robot consegue levar a ovelha no seu percurso sem que esta faça um movimento aleatório, gritando sempre


def percursoValido(percursoOvelha, custoMovimentoTabuleiro, numeroOvelhas, indexRobotPar, nivelRecursivo):
    global numeroMovimentosRobot, tabuleiro
    chegouSolucao = False
    possivelIndexRobot = indexRobotPar
    proximoIndexRobot = possivelIndexRobot
    percursoRobot = [possivelIndexRobot]
    copiaTabuleiro = tabuleiro.copy()
    for index in range(len(percursoOvelha)-1):
        nivelRecursivo += 1
        chegouSolucao = False
        possiveisProximosIndexesRobot = []
        # Verifica-se em quais posições (acima, à esquerda, à direita e abaixo da ovelha) o robot pode gritar de modo a que ovelha mantenha-se no percurso e vê-se se o robot consegue chegar a essa posição com o número de movimentos permitido (infinito se a ovelha ainda não se mexeu, 2 caso contrário)
        if percursoOvelha[index]//TAMANHO_LINHA_TABULEIRO == (percursoOvelha[index]+ESQUERDA)//TAMANHO_LINHA_TABULEIRO and calculateSheepMovement("S", percursoOvelha[index], percursoOvelha[index]+ESQUERDA) == percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado = AEstrela(
                possivelIndexRobot, percursoOvelha[index]+ESQUERDA, numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado) != 0 or possivelIndexRobot == percursoOvelha[index]+ESQUERDA:
                proximoIndexRobot = percursoOvelha[index]+ESQUERDA
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        if percursoOvelha[index]//TAMANHO_LINHA_TABULEIRO == (percursoOvelha[index]+DIREITA)//TAMANHO_LINHA_TABULEIRO and calculateSheepMovement("S", percursoOvelha[index], percursoOvelha[index]+DIREITA) == percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado = AEstrela(
                possivelIndexRobot, percursoOvelha[index]+DIREITA, numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado) != 0 or possivelIndexRobot == percursoOvelha[index]+DIREITA:
                proximoIndexRobot = percursoOvelha[index]+DIREITA
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        if calculateSheepMovement("S", percursoOvelha[index], percursoOvelha[index]+BAIXO) == percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado = AEstrela(
                possivelIndexRobot, percursoOvelha[index]+BAIXO, numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado) != 0 or possivelIndexRobot == percursoOvelha[index]+BAIXO:
                proximoIndexRobot = percursoOvelha[index]+BAIXO
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        if calculateSheepMovement("S", percursoOvelha[index], percursoOvelha[index]+CIMA) == percursoOvelha[index+1]:
            percursoRobotAteQuadradoDesejado = AEstrela(
                possivelIndexRobot, percursoOvelha[index]+CIMA, numeroMovimentosRobot)
            if len(percursoRobotAteQuadradoDesejado) != 0 or possivelIndexRobot == percursoOvelha[index]+CIMA:
                proximoIndexRobot = percursoOvelha[index]+CIMA
                possiveisProximosIndexesRobot.append(proximoIndexRobot)
        # Se encontrou-se uma possível posição para o robot guarda-se esta e avança-se para a próxima posição
        if len(possiveisProximosIndexesRobot) == 1:
            percursoRobotAteQuadradoDesejado = AEstrela(
                possivelIndexRobot, proximoIndexRobot, numeroMovimentosRobot)
            possivelIndexRobot = percursoRobotAteQuadradoDesejado[len(
                percursoRobotAteQuadradoDesejado)-1]
            relocateSheep(percursoOvelha[index],
                          percursoOvelha[index+1], numeroOvelhas)
            percursoRobot.append(possivelIndexRobot)
            numeroMovimentosRobot = 2
        # se encontramos várias posições, explora-se cada uma destas recursivamente
        elif len(possiveisProximosIndexesRobot) > 1:
            copiaCustoTabuleiro = custoMovimentoTabuleiro.copy()
            resultado = []
            posicoesInvalidas = []
            niveisFalhancos = []
            for possivelIndex in possiveisProximosIndexesRobot:
                relocateSheep(
                    percursoOvelha[index], percursoOvelha[index+1], numeroOvelhas)
                numeroMovimentosRobot = 2
                resultado = percursoValido(
                    percursoOvelha[index+1:], custoMovimentoTabuleiro, numeroOvelhas, possivelIndex, nivelRecursivo)
                if resultado[0]:  # se encontrou-se que o percurso é válido numa das procuras recursivas então acrescenta-se ao percurso do robot aquele encontrado e não se verifica as próximas posições
                    percursoRobot += resultado[1]
                    chegouSolucao = True
                    break
                else:  # se não se encontrou que o percurso era válido guarda-se o nível do percurso ao qual chegou e a posição que deu problemas
                    custoMovimentoTabuleiro = copiaCustoTabuleiro.copy()
                    posicoesInvalidas.append(resultado[3])
                    niveisFalhancos.append(resultado[2])
                    tabuleiro = copiaTabuleiro.copy()
            # se não se encontrou que o percurso era válido em nenhuma das procuras recursivas então atualiza-se a "matriz" do custo de movimento (usada para encontrar o percurso da ovelha) com um -1, de modo a não ser considerada em cálculos posteriores do percurso da ovelha, na posição inváida da procura que chegou mais longe (maior nível recursivo)
            if not chegouSolucao:
                tabuleiro = copiaTabuleiro.copy()
                custoMovimentoTabuleiro = copiaCustoTabuleiro.copy()
                maxNiveisRecursivos = max(niveisFalhancos)
                indexPosicaoInvalida = posicoesInvalidas[niveisFalhancos.index(
                    maxNiveisRecursivos)]
                custoMovimentoTabuleiro[indexPosicaoInvalida] = -1
                for indexCost in range(len(custoMovimentoTabuleiro)):
                    if custoMovimentoTabuleiro[indexCost] != -1:
                        custoMovimentoTabuleiro[indexCost] = 0
                return [False, custoMovimentoTabuleiro, nivelRecursivo, indexPosicaoInvalida]
        else:  # se não se encontrou uma posição para o robot que mantivesse a ovelha no percurso atualiza a "matriz" do custo de movimento de modo a não considerar a posição do percurso da ovelha que originou o problema
            tabuleiro = copiaTabuleiro.copy()
            for indexCost in range(len(custoMovimentoTabuleiro)):
                if custoMovimentoTabuleiro[indexCost] != -1:
                    custoMovimentoTabuleiro[indexCost] = 0
            if(index+1) == (len(percursoOvelha)-1):
                custoMovimentoTabuleiro[percursoOvelha[index]] = -1
                return [False, custoMovimentoTabuleiro, nivelRecursivo, percursoOvelha[index]]
            else:
                custoMovimentoTabuleiro[percursoOvelha[index+1]] = -1
                return [False, custoMovimentoTabuleiro, nivelRecursivo, percursoOvelha[index+1]]
            return [False, custoMovimentoTabuleiro, nivelRecursivo, percursoOvelha[index+1]]
        if chegouSolucao:
            break
    return [True, percursoRobot, nivelRecursivo, -1]


# Função que faz a busca A* do indexOvelha para indexDestino e retorna o percurso gerado. Este percurso está definido de modo a que o robot nunca "perca as ovelhas",isto é, as ovelhas não fazem movimentos aleatórios
def AEstrelaOvelhas(indexStart, indexDestino, numeroOvelhas, resetNumeroMovimentosRobot):
    global tabuleiro, indexRobot, indexOvelha1, indexOvelha2, numeroMovimentosRobot
    custoMovimentoTabuleiro = [0] * \
        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    while True:
        custoMovimentoTabuleiro[indexStart] = 1
        num = 1
        percursoEncontrado = False
        # enquanto não se fez o número máximo de movimentos (garantir que há um percurso possível) expande-se a busca
        while not percursoEncontrado and num < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO:
            percursoEncontrado = stepAEstrelaOvelhas(
                num, custoMovimentoTabuleiro, indexDestino)
            num += 1
        if not percursoEncontrado:  # se não se encontrou um percurso retorna-se uma lista vazia por questões de verificação
            return []
        percurso = [indexDestino]
        index = indexDestino
        num = custoMovimentoTabuleiro[indexDestino]
        while num > 1:  # faz-se backtracking desde o destino para o início encontrando o quadrado adjacente com valor igual a num-1 de modo a encontrar o percurso mais curto
            if (index+ESQUERDA) > -1 and custoMovimentoTabuleiro[index+ESQUERDA] == num-1 and sheepCanGoForward(OESTE, index):
                index += ESQUERDA
                percurso.append(index)
                num -= 1
            elif (index+BAIXO) > -1 and custoMovimentoTabuleiro[index+BAIXO] == num-1 and sheepCanGoForward(SUL, index):
                index += BAIXO
                percurso.append(index)
                num -= 1
            elif (index+DIREITA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+DIREITA] == num-1 and sheepCanGoForward(ESTE, index):
                index += DIREITA
                percurso.append(index)
                num -= 1
            elif (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == num-1 and sheepCanGoForward(NORTE, index):
                index += CIMA
                percurso.append(index)
                num -= 1
        percurso.reverse()
        numeroMovimentosRobot = resetNumeroMovimentosRobot
        resultado = percursoValido(
            percurso, custoMovimentoTabuleiro, numeroOvelhas, indexRobot, 0)  # verifica-se se o percurso gerado é válido, isto é, a ovelha não se movimentará aleatoriamente
        if resultado[0]:  # se o percurso é válido, resultado[0] é true e por isso guardamos o percurso que o robot efetuará
            percursoRobot = resultado[1][1:]
            break
        else:  # caso contrário, atualiza-se a "matriz" do custo do movimento de modo a considerar a posição que deu problemas e não considerarmos esta em cálculos posteriores do percurso da ovelha
            custoMovimentoTabuleiro = resultado[1]
    # retornamos o percurso da ovelha (percurso), o percurso do robot e a primeira posição que o robot deverá ocupar
    return percurso, percursoRobot, percursoRobot[0]


# Função que faz um "step" da busca A*, preenchendo a matriz do custo com os custos para chegar aos quadrados em questão
def stepAEstrelaOvelhas(num, custoMovimentoTabuleiro, objetivo):
    chegouObjetivo = False
    for index in range(len(custoMovimentoTabuleiro)):
        if custoMovimentoTabuleiro[index] == num:
            if sheepCanGoForward(SUL, index) and (index+BAIXO) >= 0 and custoMovimentoTabuleiro[index+BAIXO] == 0:
                custoMovimentoTabuleiro[index+BAIXO] = num+1
                chegouObjetivo = chegouObjetivo or (index+BAIXO) == objetivo
            if sheepCanGoForward(OESTE, index) and (index+ESQUERDA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+ESQUERDA] == 0:
                custoMovimentoTabuleiro[index+ESQUERDA] = num+1
                chegouObjetivo = chegouObjetivo or (index+ESQUERDA) == objetivo
            if sheepCanGoForward(NORTE, index) and (index+CIMA) < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO and custoMovimentoTabuleiro[index+CIMA] == 0:
                custoMovimentoTabuleiro[index+CIMA] = num+1
                chegouObjetivo = chegouObjetivo or (index+CIMA) == objetivo
            if sheepCanGoForward(ESTE, index) and (index+DIREITA)//TAMANHO_LINHA_TABULEIRO == (index//TAMANHO_LINHA_TABULEIRO) and custoMovimentoTabuleiro[index+DIREITA] == 0:
                custoMovimentoTabuleiro[index+DIREITA] = num+1
                chegouObjetivo = chegouObjetivo or (index+DIREITA) == objetivo
        if chegouObjetivo:
            break
    return chegouObjetivo


"""
                    GAME FUNCTIONS
"""

# Função que determina que ovelha está mais longe do curral, através do step do AEstrelaOvelhas de modo a ver qual ovelha chega ao curral com menos movimentos


def whichSheepEstaMaisLongeDoCurral():
    global indexOvelha1, indexOvelha2
    distanciaOvelha1ParaCurral = 1
    distanciaOvelha2ParaCurral = 1
    percursoEncontrado = False
    custoMovimentoTabuleiro = [0] * \
        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexOvelha1] = 1
    while not percursoEncontrado and distanciaOvelha1ParaCurral < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO:
        percursoEncontrado = stepAEstrelaOvelhas(
            distanciaOvelha1ParaCurral, custoMovimentoTabuleiro, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1)
        distanciaOvelha1ParaCurral += 1
    percursoEncontrado = False
    custoMovimentoTabuleiro = [0] * \
        TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    custoMovimentoTabuleiro[indexOvelha2] = 1
    while not percursoEncontrado and distanciaOvelha2ParaCurral < TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO:
        percursoEncontrado = stepAEstrelaOvelhas(
            distanciaOvelha2ParaCurral, custoMovimentoTabuleiro, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1)
        distanciaOvelha2ParaCurral += 1
    if distanciaOvelha1ParaCurral > distanciaOvelha2ParaCurral:
        return 1
    return 2

# Função que trata de juntar as ovelhas no mesmo quadrado, para levar as duas para o curral ao mesmo tempo


def connectSheep():
    global indexOvelha1, indexOvelha2, indexRobot, numeroMovimentosRobot
    # True se a ovelha mais longe é aquela em indexOvelha1
    ovelhaMaisLongeDoCurralE1 = whichSheepEstaMaisLongeDoCurral() == 1
    canConnectSheep = True
    if ovelhaMaisLongeDoCurralE1:
        # retorna true se conectou as ovelhas
        canConnectSheep = moveSheepTo(indexOvelha1, indexOvelha2, 1)
        if canConnectSheep:  # se conetou atualizamos os indexes das ovelhas para serem iguais
            indexOvelha1 = indexOvelha2
    else:
        # retorna true se conectou as ovelhas
        canConnectSheep = moveSheepTo(indexOvelha2, indexOvelha1, 1)
        if canConnectSheep:  # se conetou atualizamos os indexes das ovelhas para serem iguais
            indexOvelha2 = indexOvelha1
    return canConnectSheep

# Função chamada após o reconhecimento para o robot começar a jogar, junta as ovelhas no mesmo quadrado e depois leva-lhes juntas para o curral


def playGame():
    global indexOvelha1, indexOvelha2, tabuleiro, numeroMovimentosRobot, indexRobot
    numeroMovimentosRobot = TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
    conetouOvelhas = connectSheep()
    if conetouOvelhas: #se ele conetou as ovelhas então leva as duas para o curral e sabemos que ele só pode efetuar 2 movimentos após juntar as ovelhas
        numeroMovimentosRobot = 2
        moveSheepTo(indexOvelha1, TAMANHO_LINHA_TABULEIRO *
                    TAMANHO_LINHA_TABULEIRO-1, 2)
    else: #se não juntou as ovelhas então tem de levá-las separadas, por isso tem movimentos "infinitos" até começar a movimentar uma ovelha
        numeroMovimentosRobot = TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
        if whichSheepEstaMaisLongeDoCurral() == 2: #se a ovelha mais longe do curral é aquela em indexOvelha2 então leva-se primeiro a ovelha 1 que é a que está mais perto do curral
            consegue = moveSheepTo(
                indexOvelha1, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1, 1)
            if consegue: #se ele conseguiu levar a ovelha 1 ao curral então tenta levar a 2ª ovelha
                numeroMovimentosRobot = TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
                consegue = moveSheepTo(
                    indexOvelha2, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1, 1)
            if not consegue: #se ele não consegue levar alguma das ovelhas ao curral então admite que perdeu
                movement.admitDefeat()
        else:#se a ovelha mais longe do curral é aquela em indexOvelha1 então leva-se primeiro a ovelha 2 que é a que está mais perto do curral
            consegue = moveSheepTo(
                indexOvelha2, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1, 1)
            if consegue:#se ele conseguiu levar a ovelha 2 ao curral então tenta levar a 2ª ovelha
                numeroMovimentosRobot = TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO
                consegue = moveSheepTo(
                    indexOvelha1, TAMANHO_LINHA_TABULEIRO*TAMANHO_LINHA_TABULEIRO-1, 1)
            if not consegue:#se ele não consegue levar alguma das ovelhas ao curral então admite que perdeu
                movement.admitDefeat()


fillStartingBoard() #preenche-se as bordas do tabuleiro
terminouRecon = recon() #robot tenta fazer o reconhecimento do tabuleiro
curral = list(tabuleiro[len(tabuleiro)-1])
if (curral[ESTE] == PAREDE and curral[NORTE] == PAREDE and curral[SUL] == PAREDE and curral[OESTE] == PAREDE) or not terminouRecon: #se o curral está fechado (ovelhas não conseguem entrar) ou o robot não terminou o reconhecimento pois está trancado então admite que perdeu
    movement.admitDefeat()
else: #caso contrário ele começa a jogar
    playGame()
