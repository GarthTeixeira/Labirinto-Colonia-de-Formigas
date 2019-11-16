import random

class Ant:
    posI=1
    posJ=1
    PosDispo=[]
    Caminho=[]
            
        
    def caminhoLivre(self,matrix):
        if(matrix[self.posI][self.posJ+1]==0):
            self.PosDispo.append([self.posJ+1,self.posI])

        if(matrix[self.posI][self.posJ-1]==0):
            self.PosDispo.append([self.posJ-1,self.posI])

        if(matrix[self.posI+1][self.posJ]==0):
            self.PosDispo.append([self.posJ,self.posI+1])

        if(matrix[self.posI-1][self.posJ]==0):
            self.PosDispo.append([self.posJ,self.posI-1])

    def andar(self,objetivo):
        self.Caminho.append([self.posJ,self.posI])
        self.posI=objetivo[1];
        self.posJ=objetivo[0];

    


    
class Labrinth:
    
    PathMatrix=[]
    FeromonMatrix=[]
    pnt_init=[]
    pnt_end=[]
    
    def __init__(self,file):
        f = open(file,'r') 
        f_content = f.readlines()
        matrix1=[]
        matrix2=[]
        matrix3=[]

        for i in f_content:
            for  j in i:    
                if(j==' '):
                    matrix2.append(0)
                elif(j=='S'):
                    matrix2.append(2)
                elif(j=='E'):
                    matrix2.append(3)
                else:
                    matrix2.append(1)
            aux=matrix2.copy()
            matrix1.append(aux)
            matrix2.clear()
        
        f.close()

        for line in matrix1:
            for i in range(0,len(line),2):
                matrix2.append(line[i])
            aux=matrix2.copy()
            matrix3.append(aux)
            matrix2.clear()
        
        self.PathMatrix=matrix3.copy()
        matrix3.clear()

         
        for i in self.PathMatrix:
            if (2 in i):
                    self.pnt_init.append(i.index(2)) 
                    self.pnt_init.append(self.PathMatrix.index(i)) 
            if (3 in i):
                    self.pnt_end.append(i.index(3))
                    self.pnt_end.append(self.PathMatrix.index(i)) 
            for j in i:
                if(j==1):
                    matrix2.append(0)
                else:
                    matrix2.append(random.random())
            aux=matrix2.copy()
            self.FeromonMatrix.append(aux)
            matrix2.clear()

    def Atualizapath(self,caminho):
            posI=caminho[1]
            posJ=caminho[0]
            self.PathMatrix[posI][posJ]=4
    


mapa = Labrinth("LabirintoExemplo01.txt")

for i in mapa.PathMatrix:
    print(i)

print ("\n")

for i in mapa.FeromonMatrix:
    print(i)


            


    
        