import random
import numpy as np
SUSCEPTIBLE = 0
INFECTED = 1
VACCINATED = 2

def RNG(probability):
    return random.random() < probability

class VaccineModel(object):
    """docstring for VaccineModel."""

    def __init__(self, parametres = {}, size = [50,50]):
        self.printed = False
        self.X, self.Y = size

        self.parametres = parametres

        self.createSets()
        self.applyDefaultParametres()

        self.population = np.full((self.Y, self.X), SUSCEPTIBLE)

    def clear(self):
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

    def changeParam(self, parametres):
        #prend un dictionnaire en parametres et change les valeurs de prob
        self.parametres = parametres
        self.applyDefaultParametres()


    def applyDefaultParametres(self):
        defaults =\
        {'probVaccine' : 0.5,\
         'probInfect' : 1,\
         'probCure' : 0,\
          'maxTime' : 50,\
          'I0' : 1\
        }
        for elem in defaults.keys():
            if elem not in self.parametres:
                self.parametres[elem] = defaults[elem]

    def vaccinatePopulation(self):
        susceptibles = list(self.susceptibles)
        random.shuffle(susceptibles)

        #Nombre total de gens vacciné
        toVaccine = int(self.parametres['probVaccine']*(self.X*self.Y))
        for count in range(toVaccine):
            self.vaccinate(susceptibles.pop())

    def vaccinate(self, indexPair, force=False):
        i, j = indexPair
        if force or indexPair in self.susceptibles: #Vaccine que les sus
            if indexPair in self.susceptibles :
                #on peut pas le retirer si il est pas dedans
                self.susceptibles.remove(indexPair)
            self.vaccinated.add(indexPair)
            self.population[j][i] = VACCINATED
            return True
        return False

    def infectI0Susceptibles(self):
        susceptibles = list(self.susceptibles)
        random.shuffle(susceptibles)

        #Nombre total de gens vacciné
        for count in range(self.parametres['I0']):
            self.infect(susceptibles.pop())

    def infect(self, indexPair):
        i, j = indexPair
        if indexPair in self.susceptibles: #infecte que le sus
            self.susceptibles.remove(indexPair)
            self.infected.add(indexPair)
            self.population[j][i] = INFECTED
            return True
        return False



    def spread(self):
        susceptiblesBefore = len(self.susceptibles)
        stack = []
        if len(self.infected) > len(self.susceptibles):
            for human in self.susceptibles:
                for human2 in self.neighbours(human):
                    if human2 in self.infected:
                        if RNG(self.parametres['probInfect']):
                            stack.append(human)
                        if RNG(self.parametres['probCure']):
                            self.vaccinate(human2, force=True)
        else:
            for human in self.infected:
                for human2 in self.neighbours(human):
                    if human2 in self.susceptibles and RNG(self.parametres['probInfect']):
                        stack.append(human2)
                if RNG(self.parametres['probCure']):
                    self.vaccinate(human, force=True)
        for futureinfected in stack:
            self.infect(futureinfected)
        done = susceptiblesBefore == len(self.susceptibles)

        #Fin du spreading, on affiche les résultats
        if done and not self.printed:
            nombreSainDépart = self.X*self.Y
            nombreVacciné = len(self.vaccinated)
            nombreInfecté = len(self.infected)
            nombreSain = len(self.susceptibles)
            print(f"Pour une population vaccinée à {self.parametres['probVaccine']*100}%")
            print(f"Nous constatons que parmis les non vaccinés ( {nombreSain+nombreInfecté} cases blanches au départ), \
            seulement {100*nombreSain/(nombreSain+nombreInfecté)}% ont été épargnés du virus")
            self.printed = True

    def neighbours(self, ij):
        i, j = ij
        res = set()
        if 0 <= i-1:
            res.add((i-1,j))

        if 0 <= j-1:
            res.add((i,j-1))
        res.add((i,j))
        if j+1 < self.X:
            res.add((i, j+1))

        if i+1 < self.Y:
            res.add((i+1,j))
        return res
