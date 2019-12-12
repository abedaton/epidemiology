import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SIS(object):
    """docstring for SEIRS."""
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
        eval("self."+var+" = "+val)