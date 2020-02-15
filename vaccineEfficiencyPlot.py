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
            data[i] = float(ligne)
            i += 1
    return data

data = importData('100prob10iter-results.txt')
data = (100/2500)*data

f, ax = plt.subplots()
ax.set_yticks(np.linspace(0, 100, 21))
ax.set_ylabel("Pourcentage de la population intouchée")
ax.set_xticks(np.linspace(0, 100, 21))
ax.set_xlabel("Pourcentage de la population vaccinée")
ax.grid(True)
ax.plot(data)
plt.show()
