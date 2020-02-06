import random

def RNG(probability):
    return random.random() < probability

class VaccineModel(object):
    """docstring for VaccineModel."""

    def __init__(self, parametres = {}, size = [30,30]):
        self.counter = 0
        self.X, self.Y = size
        self.parametres = parametres
        self.currentValues = {'nbSusceptible' : self.X*self.Y, 'nbInfected' : 0, 'nbVaccinated' : 0}
        self.representation = {'SUSCEPTIBLE' : 0, 'INFECTED' : 1, 'VACCINATED' : 2}
        self.defaultParametres()
        self.population = [[self.get('SUSCEPTIBLE') for j in range(self.X)] for i in range(self.Y)]
        self.vaccinatePopulation()



    def get(self, nameOfParam):
        if nameOfParam in self.parametres:
            return self.parametres[nameOfParam]
        if nameOfParam in self.currentValues:
            return self.currentValues[nameOfParam]
        if nameOfParam in self.representation:
            return self.representation[nameOfParam]

    def defaultParametres(self):
        self.defaults = {'base' : 0, 'probVaccine' : 0.5, 'probInfect' : 1, 'maxTime' : 50}
        for elem in self.defaults.keys():
            if elem not in self.parametres:
                self.parametres[elem] = self.defaults[elem]

    def vaccinatePopulation(self):
        for i, row in enumerate(self.population):
            for j, people in enumerate(row):
                if RNG(self.get('probVaccine')):
                    self.vaccinate(i,j)

    def vaccinate(self, i, j):
        self.population[i][j] = self.get('VACCINATED')
        self.currentValues['nbSusceptible'] -= 1
        self.currentValues['nbVaccinated'] += 1

    def infect(self, i, j):
        if self.population[i][j] == self.get('SUSCEPTIBLE'):
            self.population[i][j] = self.get('INFECTED')
            self.currentValues['nbSusceptible'] -= 1
            self.currentValues['nbInfected'] += 1

    def startInfection(self, I0 = 1):
        while I0 > 0:
            I0 -= 1
            #force infection
            self.population[random.randrange(0, self.Y)][random.randrange(0,self.X)] = self.get('INFECTED')

    def spread(self):
        self.counter += 1
        for iOne, row in enumerate(self.population):
            for jOne, people in enumerate(row):
                for i,j in self.neighbours(iOne,jOne):
                    if self.population[i][j] == self.get('INFECTED') and RNG(self.get('probInfect')):
                        self.infect(iOne,jOne)
        if self.counter == self.get('maxTime')-1:
            nombreSainDépart = self.X*self.Y
            nombreVacciné = self.get('nbVaccinated')
            nombreInfecté = self.get('nbInfected')
            nombreSain = self.get('nbSusceptible')
            print(nombreSain, nombreInfecté, nombreVacciné)
            print(f"Pour une population vaccinée à {self.get('probVaccine')*100}%")
            print(f"Nous constatons que parmis les non vaccinés, \
            {nombreSain/(nombreSain+nombreInfecté)}% ont été infectés")

    def neighbours(self, i,j):
        res = []
        if 0 < i-1:
            if 0 < j-1:
                res.append((i-1,j-1))
            res.append((i-1,j))
            if j+1 < self.X:
                res.append((i-1, j+1))

        if 0 < j-1:
            res.append((i,j-1))
        res.append((i,j))
        if j+1 < self.X:
            res.append((i, j+1))

        if i+1 < self.Y:
            if 0 < j-1:
                res.append((i+1,j-1))
            res.append((i+1,j))
            if j+1 < self.X:
                res.append((i+1, j+1))
        return res
