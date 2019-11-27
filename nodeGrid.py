import matplotlib.pyplot as plt
import networkx as nx
from random import randint
import numpy as np
from scipy.integrate import odeint

class NodeGrid(object):
    """docstring for NodeGrid."""

    def __init__(self, n=1001, color_s='gray',color_i='red',scenario='global',t=10):
    
    
        self.n=n
        self.sizeX = 10
        self.sizeY = 5
        print(self.sizeX,self.sizeY)
        
        self.scenario=scenario
        self.s_Color = color_s #susceptible
        self.i_Color = color_i #infecté
        self.run_sim()
        self.prepareGraph()
        
        for i in range (t):
            self.plot()
            self.startInfection()
    
    def run_sim(self):
        I0=1
        R0 = 0
        N = 1001
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
        self.S=S
        self.I=I
        self.R=R

    def prepareGraph(self):
        self.G = nx.grid_2d_graph(self.sizeX, self.sizeY)

        # Sans le pos, le graphe s'imprime de manière aléatoire et non ordonée
        self.pos = dict( (n, n) for n in self.G.nodes() )
        # Sans le labels on voit rien, y'a un label automatique : (i,j)
        # sur chaque noeud
        self.labels = dict( ((i, j), " ") for i, j in self.G.nodes() )

        self.colors = [self.s_Color for i in range(len(self.G.nodes()))]

    def changeNodeAtColor(self, i, j, color):
        self.colors[i*self.sizeY + j] = color

    def startInfection(self, I=1):
        to_change=[]
        for i in range (self.sizeY):
            for j in range (self.sizeY):
                
                if self.colors[i*self.sizeY + j] == self.s_Color and self.scenario=='local':
                    if i>0 and randint(0,10)==1:
                        i_victim=i-1
                        j_victim=j
                        
                        self.changeNodeAtColor(i_victim,j_victim, 'red')
                        #to_change.append((i*j,i_victim*j_victim))
                        
                    if j>0 and randint(0,10)==1:
                        i_victim=i
                        j_victim=j-1
                        
                        self.changeNodeAtColor(i_victim,j_victim, 'red')
                        #to_change.append((i*j,i_victim*j_victim))
                        
                    if i<self.sizeY and randint(0,10)==1:
                        i_victim=i+1
                        j_victim=j
                        
                        self.changeNodeAtColor(i_victim,j_victim, 'red')
                        #to_change.append((i*j,i_victim*j_victim))
                          
                    if j<self.sizeX and randint(0,10)==1:
                        i_victim=i
                        j_victim=j+1

                        self.changeNodeAtColor(i_victim,j_victim, 'red')
                        #to_change.append((i*j,i_victim*j_victim))
         
                if self.colors[i*self.sizeY + j] == self.s_Color and self.scenario=='global':
                    if randint(0,10)==1:
                        i_victim=randint(0,self.sizeY)
                        j_victim=randint(0,self.sizeX)
                
                        self.changeNodeAtColor(i_victim,j_victim, 'red')
                        #to_change.append((i*j,i_victim*j_victim))
                    
        self.G.add_edges_from(to_change)

    def plot(self):
        nx.draw_networkx(self.G, pos=self.pos, labels=self.labels, node_color=self.colors )
        plt.show()

if __name__ == '__main__':
    NodeGrid()
