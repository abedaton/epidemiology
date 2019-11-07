import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# N = Population Totale.
# S = suceptible , E = exposed , I = infected , H = hospitalized
# F = funeralized ,R = removed
# I0,E0,H0,F0 et R0 sont les états de base a l'instant t = 0
S0, E0, I0, H0, F0, B0, R0 =  1000, 0, 1, 0, 0, 0, 0
N = S0+E0+I0+H0+F0+B0+R0
# set param for Ebola by cautkin River
# beta = virulance (contact rate) can be I or F or H in community , funeral, hospital
betaI = 0.190
betaF = 0.668
betaH = 0.641
# alpha = 1/incubation period
alpha = 1.555
# gamma = "recovery rate" (/jours). can in H or DH in 1/time until hospitalization , 1/from hospitalisation to death
gammaH = 0.285
gammaDH = 0.838
# gammaF = 1/ duration of traditional funeral , gammaI = 1/duration of  infection
gammaF = 0.726
gammaI = 0.085
# gammaD = 1/ time from infection to death , gammaIH = 1/ time from hospitalization to recovery
gammaD = 0.419
gammaIH = 0.344
# theta = probability a case is hospitalized
theta = 0.197
# delta1 = Case fatality rate, unhospitalized , delta2 = Case fatality rate, hospitalized
delta1 = 0.750
delta2 = 0.750

t = np.linspace(0, 1000, 1000)

# Equadif de SEIHFR adapté pour séparé soigné et mort
def deriv(y, t, N, betaI, betaF, betaH, alpha, gammaH, gammaDH, gammaF, gammaI, gammaD, gammaIH, theta, delta1, delta2):
    S, E, I, H, F, B, R = y
    dSdt = -((betaI*S*I) + (betaH*S*H) + (betaF*S*F))/ N
    dEdt = (((betaI*S*I) + (betaH*S*H) + (betaF*S*F))/ N) - alpha*E
    dIdt = alpha*E-(gammaH*theta + gammaI*(1-theta)*(1-delta1) + gammaD*(1-theta)*delta1)*I
    dHdt = gammaH*theta*I - (gammaDH*delta2 + gammaIH*(1-delta2))*H
    dFdt = gammaD*(1-theta)*delta1*I + gammaDH*delta2*H - gammaF*F
    dBt = gammaF*F
    dRdt = gammaI*(1-theta)*(1-delta1)*I + gammaIH*(1-delta2)*H
    return dSdt, dEdt, dIdt, dHdt, dFdt, dBt, dRdt

# vecteur initial
y0 = S0, E0, I0, H0, F0, B0, R0

# On résoud l'equadiff
ret = odeint(deriv, y0, t, args=(N, betaI, betaF, betaH, alpha, gammaH, gammaDH, gammaF, gammaI, gammaD, gammaIH, theta, delta1, delta2))
S, E, I, H, F, B,  R = ret.T

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='(S)usceptible')
i = 0
while i <= 1.2:
	ax.hlines(i, -1, 200, color="black", linestyle = "dashed")
	i += 0.2

for i in range(20, 200, 20):
	ax.vlines(i, 0, 20000, color="black", linestyle = "dashed")

ax.plot(t, E/1000, 'darkorange', alpha=0.5, lw=2, label='(E)xposed')
ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='(I)nfected')
ax.plot(t, H/1000, 'deepskyblue', alpha=0.5, lw=2, label='(H)ospitalized')
ax.plot(t, F/1000, 'yellow', alpha=0.5, lw=2, label='(F)uneralized')
ax.plot(t, B/1000, 'dimgray', alpha=0.5, lw=2, label='(B)urried')
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
print("Nombre de personne susceptibles au debut =", S[0])
print("Nombre de personne susceptible a la fin =", S[-1])
print("Nombre de personne exposée a la fin =", E[-1])
print("Nombre de personne infectée a la fin =", I[-1])
print("Nombre de personne hospitalisée a la fin =", H[-1])
print("Nombre de personne morte mais pas Bcore Bterée  a la fin =", F[-1])
print("Nombre de personne retablie à la fin =", R[-1])
print("Nombre de personne entérée à la fin =", B[-1])
print("Nombre de personne totalle calcul =" ,round(B[-1]+ S[-1]+ R[-1],0))
print("Nombre de personne totalle calcul total =" ,B[-1]+ S[-1]+E[-1]+I[-1]+H[-1] + F[-1]+ R[-1],0)
print("Nombre de personne totalle réelle =" ,N)
plt.show()


