import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SIS(object):
    """docstring"""
    name = "SIS"
    initial = { "S0" : "Suceptible",
                "I0" : "Infected"}
    vars = {"beta"   : "infectiousRate",
            "gamma"  : "recoveryRate"}

    def get(self, var):
        try:
            return eval("self."+var)
        except:
            return None

    def set(self, var, val):
        exec("self."+var+" = "+str(val))

    def __init__(self, nbSscptbl0=999, nbInfctd0=1,\
                 infectiousRate=0.3, recoveryRate=0.05, \
                 timeStart=0, timeStop=1000, nbSteps=1001):

        self.S0 = nbSscptbl0
        self.I0 = nbInfctd0
        self.N = self.S0 + self.I0
        self.S, self.I = None, None
        self.beta = infectiousRate
        self.gamma = recoveryRate
        self.timeParam = [timeStart, timeStop, nbSteps]
        self.timeVector = np.linspace(timeStart, timeStop, nbSteps)

    def differentialEq(self, y, t):
        pass

    def solveDifferential(self):
        # vecteur initial
        list0 = []
        for elem in self.initial.keys():
            list0.append(self.get(elem))
        y0 = tuple(list0)
        ret = odeint(self.differentialEq, y0, self.timeVector)

        for index, elem in enumerate(self.initial.keys()):
            self.set(elem[0], list(ret.T[index]))

        return ret.T

    def createGraph(self, duration=None, Color=['b','y','r','g']):
        """
        Susceptible in blue, Exposed in yellow, Infected in red, recovered in green
        """
        if duration == None:
            duration = self.timeVector[-1]

        self.solveDifferential()

        fig = plt.figure()
        ax = fig.add_subplot()
        for index, elem in enumerate(self.initial.keys()):
            var = self.get(elem[0])
            name = self.initial[elem]
            name = '('+name[0].upper()+')'+name[1:]
            ax.plot(self.timeVector, var, Color[index], label=name)
        ax.set_xlabel('Time (in days)')
        ax.set_ylabel('Populaton (in person)')

        ax.set_xlim(0, duration)
        legend = ax.legend() #ET?

    def plot(self, duration=None):
        self.createGraph(duration)
        plt.show()

    def export(self, filename=None, duration=None, d=":"):
        if filename ==None:
            filename = "Images/"+self.name
        for elem in self.initial.keys():
            filename += self.get(elem)
            filename += d
        for val in self.vars.keys():
           filename += self.get(val)
           filename += d
        filename += str(self.timeParam[0]) + d + str(self.timeParam[1]) + d + str(self.timeParam[2])
        filename += ".png"
        self.createGraph(duration)
        plt.savefig(filename)

if __name__ == "__main__":
    model = SIS()
    model.set("S0", 10)
    print(model.get("S0"))
