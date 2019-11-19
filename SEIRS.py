import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SEIRS(object):
    """docstring for SEIRS."""

    def __init__(self, nbSscptbl0=999, nbExpsd0=0, nbInfctd0=1,\
                 nbRcvrd0=0, population=1000, infectiousRate=0.3,\
                 incubationRate=0.1, recoveryRate=0.05, lossImunityRate=0.01, \
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

    def plot(self, duration=None, \
             SColor='b', EColor='y', IColor='r', RColor='g', ):
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

        plt.show()

if __name__ == '__main__':
    test = SEIRS()
    test.print(4)
    test.plot(300)
