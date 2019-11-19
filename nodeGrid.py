import matplotlib.pyplot as plt
import networkx as nx

class NodeGrid(object):
    """docstring for NodeGrid."""

    def __init__(self, sizeX=10, sizeY=5):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.prepareGraph()
        self.plot()

    def prepareGraph(self):
        self.G = nx.grid_2d_graph(self.sizeX, self.sizeY)
        # Sans le pos, le graphe s'imprime de manière aléatoire et non ordonée
        self.pos = dict( (n, n) for n in self.G.nodes() )
        # Sans le labels on voit rien, y'a un label automatique : (i,j)
        # sur chaque noeud
        self.labels = dict( ((i, j), " ") for i, j in self.G.nodes() )

    def plot(self):
        nx.draw_networkx(self.G, pos=self.pos, labels=self.labels)
        plt.show()


if __name__ == '__main__':
    NodeGrid()
