import matplotlib.pyplot as plt
import networkx as nx
from random import randint

class NodeGrid(object):
    """docstring for NodeGrid."""

    def __init__(self, sizeX=10, sizeY=5, color='gray'):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.baseColor = color
        self.prepareGraph()
        self.plot()
        self.startInfection()
        self.plot()

    def prepareGraph(self):
        self.G = nx.grid_2d_graph(self.sizeX, self.sizeY)
        # Sans le pos, le graphe s'imprime de manière aléatoire et non ordonée
        self.pos = dict( (n, n) for n in self.G.nodes() )
        # Sans le labels on voit rien, y'a un label automatique : (i,j)
        # sur chaque noeud
        self.labels = dict( ((i, j), " ") for i, j in self.G.nodes() )

        self.colors = [self.baseColor for i in range(len(self.G.nodes()))]

    def changeNodeAtColor(self, i, j, color):
        self.colors[i*self.sizeY + j] = color

    def startInfection(self, I=1):
        for i in range(I):
            j = randint(0, self.sizeY-1)
            i = randint(0, self.sizeX-1)
            self.changeNodeAtColor(i,j, 'red')

    def plot(self):
        nx.draw_networkx(self.G, pos=self.pos, labels=self.labels, node_color=self.colors )
        plt.show()


if __name__ == '__main__':
    NodeGrid()
