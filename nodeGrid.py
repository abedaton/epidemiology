import matplotlib.pyplot as plt
import networkx as nx
from random import randint
import numpy as np
from scipy.integrate import odeint
from all import *

class NodeGrid(object):
    """docstring for NodeGrid."""

    def __init__(self, scenario='global',N=101,I0=1,R0=0,S0=100,t=1000,param={"beta" : 0.2, "gamma" : 1./10},sim_type="SIR"):
        self.sizeX = int((N**0.5)+1)
        self.sizeY = int(N/int(N**0.5))
        
        self.N=N
        
        self.scenario=scenario
         
        #self.b_Color = 'grey'
        #self.s_Color = 'grey'
        #self.e_Color = 'blue'
        #self.i_Color = 'red'
        #self.r_Color = 'green'
        
        self.prepareGraph()
        
        Ep = Epidemy(N,I0,R0,S0,t,param)
        self.S, self.I, self.R = Ep.solve(sim_type)
        #pour l'instant, ne pas choisir autre chose que sir

        #print(len(self.S),len(self.I),len(self.R))
        
        #print(self.S[i],self.I[t],self.R[t])

        pas=10
        for i in range (0,t-1,pas):
        	   #print(self.S[i],self.I[i],self.R[i])
            self.plot(i,pas)

    def prepareGraph(self):
        self.G = nx.grid_2d_graph(self.sizeX, self.sizeY)

        # Sans le pos, le graphe s'imprime de manière aléatoire et non ordonée
        self.pos = dict( (n, n) for n in self.G.nodes() )
        # Sans le labels on voit rien, y'a un label automatique : (i,j)
        # sur chaque noeud
        self.labels = dict( ((i, j), " ") for i, j in self.G.nodes() )

        self.colors = ['grey' for i in range(len(self.G.nodes()))]

    def changeNodeAtColor(self, i, j, color):
        self.colors[i*self.sizeY + j] = color

    def plot(self,t,dt):
        #print(t,t-dt)
    	#to_change=[]
        #delta_e=
        #delta_s=int(((self.I[t]-self.R[t-1])/100)*self.N)
        delta_i=int(((self.I[t]-self.I[t-dt])/100)*self.N)
        delta_r=int(((self.R[t]-self.R[t-dt])/100)*self.N)
        
        
        #print((int(self.S[t-dt])/100)*self.N, (int(self.I[t])/100)*self.N, (int(self.R[t])/100)*self.N)
        #print((int(self.S[t])/100)*self.N, (int(self.I[t])/100)*self.N, (int(self.R[t])/100)*self.N)
        
        #Ajout des nouveaux infectés
        if delta_i>0:
            for new_victim in range (delta_i):
            	if 'grey' in self.colors:
                    _new_x=randint(0,self.sizeX)
                    _new_y=randint(0,self.sizeY)
                
                    col='red'

                    while col!='grey':
                        _new_x=randint(0,self.sizeX)
                        _new_y=randint(0,self.sizeY)
                        try:
                            col=self.colors[_new_x*self.sizeY + _new_y]

                        except:
                            col='red'

                    #to_change.append((i*j,i_victim*j_victim))
                    self.changeNodeAtColor(_new_x,_new_y,'red')


        #Ajout des nouveaux recovered
        if delta_r>0 :
            for new_victim in range (delta_r):
                if 'red' in self.colors:
                    _new_x=randint(0,self.sizeX)
                    _new_y=randint(0,self.sizeY)
                   
                    col='green'

                    while  col!='red':
                        _new_x=randint(0,self.sizeX)
                        _new_y=randint(0,self.sizeY)
                        try:
                        	col=self.colors[_new_x*self.sizeY + _new_y]
                        except:
                        	col='green'

 
                    #to_change.append((i*j,i_victim*j_victim))
                    self.changeNodeAtColor(_new_x,_new_y,'green')
                else:
                    print('erreur 404')
        #self.G.add_edges_from(to_change)

        nx.draw_networkx(self.G, pos=self.pos, labels=self.labels, node_color=self.colors )
        plt.show()

if __name__ == '__main__':
    NodeGrid()
