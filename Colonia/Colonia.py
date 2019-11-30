import os
import random
import sys
import time
import pygame
#py colonia.py LABIRINTO.txt PIXELS CICLOS FORMIGAS VERSÃO TAXAEVAPORAÇÃO TAXAFEROMONIO
pygame.init()  # InniciaPygame

inicial = millis = int(round(time.time() * 1000))

if len(sys.argv) > 3:
    NC = int(sys.argv[3])  # Número de Cíclos
else:
    NC = 10
if len(sys.argv) > 4:
    NF = int(sys.argv[4])   # Número de Formigas
else:
    NF = 5
if len(sys.argv) > 2:
    px = int(sys.argv[2])   # Tamanho do pixel
else:
    px = 1
if len(sys.argv) > 5:
    ver = sys.argv[5]
else:
    ver = "-v1"
if len(sys.argv) > 1:
    lab = sys.argv[1]
else:
    lab = "m1.txt"

FeromInit = 50  # Valor inicial de feromônio
FeromMin = 1  # Valor minimo de ferômonio
FeromMax = 300  # Valor maximo de feromônio

if len(sys.argv) > 7:
    FeromRate = sys.argv[7]
else:
    FeromRate = 10  # Taxa de feromônio
if len(sys.argv) > 6:
    EvapoRate = sys.argv[6]
else:
    EvapoRate = 3  # Taxa de evaporação
Plus = 2  # Bonificação para caminhos menores


# -------Funções da Formiga-------------------

class Ant:

    def __init__(self, origem, objetivo):

        self.posJ = origem[0]
        self.posI = origem[1]
        self.ObjetivoJ = objetivo[0]
        self.ObjetivoI = objetivo[1]
        self.PosDispo = []
        self.Caminho = []
        self.iteracao = 0
        self.no = []

        self.Caminho.append([self.posJ, self.posI])

    def come(self):
        while (self.Caminho[-1] is not self.no[-1]):
            self.Caminho.pop()
        self.posJ = self.Caminho[-1][0]
        self.posI = self.Caminho[-1][1]
        if (self.fechado):
            self.no.pop()

    def reeset(self, origem):
        self.posJ = origem[0]
        self.posI = origem[1]
        self.PosDispo.clear()
        self.Caminho.clear()
        self.no = []
        self.Caminho.append([self.posJ, self.posI])

    def andar(self, proximo):
        self.posJ = proximo[0]
        self.posI = proximo[1]
        self.Caminho.append([self.posJ, self.posI])
        self.PosDispo.clear()

    def find(self):
        if ((self.posI == self.ObjetivoI) and (self.posJ == self.ObjetivoJ)):
            return True
        else:
            return False

    def caminhoLivre(self, matrix):

        if (matrix.PathMatrix[self.posI][self.posJ + 1] == 0 or matrix.PathMatrix[self.posI][self.posJ + 1] == 3):
            self.PosDispo.append([self.posJ + 1, self.posI])

        if (matrix.PathMatrix[self.posI][self.posJ - 1] == 0 or matrix.PathMatrix[self.posI][self.posJ - 1] == 3):
            self.PosDispo.append([self.posJ - 1, self.posI])

        if (matrix.PathMatrix[self.posI + 1][self.posJ] == 0 or matrix.PathMatrix[self.posI + 1][self.posJ] == 3):
            self.PosDispo.append([self.posJ, self.posI + 1])

        if (matrix.PathMatrix[self.posI - 1][self.posJ] == 0 or matrix.PathMatrix[self.posI - 1][self.posJ] == 3):
            self.PosDispo.append([self.posJ, self.posI - 1])

        if ([self.ObjetivoJ, self.ObjetivoI] in self.PosDispo):
            self.PosDispo.clear()
            self.posI = self.ObjetivoI
            self.posJ = self.ObjetivoJ
            self.Caminho.append([self.posJ, self.posI])
            return

    def fechado(self):
        if (len(self.PosDispo) == 0 and (not self.find())):
            return True
        else:
            return False

    def choose(self, mapa):
        if (not self.find()):
            feromonios = []
            sum = 0

            if (len(self.PosDispo) == 1):
                self.andar(self.PosDispo[0])

            elif (len(self.PosDispo) == 2):
                self.no.append(self.Caminho[-1])
                for pnt in self.PosDispo:
                    feromonios.append(mapa.FeromonMatrix[pnt[1]][pnt[0]])
                    sum += mapa.FeromonMatrix[pnt[1]][pnt[0]]

                val = random.randint(1, sum)
                intervalo1 = feromonios[0]
                intervalo2 = sum
                if (val in range(1, intervalo1 + 1)):
                    self.andar(self.PosDispo[0])
                else:
                    self.andar(self.PosDispo[1])
            else:
                self.no.append(self.Caminho[-1])

                for pnt in self.PosDispo:
                    feromonios.append(mapa.FeromonMatrix[pnt[1]][pnt[0]])
                    sum += mapa.FeromonMatrix[pnt[1]][pnt[0]]

                val = random.randint(1, sum)
                intervalo1 = feromonios[0]
                intervalo2 = feromonios[1] + feromonios[0]

                if (val in range(1, intervalo1 + 1)):
                    self.andar(self.PosDispo[0])
                elif (val in range(intervalo1 + 1, intervalo2 + 1)):
                    self.andar(self.PosDispo[1])
                else:
                    self.andar(self.PosDispo[2])


# -------Funções do Labirinto-------------------

class Labrinth:

    def __init__(self, file):
        f = open(file, 'r')
        f_content = f.readlines()
        self.PathMatrix = []
        self.FeromonMatrix = []
        self.pnt_init = []
        self.pnt_end = []

        matrix1 = []
        matrix2 = []
        matrix3 = []

        for i in f_content:
            for j in i:
                if (j == ' '):
                    matrix2.append(0)
                elif (j == 'S'):
                    matrix2.append(2)
                elif (j == 'E'):
                    matrix2.append(3)
                else:
                    matrix2.append(1)
            aux = matrix2.copy()
            matrix1.append(aux)
            matrix2.clear()

        f.close()

        for line in matrix1:
            for i in range(0, len(line), 2):
                matrix2.append(line[i])
            aux = matrix2.copy()
            matrix3.append(aux)
            matrix2.clear()

        self.PathMatrix = matrix3.copy()
        matrix3.clear()

        for i in self.PathMatrix:
            if (2 in i):
                self.pnt_init.append(i.index(2))
                self.pnt_init.append(self.PathMatrix.index(i))
            if (3 in i):
                self.pnt_end.append(i.index(3))
                self.pnt_end.append(self.PathMatrix.index(i))
            for j in i:
                if (j == 1):
                    matrix2.append(0)
                else:
                    matrix2.append(FeromInit)

            aux = matrix2.copy()
            self.FeromonMatrix.append(aux)
            matrix2.clear()

    def Atualizapath(self, Formiga):
        posI = Formiga.Caminho[-1][1]
        posJ = Formiga.Caminho[-1][0]
        self.PathMatrix[posI][posJ] = 4

    def CleanTrail(self, Formiga):
        for pnt in Formiga.Caminho:
            if (self.PathMatrix[pnt[1]][pnt[0]] == 4):
                self.PathMatrix[pnt[1]][pnt[0]] = 0

    def EvaporaFerom(self):
        for l in self.FeromonMatrix:
            for j in range(len(l)):
                if (l[j] > FeromMin):
                    l[j] = l[j] - EvapoRate
                    if (l[j] < FeromMin):
                        l[j] = FeromMin

    def AtualizaFerom(self, Formiga, plus):

        for pnt in Formiga.Caminho:
            if (self.FeromonMatrix[pnt[1]][pnt[0]] < FeromMax):
                self.FeromonMatrix[pnt[1]][pnt[0]] = self.FeromonMatrix[pnt[1]][pnt[0]] + FeromRate + plus
                if (self.FeromonMatrix[pnt[1]][pnt[0]] > FeromMax):
                    self.FeromonMatrix[pnt[1]][pnt[0]] = FeromMax

    def print(self):
        print("Labirinto:")
        print("\n")
        for i in self.PathMatrix:
            print(i)
        print("\n")
        print("Matrix de Feromonio:")
        print("\n")
        for i in self.FeromonMatrix:
            print(i)
        print("\n")

    def limpaBeco(self):
        for i in range(len(self.PathMatrix)):
            for j in range(len(self.PathMatrix[0])):
                if(self.PathMatrix[j][i] == 4):
                    self.PathMatrix[j][i] = 0

# -------Funções do Algoritmo-------------------

def print_result(formiga, map, index):
    if (formiga.find()):
        print("Caminho da Formiga " + str(index) + " : "),
        print("Chegou")
        print("Interações:", end=" ")
        print(formiga.iteracao)
        map.print()
        print("Caminho Resultado:", end=" ")
        for i in range(10):
            print(formiga.Caminho[i], end=" ")

    if (formiga.fechado()):
        print("Caminho da Formiga " + str(index) + " : "),
        print("Bateu")
        print("Posição:", end=" ")
        print(formiga.Caminho[-1])
        print("Interações:", end=" ")
        print(formiga.iteracao)


def printaBest(formiga, m2, mferomonio):
    tela = pygame.display.set_mode((len(m2) * px, len(m2) * px))
    a = 255 / (FeromMax - FeromMin)

    for i in range(len(m2)):
        for j in range(len(m2[0])):
            x = mferomonio[i][j]
            y = int(a * x - FeromMin)

            if m2[i][j] == 1:
                pygame.draw.rect(tela, (255, 255, 255), [j * px, i * px, px, px])
            elif m2[i][j] == 2:
                pygame.draw.rect(tela, (0, 0, 255), [j * px, i * px, px, px])
            if mferomonio[i][j] > 0:
                pygame.draw.rect(tela, (y, 0, 0), [j * px, i * px, px, px])
            if m2[i][j] == 4:
                pygame.draw.rect(tela, (202, 205, 0), [j * px, i * px, px, px])



    pygame.draw.rect(tela, (255, 255, 0), [formiga.ObjetivoJ * px, formiga.ObjetivoI * px, px, px])
    #pygame.draw.rect(tela, (0, 255, 0), [formiga.posJ * px, formiga.posI * px, px, px])
    pygame.display.update()

def PRINTA(formiga, m2, mferomonio):
    tela = pygame.display.set_mode((len(m2) * px, len(m2) * px))
    a = 255 / (FeromMax - FeromMin)

    for i in range(len(m2)):
        for j in range(len(m2[0])):
            x = mferomonio[i][j]
            y = int(a * x - FeromMin)

            if m2[i][j] == 1:
                pygame.draw.rect(tela, (255, 255, 255), [j * px, i * px, px, px])
            elif m2[i][j] == 2:
                pygame.draw.rect(tela, (0, 0, 255), [j * px, i * px, px, px])
            if mferomonio[i][j] > 0:
                pygame.draw.rect(tela, (y, 0, 0), [j * px, i * px, px, px])
            if m2[i][j] == 4:
                pygame.draw.rect(tela, (202, 205, 0), [j * px, i * px, px, px])

    pygame.draw.rect(tela, (255, 255, 0), [formiga.ObjetivoJ * px, formiga.ObjetivoI * px, px, px])
    pygame.draw.rect(tela, (0, 255, 0), [formiga.posJ * px, formiga.posI * px, px, px])
    pygame.display.update()


def pheromoneMax(mferomonio):
    max = 0
    for i in range(len(mferomonio)):
        for j in range(len(mferomonio[0])):
            if mferomonio[i][j] > max:
                max = mferomonio[j][i]

    return max

def meanPaths(caminhos):
    tamanho = 0
    for a in caminhos:
        tamanho+=len(a)
    return (tamanho/len(caminhos))
# Inicio do programa

mapa = Labrinth(lab)

Colonia = []
CaminhosEcontrados = []

saida = False

for i in range(NF):
    Colonia.append(Ant(mapa.pnt_init, mapa.pnt_end))
ciclos = 0
tempo = 0
tamanho = 0
feromax = 0
for i in range(NC):
    Best = 0
    inicial = (time.time() * 1000)
    for m in Colonia:
        m.caminhoLivre(mapa)

        while (not m.find()):
            #Habilitado botão de fechar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            m.choose(mapa)
            if ver == "-v2":
                PRINTA(m, mapa.PathMatrix, mapa.FeromonMatrix)
            mapa.Atualizapath(m)
            m.caminhoLivre(mapa)

            while (m.fechado()):
                #print_result(m, mapa, Colonia.index(m))
                m.come()
                m.caminhoLivre(mapa)

        mapa.limpaBeco()
        m.iteracao += 1
        if ver == "-v1":
            printaBest(m, mapa.PathMatrix, mapa.FeromonMatrix)

        #print_result(m, mapa, Colonia.index(m))

    for m in Colonia:

        CaminhosEcontrados.append(m.Caminho.copy())

        if (len(m.Caminho) <= Best):
            Best = len(m.Caminho)
            mapa.AtualizaFerom(m, Plus)
        else:
            mapa.AtualizaFerom(m, 0)
        mapa.EvaporaFerom()
        m.reeset(mapa.pnt_init)

    encontrou = (time.time() * 1000)

    tempo += (encontrou - inicial)
    tamanho += meanPaths(CaminhosEcontrados)
    feromax += pheromoneMax(mapa.FeromonMatrix)
    ciclos += 1
sair = True

print("APERTE O X DA JANELA PARA SAIR!!!")
while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False

print("Ciclos: "+ str(ciclos))
print("Tempo médio: "+ str(format((tempo/ciclos), '.4f')) + " ms")
print("Tamanho médio: "+ str(tamanho/ciclos))
print("Feromonio Max :"+ str(feromax/ciclos))




