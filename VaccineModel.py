import random
import numpy as np
import sys
SUSCEPTIBLE = 0
INFECTED = 1
VACCINATED = 2
CURED = 3

def RNG(probability):
    return random.random() < probability

class VaccineModel(object):
    """docstring for VaccineModel."""

    def __init__(self, parametres = {}, size = [50,50], parent=None):
        self.running = True
        self.parent = parent
        self.X, self.Y = size

        self.parametres = parametres

        self.createSets()
        self.applyDefaultParametres()

        self.population = np.full((self.Y, self.X), SUSCEPTIBLE)
        self.maxInfected = 0

    def setIndexState(self, index, state):
        self.population[index[0]][index[1]] = state

    def getIndexState(self, index):
        return self.population[index[0]][index[1]]

    def checkIndexState(self, index, state):
        return self.population[index[0]][index[1]] == state

    def clear(self):
        self.running = True
        self.maxInfected = 0
        self.createSets()
        self.population = [[SUSCEPTIBLE for i in range(self.X)] for j in range(self.Y)]

    def createSets(self):
        self.susceptibles = set()
        #Tout le monde est susceptible au départ
        for i in range(self.X):
            for j in range(self.Y):
                self.susceptibles.add((i,j))

        self.vaccinated = set()
        self.infected = set()


    def buildFirstFrame(self):
        self.vaccinatePopulation()
        self.infectI0Susceptibles()

    def changeParam(self, parametres = {}):
        #prend un dictionnaire en parametres et change les valeurs de prob
        self.parametres = parametres
        self.applyDefaultParametres()


    def applyDefaultParametres(self):
        defaults =\
        {'probVaccine' : 0.5,\
         'probInfect' : 1,\
         'probCure' : 0.13,\
          'maxTime' : 50,\
          'I0' : 1\
        }
        for elem in defaults.keys():
            if elem not in self.parametres:
                self.parametres[elem] = defaults[elem]


    def cureSquare(self, ij):
        self.infected.remove(ij)
        self.vaccinated.add(ij)
        self.setIndexState(ij, CURED)
        return True

    def vaccinateSquare(self, ij):
        self.vaccinated.add(ij)
        self.susceptibles.remove(ij)
        self.setIndexState(ij, VACCINATED)
        return True

    def infectSquare(self, ij):
        if self.checkIndexState(ij, SUSCEPTIBLE): #infecte que le sus
            self.susceptibles.remove(ij)
            self.infected.add(ij)
            self.setIndexState(ij, INFECTED)
            self.maxInfected += 1
            return True
        return False

    def vaccinatePopulation(self):
        susceptibles = list(self.susceptibles)
        random.shuffle(susceptibles)

        #Nombre total de gens vacciné
        toVaccine = int(self.parametres['probVaccine']*(self.X*self.Y))
        for count in range(toVaccine):
            self.vaccinateSquare(susceptibles.pop())

    def infectI0Susceptibles(self):
        susceptibles = list(self.susceptibles)
        random.shuffle(susceptibles)

        #Nombre total de gens vacciné
        for count in range(self.parametres['I0']):
            self.infectSquare(susceptibles.pop())


    def spread(self):
        if self.running:
            if len(self.infected) >= len(self.susceptibles):
                stackToInfect = self.spreadFromSus()
            else:
                stackToInfect = self.spreadFromSus()

            stackToCure = self.cureIteration()

            for futureInfected in stackToInfect:
                self.infectSquare(futureInfected)
            for futureCured in stackToCure:
                self.cureSquare(futureCured)

            self.running = (len(self.infected) > 0)

            #Si fin du spreading, on affiche les résultats
            if not self.running:
                self.printEnd()
        return self.running


    def spreadFromSus(self):
        stack = []
        for cleanGuy in self.susceptibles:
            for neighbour in self.neighbours(cleanGuy):
                if self.getIndexState(neighbour) == INFECTED and RNG(self.parametres['probInfect']):
                    stack.append(cleanGuy)
        return stack

    def spreadFromInf(self):
        stack = []
        for infected in self.infected:
            for neighbour in self.neighbours(infected):
                if RNG(self.parametres['probInfect']):
                    stack.append(neighbour)
        return stack


    def cureIteration(self):
        stack = []
        for infected in self.infected:
            if RNG(self.parametres['probCure']):
                stack.append(infected)
        return stack


    def printEnd(self):
        nombreSainDépart = self.X*self.Y
        nombreVacciné = int(self.parametres['probVaccine']*(self.X*self.Y))
        nombreSain = len(self.susceptibles)
        nombreGueri = self.maxInfected
        self.trueResults = nombreSain+nombreVacciné
        self.results  = f"Dans une population vaccinée à {self.parametres['probVaccine']*100}%\n"
        self.results += f"Parmis les {nombreSain+nombreGueri} personnes susceptibles d'être touchées au départ \n"
        self.results += f"{100-100*nombreSain/(nombreSain+nombreGueri)}% ont été touchés par l'infection\n"
        if not self.running:
            if self.parent != None and self.parent.parent != None:
                self.parent.parent.setEndMessage(self.results)

    def neighbours(self, ij):
        mostUp    = max(ij[0]-1, 0)
        mostRight = min(ij[1]+1, self.X-1)
        mostDown  = min(ij[0]+1, self.Y-1)
        mostLeft  = max(ij[1]-1, 0)
        return ( (mostUp, mostLeft)  ,  (mostUp, ij[1])  ,  (mostUp, mostRight),
                 (ij[0], mostLeft)   ,  (ij[0], ij[1])   ,  (ij[0] , mostRight),
                 (mostDown, mostLeft),  (mostDown, ij[1]),  (mostDown, mostRight))

if __name__ == '__main__' and len(sys.argv) >= 3 and sys.argv[1] == "testing":
    outputFileName = sys.argv[2]
    for vaccineProb in range(100):
        print(vaccineProb)
        average = 0
        for i in range(10):
            print("",i)
            simulation = VaccineModel({'probVaccine' : vaccineProb/100})
            simulation.buildFirstFrame()
            while simulation.spread():
                pass
            average += simulation.trueResults
        with open(outputFileName, 'a+') as fichier:
            fichier.write(str(average/10) + '\n')
