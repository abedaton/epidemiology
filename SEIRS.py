import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# I0 et R0 sont les Infécté de base et les Recovered de base a l'instant t = 0
#E0 sont les exposés
S0, E0, I0, R0 =999, 0,  1, 0

# N = Population Totale.
N = S0 + E0 + I0 + R0

# beta = virulance (contact rate) et sigma = "recovery rate" (/jours).
beta, sigma = 0.2, 1./10 

#epsilon=rate which recovered individuals return to the susceptible statue due to loss of immunity.
epsilon=0.04

#Recovery rate, sigma = 1/D, is determined by the average duration, D, of infection
gamma=1/15

t = np.linspace(0, 1000, 1000)

# Equadif de SIR
def deriv(y, t, N, beta, sigma,epsilon,gamma):
    S, E, I, R = y
    
    dSdt = (-(beta * S * I) / N ) + ( epsilon * R )
    dEdt = ((beta * S * I) / N ) - ( sigma * E )
    dIdt = (sigma * E ) - ( gamma * I )
    dRdt = (sigma * I ) - ( epsilon * R )
    
    return dSdt, dEdt, dIdt, dRdt

# vecteur initial
y0 = S0, E0, I0, R0

# On résoud l'equadiff
ret = odeint(deriv, y0, t, args=(N, beta, sigma, epsilon, gamma))
S, E, I, R = ret.T

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='(S)usceptible')
i = 0
while i <= 1.2:
	ax.hlines(i, -1, 200, color="black", linestyle = "dashed")
	i += 0.2

for i in range(20, 200, 20):
	ax.vlines(i, 0, 20000, color="black", linestyle = "dashed")

ax.plot(t, E/1000, 'y', alpha=0.5, lw=2, label='(E)xposed')
ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='(I)nfected')
ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='(R)ecovered')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number')
ax.set_ylim(0, 1.2)
ax.set_xlim(0, 200)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
print("Nombre de personne susceptible au debut =", S[0])
print("Nombre de personne susceptible a la fin =", S[-1])
print("Nombre de personne exposées a la fin =", E[-1])
print("Nombre de personne infectée a la fin =", I[-1])
print("Nombre de personne retablie a la fin =", R[-1])
plt.show()
