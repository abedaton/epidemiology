import numpy as np
import random as rd
import time
from multiprocessing import Pool
SIZE = 50
R_0 = 1
susceptiblesStart = set((x,y) for x in range(SIZE) for y in range(SIZE))

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
        self.result = SIZE*SIZE - int(self.V*SIZE*SIZE) - len(self.infected)

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
    result = 0
    for i in range(nbIter):
        result += VaccineModel((V/100)).result
    return result


if __name__ == '__main__':
    nbIter = 1000
    start = time.time()
    with Pool(100) as p:
        result = p.map(runIterTimes, [x for x in range(100)])
        print(time.time()-start)
    for i, elem in enumerate(result):
        print(i, elem/nbIter)