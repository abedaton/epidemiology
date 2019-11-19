import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# N = Population Totale.
# I0 et R0 sont les Infécté de base et les Recovered de base a l'instant t = 0
I0, R0 =  1, 0
N = 1000+I0
# Tous les autres sont donc susceptible 
S0 = N - I0 - R0
# beta = virulance (contact rate) et gamma = "recovery rate" (/jours).
beta, gamma = 0.2, 1./10 

t = np.linspace(0, 1000, 1000)

# Equadif de SIR
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# vecteur initial
y0 = S0, I0, R0


# On résoud l'equadiff
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='(S)usceptible')
i = 0
while i <= 1.2:
	ax.hlines(i, -1, 200, color="black", linestyle = "dashed")
	i += 0.2

for i in range(20, 200, 20):
	ax.vlines(i, 0, 20000, color="black", linestyle = "dashed")

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
print("Nombre de personne infectée a la fin =", I[-1])
print("Nombre de personne retablie a la fin =", R[-1])
plt.show()


