import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SIS(object):
    """docstring"""
    name = "SIS"
    initial = { "S0" : "Suceptible",
                "E0" : "Exposed",
                "I0" : "Infected",
                "R0" : "Recovered"}
    vars = {"Beta"   : "infectiousRate",
            "Sigma"  : "incubationRate",
            "Gamma"  : "recoveryRate",
            "Epsilon": "lossImunityRate"}

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
        self.set("S0", 1)
        print(self.get("S0"))
        self.I0 = nbInfctd0
        self.N = self.S0 + self.I0
        self.S, self.I = None, None
        self.beta = infectiousRate
        self.gamma = recoveryRate
        self.timeParam = [timeStart, timeStop, nbSteps]
        self.timeVector = np.linspace(timeStart, timeStop, nbSteps)
        self.solved = False

    def solveDifferential(self):
        pass

    def export(self, filename=None, duration=None, d=":"):
        if filename ==None:
            filename = "Images/"+self.name
        for elem in self.initial.keys:
            filename += self.get(elem)
            filename += d
        for val in self.vals.keys:
           filename += self.get(val)
           filename += d
        filename += str(self.timeParam[0]) + d + str(self.timeParam[1]) + d + str(self.timeParam[2])
        filename += ".png"
        self.createGraph(duration)
        plt.savefig(filename)

if __name__ == "__main__":
    SIS()