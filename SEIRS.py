from SIS import SIS
import numpy as np

class SEIRS(SIS):
    """docstring for SEIRS."""
    name = "SEIRS"
    initial = { "S0" : "Suceptible",
                "E0" : "Exposé",
                "I0" : "Infecté",
                "R0" : "Rétabli"}
    vars = {"beta"   : "taux d'infection",
            "sigma"  : "taux d'incubation",
            "gamma"  : "taux de guérison",
            "epsilon": "taux de perte d'immunité"}


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
        self.timeVector = np.linspace(timeStart, timeStop, nbSteps)

    def differentialEq(self, y, t):
        S, E, I, R = y

        dSdt = (-(self.beta * S * I) / self.N ) + ( self.epsilon * R )
        dEdt = ((self.beta * S * I) / self.N ) - ( self.sigma * E )
        dIdt = (self.sigma * E ) - ( self.gamma * I )
        dRdt = (self.gamma * I ) - ( self.epsilon * R )

        return dSdt, dEdt, dIdt, dRdt

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
