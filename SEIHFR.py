from SIS import SIS
import numpy as np

class SEIHFR(SIS):
    """docstring for SEIHFR."""
    name = "SEIHFR"
    initial = { "S0" : "Suceptible",
                "E0" : "Exposé",
                "I0" : "Infecté",
                "H0" : "Hospitalisé",
                "F0" : "Cadavres",
                "R0" : "Rétabli"}
    vars = { "betaI"   : "taux de contact des infectés",
             "betaF"   : "taux de contact des cadavres",
             "betaH"   : "taux de contact des hospitalisés",
             "alpha"   : "1/période d'incubation",
             "gammaH"  : "1/temps avant hospitalisation" ,
             "gammaDH" : "1/temps entre hospitalisé et mort" ,
             "gammaF"  : "1/durée traditionnele de funérailles " ,
             "gammaI"  : "1/durée d'infection" ,
             "gammaD"  : "1/temps entre infecté et mort" ,
             "gammaIH" : "1/temps entre hospitalisé et rétabli" ,
             "theta"   : "probabilité que un infecté soit hospitalisé",
             "delta1"  : "taux de mortalité pour non hospitalisé",
             "delta2"  : "taux de mortalité pour hospitalisé" }

    def __init__(self, S0=999, E0=0, I0=1, H0=0, F0=0, R0=0,\
                betaI = 0.190, betaF = 0.668, betaH = 0.641, alpha = 1.555,\
                gammaH = 0.285, gammaDH = 0.838, gammaF = 0.726, gammaI = 0.085,\
                gammaD = 0.419, gammaIH = 0.344, theta = 0.197, delta1 = 0.750, delta2 = 0.750,\
                timeStart=0, timeStop=1000, nbSteps=1001):
        self.S0 = S0
        self.E0 = E0
        self.I0 = I0
        self.H0 = H0
        self.F0 = F0
        self.R0 = R0
        self.N = S0+E0+I0+H0+F0+R0
        self.S,self.I,self.E,self.H,self.F,self.R = None, None, None, None, None, None
        self.betaI = betaI
        self.betaF = betaF
        self.betaH = betaH
        self.alpha = alpha
        self.gammaH = gammaH
        self.gammaDH = gammaDH
        self.gammaF = gammaF
        self.gammaI = gammaI
        self.gammaD = gammaD
        self.gammaIH = gammaIH 
        self.theta = theta
        self.delta1 = delta1
        self.delta2 = delta2
        self.timeParam = [timeStart, timeStop, nbSteps]
        self.timeVector = np.linspace(timeStart, timeStop, nbSteps)
    
    def differentialEq(self, y, t):
        S, E, I, H, F, R = y
        dSdt = -((self.betaI*S*I) + (self.betaH*S*H) + (self.betaF*S*F))/ self.N
        dEdt = (((self.betaI*S*I) + (self.betaH*S*H) + (self.betaF*S*F))/ self.N) - self.alpha*E
        dIdt = self.alpha*E-(self.gammaH*self.theta + self.gammaI*(1-self.theta)*(1-self.delta1) + self.gammaD*(1-self.theta)*self.delta1)*I
        dHdt = self.gammaH*self.theta*I - (self.gammaDH*self.delta2 + self.gammaIH*(1-self.delta2))*H
        dFdt = self.gammaD*(1-self.theta)*self.delta1*I + self.gammaDH*self.delta2*H - self.gammaF*F
        dRdt = self.gammaI*(1-self.theta)*(1-self.delta1)*I + self.gammaIH*(1-self.delta2)*H + self.gammaF*F
        return dSdt, dEdt, dIdt, dHdt, dFdt, dRdt

