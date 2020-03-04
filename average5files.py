import matplotlib.pyplot as plt
import numpy as np
data = np.empty(100)
i = 0
with open("1000iter-result.txt", 'r') as file1:
    with open("1000iter-results-2.txt", 'r') as file2:
        with open("1000iter-results-3.txt", 'r') as file3:
            with open("1000iter-results-4.txt", 'r') as file4:
                with open("1000iter-results-5.txt", 'r') as file5:
                    for i in range(100):
                        ligne1 = float(file1.readline()[:-1])
                        ligne2 = float(file2.readline()[:-1])
                        ligne3 = float(file3.readline()[:-1])
                        ligne4 = float(file4.readline()[:-1])
                        ligne5 = float(file5.readline()[:-1])
                        average = ligne1 + ligne2 + ligne3 + ligne4 + ligne5
                        average = average/5
                        print(average)
                        data[i] = 100*(float(average))/(2500-i*25-1)

print(len(data))
f, ax = plt.subplots(figsize=(1, 1))
#ax.set_title("Efficacité de la couverture vaccinale dans une population carrée de 2500 individus\n(Moyenne sur 5000 itération par pourcentage)")
ax.set_yticks(np.linspace(0, 100, 21))
#ax.set_ylabel("Population épargnée de la maladie (en %)", rotation=360, wrap=True, ha="right")
ax.set_xticks(np.linspace(0, 100, 21))
#ax.set_xlabel("Population vaccinée (en %)")
ax.grid(True)
ax.plot(data)
plt.show()
