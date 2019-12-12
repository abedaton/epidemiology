#import numpy as np
#from scipy.integrate import odeint
#import matplotlib.pyplot as plt


class SEIRS(SIS):
    """docstring for SEIRS."""
    name = "SEIRS"
    initial = { "S0" : "Suceptible",
                "E0" : "Exposed",
                "I0" : "Infected",
                "R0" : "Recovered"}
    vars = {"beta"   : "infectiousRate",
            "sigma"  : "incubationRate",
            "gamma"  : "recoveryRate",
            "epsilon": "lossImunityRate"}

    #def get(self, var):
    #    try:
    #        return eval("self."+var)
    #    except:
    #        return None
#
    #def set(self, var, val):
    #    eval("self."+var+" = "+val)


    def __init__(self, nbSscptbl0=999, nbExpsd0=0, nbInfctd0=1,\
                 nbRcvrd0=0, infectiousRate=0.3, incubationRate=0.1,\
                 recoveryRate=0.05, lossImunityRate=0.01, \
                 timeStart=0, timeStop=1000, nbSteps=1001):
        """
        Beta :    from S to E (infectiousRate)
        Sigma :   from E to I (incubationRate)
        Gamma :   from I to R (recoveryRate)
        Epsilon : from R to S (lossImunityRate)
        """
        self.S0 = nbSscptbl0
        self.E0 = nbExpsd0
        self.I0 = nbInfctd0
        self.R0 = nbRcvrd0
        self.S, self.I, self.E, self.R = None, None, None, None
        self.N = self.S0 + self.E0 + self.I0 + self.R0
        self.beta = infectiousRate
        self.sigma = incubationRate
        self.gamma = recoveryRate
        self.epsilon = lossImunityRate #rate of returning to S
        self.timeParam = [timeStart, timeStop, nbSteps]
        #number of days
        self.timeVector = np.linspace(timeStart, timeStop, nbSteps)

        self.solved = False

    def differentialEq(self, y, t):
        S, E, I, R = y

        dSdt = (-(self.beta * S * I) / self.N ) + ( self.epsilon * R )
        dEdt = ((self.beta * S * I) / self.N ) - ( self.sigma * E )
        dIdt = (self.sigma * E ) - ( self.gamma * I )
        dRdt = (self.gamma * I ) - ( self.epsilon * R )

        self.solved = True

        return dSdt, dEdt, dIdt, dRdt

    def solveDifferential(self):
        # vecteur initial
        y0 = self.S0, self.E0, self.I0, self.R0
        ret = odeint(self.differentialEq, y0, self.timeVector)
        #S E I R = vecteurs de données
        self.S, self.E, self.I, self.R = ret.T
        return self.S, self.E, self.I, self.R

    def print(self, tStart=0, tStop=100, nbSteps=4):
        if not self.solved:
            self.solveDifferential()
        valueVector = [["(S)usceptible"], ["(E)xposed"], ["(I)nfected"], ["(R)ecovered"]]
        bigSteps = int(tStop/nbSteps)
        for i in range(tStart, tStop, bigSteps):
            valueVector[0].append(round(self.S[i], 2))
            valueVector[1].append(round(self.I[i], 2))
            valueVector[2].append(round(self.E[i], 2))
            valueVector[3].append(round(self.R[i], 2))
        valueVector[0].append(round(self.S[-1], 2))
        valueVector[1].append(round(self.I[-1], 2))
        valueVector[2].append(round(self.E[-1], 2))
        valueVector[3].append(round(self.R[-1], 2))
        for list in valueVector:
            print(f"{list[0]} : ")
            for i, value in enumerate(list[1:]):
                print(f"t = {bigSteps*i} | {value}")

    def createGraph(self, duration=None, \
             SColor='b', EColor='y', IColor='r', RColor='g'):
        """
        Susceptible in blue, Exposed in yellow, Infected in red, recovered in
        green
        """
        if duration == None:
            duration = self.timeVector[-1]
        if not self.solved:
            self.solveDifferential()

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(self.timeVector, self.S, 'b', label='(S)usceptible')
        ax.plot(self.timeVector, self.E, 'y', label='(E)xposed')
        ax.plot(self.timeVector, self.I, 'r', label='(I)nfected')
        ax.plot(self.timeVector, self.R, 'g', label='(R)ecovered')
        ax.set_xlabel('Time (in days)')
        ax.set_ylabel('Populaton (in person)')

        ax.set_xlim(0, duration)

        legend = ax.legend()



    def plot(self, duration=None):
        self.createGraph(duration)
        plt.show()

    def export(self, filename="Images/SEIRS", duration=None, d=":"):
        if filename == "Images/SEIRS":
            filename += str(self.S0) + d + str(self.E0) + d + str(self.I0) + \
                        d + str(self.R0) + d +  str(self.beta) + d + \
                        str(self.sigma) + d + str(self.gamma) + d + \
                        str(self.epsilon) + d + str(self.timeParam[0]) + d + \
                        str(self.timeParam[1]) + d + str(self.timeParam[2])
            filename += ".png"
        self.createGraph(duration)
        plt.savefig(filename)

def importGraph(filename, d=":"):
    firstSlashIndex = filename.index('/')
    #Remove path
    while '/' in filename:
        filename = filename[filename.index('/')+1:]
        print(filename)

    #Remove .png
    filename = filename[:filename.rindex('.')]
    paramList = []
    for param in filename.split(d):
        paramList.append(float(param))
    return SEIRS(*paramList)



if __name__ == '__main__':
    printGraph = False
    plotGraph = True

    exportGraph = False
    importGraphV = False

    printSteps = 4
    plotSizeX = 300


    if printGraph:
        test = SEIRS()
        test.print(printSteps)

    if plotGraph:
        test = SEIRS()
        test.plot(plotSizeX)

    if exportGraph:
        test = SEIRS()
        test.export()

    if importGraphV:
        test = importGraph('Images/SEIRS999:0:1:0:0.3:0.1:0.05:0.01:0:1000:1001.png')
        test.export('test')
