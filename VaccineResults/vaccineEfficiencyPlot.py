import matplotlib.pyplot as plt
import numpy as np

def importData(filename):
    with open(filename, 'r') as file:
        data = np.empty(100)
        i = 0
        while True:
            ligne = file.readline()[:-1]
            if ligne == '':
                break
            data[i] = 100*float(ligne)/(2500-i*25)
            i += 1
    return data

data = importData('100iter100prob-resultsBIS.txt')

f, ax = plt.subplots()
ax.set_yticks(np.linspace(0, 100, 21))
ax.set_ylabel("Pourcentage de la population intouchée")
ax.set_xticks(np.linspace(0, 100, 21))
ax.set_xlabel("Pourcentage de la population vaccinée")
ax.grid(True)
ax.plot(data)
plt.show()
