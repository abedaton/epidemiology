import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class Epidemy:
	def __init__(self, N, I0, R0, S0, t, params):
		self.N = N
		self.S0 = S0
		self.I0 = I0
		self.R0 = R0
		self.t = np.linspace(0, t, t)
		for param in params: # on extrait les paramétres et on les ajoutent en attribus
			setattr(self, param, params.get(param))
		self.colors = ["b", "r", "g", "yellow", "dimgray", "deepskyblue", "darkorange"]

	def SIR(self, y, t):
		S, I, R = y
		dSdt = -self.beta * S * I / self.N
		dIdt = self.beta * S * I/self.N - self.gamma * I
		dRdt = self.gamma*I
		return dSdt, dIdt, dRdt

	def SEIHFR(self, y, t):
		S, E, I, H, F, R = y
		dSdt = -((self.betaI*S*I) + (self.betaH*S*H) + (self.betaF*S*F))/ self.N
		dEdt = (((self.betaI*S*I) + (self.betaH*S*H) + (self.betaF*S*F))/ self.N) - self.alpha*E
		dIdt = self.alpha*E-(self.gammaH*self.theta + self.gammaI*(1-self.theta)*(1-self.delta1) + self.gammaD*(1-self.theta)*self.delta1)*I
		dHdt = self.gammaH*self.theta*I - (self.gammaDH*self.delta2 + self.gammaIH*(1-self.delta2))*H
		dFdt = self.gammaD*(1-self.theta)*self.delta1*I + self.gammaDH*self.delta2*H - self.gammaF*F
		dRdt = self.gammaI*(1-self.theta)*(1-self.delta1)*I + self.gammaIH*(1-self.delta2)*H + self.gammaF*F
		return dSdt, dEdt, dIdt, dHdt, dFdt, dRdt

	def SEIRS(self, S0, E0, I0, R0, beta, sigma, epsilon, t0, TStop, nbSteps):
		model = SEIRS(S0, E0, I0, R0, beta, sigma, epsilon, t0, TStop, nbSteps)
		S, E, I, R = model.solveDifferential()

	def solve(self, model):
		if model == "SIR":
			ret = odeint(self.SIR, [self.S0, self.I0, self.R0], self.t) # Obliger de passer [S0, I0, R0] et de les utiliser en local car odeint() change leurs valeurs et on ne veut pas qu'elles soient changées en attributs
		elif model == "SEIHFR":
			ret = odeint(self.SEIHFR, [self.S0, self.E0, self.I0, self.H0, self.F0, self.R0], self.t)
		return ret.T

	def letsPlot(self, params):
		fig = plt.figure(facecolor="w")
		ax = fig.add_subplot(111, axisbelow=True)

		for dx, elem in enumerate(params):
			ax.plot(self.t, params.get(elem)[0]/1000, self.colors[dx], alpha=0.5, lw=2, label = params.get(elem)[1])

		ax.set_xlabel("Time /days")
		ax.set_ylabel("Number")
		ax.set_ylim(0, 1.2)
		ax.set_xlim(0, 200)
		ax.yaxis.set_tick_params(length=0)
		ax.xaxis.set_tick_params(length=0)
		ax.grid(b=True, which="major", c="w", lw=2, ls="-")
		legend = ax.legend()
		legend.get_frame().set_alpha(0.5)
		plt.show()

# -----------------------------------------------------------------------------------------

SIR = Epidemy(1001, 1, 0, 1000, 1000, {"beta" : 0.2, "gamma" : 1./10})
S, I, R = SIR.solve("SIR")
params = {"S" : [S, "(S)usceptible"], "I" : [I, "(I)nfected"], "R" : [R, "(R)ecovered"]}
SIR.letsPlot(params)

# -----------------------------------------------------------------------------------------

SEIHFR = Epidemy(1001, 1, 0, 1000, 1000, {"E0":0, "H0":0, "F0":0, "betaI":0.190, "betaF":0.668, "betaH":0.641, "alpha":1.555, "gammaH":0.285, "gammaDH":0.838, "gammaF":0.726, "gammaI":0.085, "gammaD":0.419, "gammaIH":0.344, "theta":0.197, "delta1":0.750, "delta2": 0.750})
S, E, I, H, F, R = SEIHFR.solve("SEIHFR")
params = {"S" : [S, "(S)usceptible"], "I" : [I, "(I)nfected"], "H": [H, "(H)ospitalized"], "F" : [F, '(F)uneralized'], "R" : [R, "(R)ecovered"]}
SEIHFR.letsPlot(params)
