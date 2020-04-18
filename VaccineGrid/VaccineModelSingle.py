import numpy as np
import random as rd
import time
import multiprocessing
from multiprocessing import Pool
import sys

import matplotlib.pyplot as plt
import numpy as np

SIZE = 50
R_0 = 1
susceptiblesStart = set((x,y) for x in range(SIZE) for y in range(SIZE))
global globalI
globalI = 0
global result
resultDict = {}

def getNeighbours(ij):
    mostUp    = max(ij[0]-1, 0)
    mostRight = min(ij[1]+1, SIZE-1)
    mostDown  = min(ij[0]+1, SIZE-1)
    mostLeft  = max(ij[1]-1, 0)
    return ( (mostUp, mostLeft)  ,  (mostUp, ij[1])  ,  (mostUp, mostRight),
             (ij[0], mostLeft)   ,  (ij[0], ij[1])   ,  (ij[0] , mostRight),
             (mostDown, mostLeft),  (mostDown, ij[1]),  (mostDown, mostRight))


class VaccineModel(object):
    """docstring for VaccineModel."""

    def __init__(self, V):
        self.timeStart = time.time()
        self.result = None
        self.V = V
        self.infected = set()
        self.susceptible = susceptiblesStart.copy()
        self.vaccinated = set()
        self.start()


    def start(self):
        self.vaccinatePopulation()
        self.infectPatientZero()
        while self.spread():
            pass
        self.result = \
        100*(SIZE*SIZE - int(self.V*SIZE*SIZE) - len(self.infected))\
        / (SIZE*SIZE - int(self.V*SIZE*SIZE))
        if self.V == 100:
            print("itération",globalI,". Programme lancé il y a", time.time()-self.timeStart,"secondes")
            print("Temps restant :", (time.time()-self.timeStart)/(globalI+1)*(nbIter-globalI-1))

    def infectPatientZero(self):
        for patient in rd.sample(self.susceptible, R_0):
            self.infected.add(patient)
            self.susceptible.remove(patient)

    def vaccinatePopulation(self):
        nbToVaccinate = int(self.V*SIZE*SIZE)
        for patient in rd.sample(self.susceptible, nbToVaccinate):
            self.vaccinated.add(patient)
            self.susceptible.remove(patient)

    def spread(self):
        numberOfInfectedBeforeSpread = len(self.infected)
        stack = set()

        if len(self.infected) < len(self.susceptible):
            for person in self.infected:
                for neighbour in getNeighbours(person):
                    if neighbour not in self.vaccinated:
                        stack.add(neighbour)
        else:
            for person in self.susceptible:
                for neighbour in getNeighbours(person):
                    if neighbour in self.infected:
                        stack.add(person)
                        break #breaks only 1 loop

        self.infected.update(stack)
        self.susceptible -= stack
        if len(self.infected) == numberOfInfectedBeforeSpread:
            return False
        return True

def runIterTimes(V):
    thisStart = time.time()
    global globalI
    for j in range(10):
        print("Itération",10*V+j,"à été effectuée 1000 fois en", time.time()-thisStart,"secondes")
        print("Temps restant :",(time.time()-thisStart)*(100-10*V-j))
        for i in range(nbIter):
            if 10*V+j in resultDict:
                resultDict[10*V+j] += VaccineModel((10*V+j)/100).result
            else:
                resultDict[10*V+j] = VaccineModel((10*V+j)/100).result
            globalI += 1

def readFile(filename):
    with open(filename, 'r') as file:
        data = np.empty(100)
        for i in range(100):
            ligne = file.readline()[:-1]
            if ligne == '':
                break
            data[i] = float(ligne)
    return data

def showResultInMPL(filename):
    data = readFile(filename)

    f, ax = plt.subplots()
    ax.set_title("Efficacité de la couverture vaccinale dans une population carrée de 2500 individus\n(Moyenne sur 5000 itération par pourcentage)")
    ax.set_yticks(np.linspace(0, 100, 21))
    ax.set_ylabel("Population épargnée de la maladie (en %)", rotation=360, wrap=True, ha="right")
    ax.set_xticks(np.linspace(0, 100, 21))
    ax.set_xlabel("Population vaccinée (en %)")
    ax.grid(True)
    ax.plot(data)
    plt.show()

nbIter = 1000
if __name__ == '__main__':
    outputFileName = sys.argv[1] if len(sys.argv) > 1 else "Result" + str(nbIter)
    show = sys.argv[2] if len(sys.argv) > 2 else False
    start = time.time()
    for V in range(10):
        runIterTimes(V)
    print(time.time()-start)
    print(resultDict)
    print(resultDict.keys())
    with open(outputFileName, 'a+') as fichier:
        for i in range(100):
            fichier.write(str(resultDict[i]/nbIter) + '\n')
    if show:
        showResultInMPL(outputFileName)
