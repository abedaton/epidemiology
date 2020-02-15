import random
import numpy as np
SUSCEPTIBLE = 0
INFECTED = 1
VACCINATED = 2
CURED = 3

def RNG(probability):
    return random.random() < probability

class VaccineModel(object):
    """docstring for VaccineModel."""

    def __init__(self, parametres = {}, size = [50,50], parent=None):
        self.printed = False
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
        self.maxInfected = 0
        self.printed = False
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


    def cure(self, ij):
        self.infected.remove(ij)
        self.vaccinated.add(ij)
        self.setIndexState(ij, CURED)
        return True

    def vaccinate(self, ij):
        self.vaccinated.add(ij)
        self.susceptibles.remove(ij)
        self.setIndexState(ij, VACCINATED)
        return True

    def infect(self, ij):
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
            self.vaccinate(susceptibles.pop())

    def infectI0Susceptibles(self):
        susceptibles = list(self.susceptibles)
        random.shuffle(susceptibles)

        #Nombre total de gens vacciné
        for count in range(self.parametres['I0']):
            self.infect(susceptibles.pop())


    def spread(self):
        susceptiblesBefore = len(self.susceptibles)

        if len(self.infected) >= len(self.susceptibles):
            stack = self.spreadFromSus()
        else:
            stack = self.spreadFromSus()

        self.cureIteration()

        for futureinfected in stack:
            self.infect(futureinfected)

        #Fin du spreading, on affiche les résultats
        if len(self.infected) == 0 and not self.printed:
            if self.parent != None:
                self.parent.spreadingIsRunning = False
            self.printEnd()


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

        for infected in stack:
            self.cure(infected)


    def printEnd(self):
        nombreSainDépart = self.X*self.Y
        nombreVacciné = len(self.vaccinated)
        nombreSain = len(self.susceptibles)
        nombreGueri = self.maxInfected
        print(f"Pour une population vaccinée à {self.parametres['probVaccine']*100}%")
        print(f"Nous constatons que parmis les non vaccinés ( {nombreSain+nombreGueri} cases blanches au départ), \
        seulement {100*nombreSain/(nombreSain+nombreGueri)}% ont été épargnés du virus")
        self.printed = True

    def neighbours(self, ij):
        mostUp    = max(ij[0]-1, 0)
        mostRight = min(ij[1]+1, self.X-1)
        mostDown  = min(ij[0]+1, self.Y-1)
        mostLeft  = max(ij[1]-1, 0)
        return ( (mostUp, mostLeft)  ,  (mostUp, ij[1])  ,  (mostUp, mostRight),
                 (ij[0], mostLeft)   ,  (ij[0], ij[1])   ,  (ij[0] , mostRight),
                 (mostDown, mostLeft),  (mostDown, ij[1]),  (mostDown, mostRight))
