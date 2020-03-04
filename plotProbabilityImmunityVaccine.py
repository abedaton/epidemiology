import matplotlib.pyplot as plt
from math import factorial
import numpy as np
x = np.linspace(0, 100, 101)

def nchoosek(n, k):
    return factorial(n)/(factorial(k)*factorial(n-k))

def binomiale(n, p):
    k = 8
    return nchoosek(k, n) * (p**n) * (1-p)**(k-n)

f, ax = plt.subplots()
#ax.set_title("Probabilité pour un individu d'avoir x voisins vaccinés\ndans une population en fonction du pourcentage de vaccinés")
ax.set_yticks(np.linspace(0, 1, 21))
#ax.set_ylabel("Probabilité d'avoir x voisins vaccinés")#, rotation=360, wrap=True, ha="right")
ax.set_xticks(np.linspace(0, 1, 11))
#ax.set_xlabel("Probabilité pour chaque individu d'être vacciné")
ax.grid(True)
for j in range(1,9):
    y = np.empty_like(x)
    for i in range(len(y)):
        y[i] = binomiale(j, i/100)
    ax.plot(x/100, y, label=f'{j} voisins')
ax.legend()
plt.show()
