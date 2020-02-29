import multiprocessing
import time
from VaccineModel import VaccineModel
import sys

global results
results = {}

def executeFunction(id, queue):
    print(id, queue)
    simulation = VaccineModel({'probVaccine' : id/100, 'probDeath' : 0, 'probCure' : 0})
    simulation.buildFirstFrame()
    while simulation.spread():
        pass
    queue.put(simulation.trueResults)


nbIter = 100

if __name__ == '__main__' and sys.argv[1] == "thread":
    print("STARTING TIME")
    start = time.time()
    p = []
    q = multiprocessing.Queue()
    for k in range(1):
        for i in range(nbIter):
            p = multiprocessing.Process(target=executeFunction, args=(i,q,))
            p.start()


        for i in range(nbIter):
            print(q.get())
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
