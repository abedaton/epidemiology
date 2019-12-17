import random as rd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import numpy as np
import sys

from modele_graph import modele

VIRGIN = 0
INFECTED = 1
IMMUNE = 2
DEAD = 3
statesName = ['Susceptible', 'Wild_infected', 'Virulent_infected', 'Dead']
nbStates = len(statesName)


class PixelGrid(object):
    """docstring for PixelGrid."""

    def __init__(self, sizeX, sizeY, seed=None, infectNeighbourProb=0.2, cureProb=0.1, dieProb=0.05, base = 0):
        if len(sys.argv) > 1 :
            loca='1' in str(sys.argv[1])
            globa='1' in str(sys.argv[2])
            self.modele = modele(loc=loca,gl=globa)
        else:
            self.modele=modele()
        self.seed = seed
        self.X = sizeX
        self.Y = sizeY
        self.pixels = np.full((sizeY, sizeX), base)
        self.susceptible = set()
        self.infected = set()
        self.recovered = set()
        self.dead = set()
        self.infectNeighbourProb=infectNeighbourProb
        self.cureProb=cureProb
        self.dieProb=dieProb

    def __getitem__(self, key):
        return self.modele[key[0]][key[1]]

    def startInfection(self, I0=1):
        for patientsZero in range(I0):
            i = rd.randrange(0,self.Y)
            j = rd.randrange(0,self.X)
            self.infect((i,j))
        self.createGraph()

    def canBeInfected(self, cell):
        return cell not in self.infected and\
               cell not in self.recovered and\
               cell not in self.dead

    def infect(self, cell):
        if self.canBeInfected(cell):
            self.pixels[cell] = INFECTED
            self.infected.add(cell)

    def immunize(self, cell):
        self.pixels[cell] = IMMUNE
        self.infected.remove(cell)
        self.recovered.add(cell)

    def die(self, cell):
        self.pixels[cell] = DEAD
        self.infected.remove(cell)
        self.dead.add(cell)

    def stepInfection(self):
        self.modele.spread()

    def createGraph(self, cmap='hot'):
        gs = GridSpec(3,3) #Création d'un layout 3 rows 3 column
        #création de la fenêtre
        self.figure = plt.figure()

        self.createHeatmap(gs)
        self.createProgressStamp()
        self.createParamStamp()



    def createHeatmap(self, gs):
        hm = self.figure.add_subplot(gs[0:3,:])
        hm.set_title("Modélisation d'une infection.")
        cmap = mpl.colors.ListedColormap(['white', 'red', 'blue', 'black'])
        #création heatmap avec colorbar
        self.image = hm.imshow(self.modele.mat, cmap=cmap, vmin=0,vmax=nbStates)
        cbar = self.createColorBar(hm)


    def createColorBar(self, hm):
        cbar = self.figure.colorbar(self.image, ax=hm,ticks=np.arange(0,nbStates+1,1))
        cbar.ax.set_yticklabels(statesName)
        return cbar

    def createProgressStamp(self):
        axtext = self.figure.add_axes([0,0.05,0.1,0.05])
        axtext.axis("off")
        self.timeStep = axtext.text(0.5,0.5, str(0), ha="left", va="top")

    def createParamStamp(self):
        axtext = self.figure.add_axes([0,0.95,0.1,0.05])
        axtext.axis("off")
        param = axtext.text(0.5,0.5, str(0), ha="left", va="top")
        text = "Seed= " + str(self.seed) + " I=" + str(self.infectNeighbourProb) + " C=" + str(self.cureProb) + " D=" + str(self.dieProb)
        print(text)
        param.set_text(text)


    def refreshHeatmap(self, frame):
        self.stepInfection()
        self.timeStep.set_text(str("t=") + str(frame))
        self.image.set_data(self.modele.mat)

    def animate(self, stepTimeInterval=50, nbSteps=150):
        ani = animation.FuncAnimation(self.figure, self.refreshHeatmap,\
        interval=stepTimeInterval, frames=nbSteps, repeat=False)
        plt.show()


    def neighbors(self, host):
        i = host[0]
        j = host[1]
        res = [(i-1, j-1), (i-1,j), (i-1,j+1), \
               (i,j-1),               (i,j+1), \
               (i+1, j-1), (i+1,j), (i+1,j+1)  ]
        return [(i,j) for i,j in res if 0 <= i < self.Y and 0 <= j < self.X]

def luckCheck(lowerThan):
    return rd.uniform(0,1) <= lowerThan

def parseParametres(argv):
    seed = float(argv[1]) if len(argv) > 1 else rd.randrange(sys.maxsize)
    I = float(argv[2]) if len(argv) > 2 else 0.2
    C = float(argv[3]) if len(argv) > 3 else 0.1
    D = float(argv[4]) if len(argv) > 4 else 0.05
    return seed, I, C, D

if __name__ == '__main__':
    param = parseParametres(sys.argv)

    rd.seed(param[0])
    print("Seed =", param[0])
    for elem in param[1:]:
        print(elem)
    test = PixelGrid(30,30, *param)
    test.startInfection()
    test.animate()
    print(test.pixels)
