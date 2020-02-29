import threading
import time
from VaccineModel import VaccineModel
import sys

class ThreadTest(threading.Thread):
    """docstring for ThreadTest."""

    def __init__(self, id, vaccineProb=0):
        super(ThreadTest, self).__init__()
        self.id = id
        self.vaccineProb = vaccineProb
        self.results = None
        self.simulation = VaccineModel({'probVaccine' : self.vaccineProb/100, 'probDeath' : 0, 'probCure' : 0})

    def run(self):
        #print(f"{self.id} starting")
        self.startTime = time.time()
        self.executeFunction()
        self.endTime = time.time()
        #print(f"{self.id} finished in {self.endTime-self.startTime} seconds")

    def executeFunction(self):
        self.simulation.buildFirstFrame()
        while self.simulation.spread():
            pass
        self.results = self.simulation.trueResults


nbIter = 24

if __name__ == '__main__' and sys.argv[1] == "thread":
    print("STARTING TIME")
    start = time.time()
    results = []
    for i in range(nbIter):
        results.append(ThreadTest(i))
        print(i)
    for i in range(nbIter):
        test = time.time()
        results[i].start()
        print(i, time.time()-test)

    print("FINISHED")
    print(" Time took : ", time.time()-start)

if __name__ == '__main__' and sys.argv[1] == "normal":

    print("STARTING TIME")
    start = time.time()
    results = []
    for i in range(nbIter):
        results.append(VaccineModel({'probVaccine' : i/100, 'probDeath' : 0, 'probCure' : 0}))
        results[-1].buildFirstFrame()
        while results[-1].spread():
            pass
        print(i)

    print("FINISHED")
    print(" Time took : ", time.time()-start)
