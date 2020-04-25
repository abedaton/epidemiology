import matplotlib.pyplot as plt
import numpy as np
from math import log


def importData(filename):
    with open(filename, 'r') as file:
        data = []
        ligne = file.readline()
        while True:
            ligne = file.readline()
            if ligne == '\n':
                break
            data.append(int(ligne[:ligne.index(";")])) #Reads first number only
    return data

data = importData('Covid19StatusThird.txt')

f, ax = plt.subplots()
plt.yscale("log")
ax.set_title("Prévision amateur de l'épidémie à COVID-19 en Belgique")
ax.set_yticks([1,10,100,1000,10000,1000000, 10000000], 7)
ax.set_ylabel("Individus infectés", rotation=360, wrap=True, ha="right")
ax.set_xticks(np.arange(0, 62, 5))
ax.set_xlabel("Jours depuis le premier infecté")
ax.grid(True)
ax.plot(data)
plt.show()
