import random
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

        self.population = [[SUSCEPTIBLE for j in range(self.X)] for i in range(self.Y)]

    def clear(self):
        self.printed = False
        self.createSets()
        self.population = [[SUSCEPTIBLE for j in range(self.X)] for i in range(self.Y)]

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
          'maxTime' : 50,\
          'I0' : 1\
        }
        for elem in defaults.keys():
            if elem not in self.parametres:
                self.parametres[elem] = defaults[elem]

    def vaccinatePopulation(self):
        #Nombre total de gens vacciné
        toVaccine = self.parametres['probVaccine']*(self.X*self.Y)
        while toVaccine > 0:
            #On vaccine la population au hasard
            i, j = random.randrange(0, self.Y), random.randrange(0, self.X)
            #Si vaccin réussi, on diminue
            if self.vaccinate((i, j)):
                toVaccine -= 1

    def vaccinate(self, indexPair):
        i, j = indexPair
        if indexPair in self.susceptibles: #Vaccine que les sus
            self.susceptibles.remove(indexPair)
            self.vaccinated.add(indexPair)
            self.population[i][j] = VACCINATED
            return True
        return False

    def infect(self, indexPair):
        i, j = indexPair
        if indexPair in self.susceptibles: #infecte que le sus
            self.susceptibles.remove(indexPair)
            self.infected.add(indexPair)
            self.population[i][j] = INFECTED
            return True
        return False

    def infectI0Susceptibles(self):
        susceptibles = tuple(self.susceptibles)
        #Infect un susceptible aléatoire
        for i in range(self.parametres['I0']):
            self.infect(susceptibles[random.randrange(0,len(susceptibles))])


    def spread(self):
        susceptiblesBefore = len(self.susceptibles)
        stack = []
        for iSus, jSus in self.susceptibles:
            for i,j in self.neighbours(iSus, jSus):
                if (i,j) in self.infected and RNG(self.parametres['probInfect']):
                    stack.append((iSus, jSus))
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

    def neighbours(self, i,j):
        res = set()
        if 0 < i-1:
            if 0 < j-1:
                res.add((i-1,j-1))
            res.add((i-1,j))
            if j+1 < self.X:
                res.add((i-1, j+1))

        if 0 < j-1:
            res.add((i,j-1))
        res.add((i,j))
        if j+1 < self.X:
            res.add((i, j+1))

        if i+1 < self.Y:
            if 0 < j-1:
                res.add((i+1,j-1))
            res.add((i+1,j))
            if j+1 < self.X:
                res.add((i+1, j+1))
        return res
