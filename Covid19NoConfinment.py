from DATACovid19Tentative import Data
import numpy as np
import random
import time
data = Data()
print(data.N,"individus")
global statuSS
statuSS = {"N" : 0, "H" : 0, "I" : 0, "D" : 0}
deadPyramid = {}
nbTotalInfected = 0
listOfAllInfected = []


class Person(object):
    """docstring for Person."""

    def __init__(self, ageGroup, remainingTime, R0, incubationTime):
        self.ageGroup = ageGroup
        self.baseR0 = max(0,R0)
        self.remainingTime = self.baseTime = max(8,remainingTime)
        self.incubationTime = max(0, incubationTime)

        ageGroupBracket = data.ageBracketToGroupBracket[ageGroup]
        self.outcome = np.random.choice(["N", "H", "I", "D"],\
        p=[data.noConsequenceRate[ageGroupBracket]/100, data.hospitalizationRate[ageGroupBracket]/100, data.ICURate[ageGroupBracket]/100, data.deathRate[ageGroupBracket]/100])
        statuSS[self.outcome] += 1

    def getNumberHeInfectsTodayAndReduceTimes(self):
        #value = np.random.binomial(n=self.baseTime,p=self.baseR0/self.baseTime) if self.remainingTime > 0 else 0
        value = np.random.uniform(low=0, high=self.baseR0) if (self.remainingTime > 0 and self.incubationTime <= 0) else 0
        self.remainingTime -= 1
        self.incubationTime -= 1
        if self.remainingTime == 0:
            self.finishHim()
        return value

    def finishHim(self):
        global listOfAllInfected, deadPyramid
        ageGroupBracket = data.ageBracketToGroupBracket[self.ageGroup]
        if self.outcome == "D":
            data.agePyramid[self.ageGroup] -=1
            if self.ageGroup in deadPyramid:
                deadPyramid[self.ageGroup] += 1
            else:
                deadPyramid[self.ageGroup] = 1
        listOfAllInfected.remove(self)




#Fonctions #####################################################################

def infectMultiplePeople(nbToInfect=1):
    global listOfAllInfected
    ageGroups = np.random.choice(data.ageGroups, size=nbToInfect, p=data.probabilityAgeWeight)
    remainingTimes = data.getTimeViralShedding(nbToInfect)
    R0s = data.getR0(nbToInfect)
    incubationTimes = data.getIncubationPeriod(nbToInfect)
    tmpListPerson = np.empty(nbToInfect, dtype=Person)
    for i in range(nbToInfect):
        if nbTotalInfected+i == data.N:
            break
        tmpListPerson[i] = Person(ageGroups[i],int(remainingTimes[i]),R0s[i], int(incubationTimes[i]))
    listOfAllInfected = list(np.append(listOfAllInfected, tmpListPerson))


def aDayPasses():
    #Exemple : Il est minuit lors du jour 10, les patients ayant 10 jours de viral shedding sont maintenant rétablis/morts
    #Les patients avec 11 jours peuvent encore infecter avant d'être rétabli/mort
    global listOfAllInfected, nbTotalInfected, done
    futureInfected = 0
    if not done:
        for person in listOfAllInfected:
            if person == None:
                break
            futureInfected += person.getNumberHeInfectsTodayAndReduceTimes()
    else:
        for person in listOfAllInfected:
            if person == None:
                break
            person.finishHim()
    futureInfected = int(futureInfected)
    nbTotalInfected += futureInfected
    return infectMultiplePeople(futureInfected)

if __name__ == '__main__':
    print(data.agePyramid)
    infectMultiplePeople()
    print("Jour 0")
    print("Nombre d'infecté :", len(listOfAllInfected))
    i = 1
    done = False
    with open('Covid19StatusFourth.txt', 'a+') as file:
        file.write("Nombre d'infecte actuel;Nombre d'infecte totaux;N,H,I,D;")
        file.write("Fin : Pyramide des populations")
    while not done:
        start = time.time()
        aDayPasses()
        print("-------------------------------")
        print("Jour",i,"effectué en", time.time()-start)
        print("Nombre d'infecté :", len(listOfAllInfected))
        print()
        print("Futur de la population :")
        print(statuSS["N"], "personnes qui survivront sans être hospitalisées")
        print(statuSS["H"], "personnes qui seront hospitalisées et survivront")
        print(statuSS["I"], "personnes qui iront en soin intensif et survivront")
        print(statuSS["D"], "personnes qui ne survivront pas")
        print()
        i += 1
        with open("Covid19StatusFourth.txt", 'a+') as file:
            file.write(str(len(listOfAllInfected)) + ";" + str(nbTotalInfected) + ";" + str(statuSS["N"]) + "," + str(statuSS["H"]) + "," + str(statuSS["I"]) + "," + str(statuSS["D"]) + ";\n")
        if nbTotalInfected >= data.N:
            done = True
    aDayPasses()
    with open('Covid19StatusFourth.txt', 'a+') as file:
        file.write("\n")
        file.write(str(data.agePyramid))
    with open('Covid19StatusFourth.txt', 'a+') as file:
        file.write("\n")
        file.write(str(deadPyramid))
    print(deadPyramid)
