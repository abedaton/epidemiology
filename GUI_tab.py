import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Presentation:
    def __init__(self, N, I0, R0, S0, t, params):
        self.S0 = S0
        self.I0 = I0
        self.R0 = R0
        self.t = np.linspace(0, t, t)
        for param in params: # on extrait les paramétres et on les ajoutent en attribus
            setattr(self, param, params.get(param))
        self.colors = ["b", "r", "g", "yellow", "dimgray", "deepskyblue", "darkorange"]

        self.root = tk.Tk()
        self.root.title("Epidémie")
        self.tabControl = ttk.Notebook(self.root)          # Create Tab Control
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)            # Create a tab 
        self.var = tk.DoubleVar()
        
        self.slider = tk.Scale(self.root,variable = self.var,orient = "horizontal", digits = 3, length = 500, resolution=0.001, from_=0,to=2)
        self.slider.bind("<ButtonRelease-1>", self.updateValue)
        self.slider.pack()

        self.bob = tk.Scale(self.tab2,variable = self.var,orient = "vertical", digits = 3, length = 500, resolution=0.001, from_=0,to=2)
        self.bob.bind("<ButtonRelease-1>", self.updateValue)
        self.bob.pack()

        self.button = tk.Button(master=self.root, text="Quit", command=self._quit)
        self.button.pack(side=tk.BOTTOM)
        
        var = tk.DoubleVar(value=1000)
        self.N = tk.Spinbox(self.tab2, from_=0, to=100000, width=20,textvariable=var)
        self.N.pack()


        
        


    def updateValue(self, event):
        print ("Value = " + str(self.var.get()))
        print ("Value = " + str(self.N.get()))
    def _quit(self):
        self.root.quit()
        self.root.destroy()

    def plot(self,params):
        fig = plt.figure(facecolor="w")
        ax = fig.add_subplot(111, axisbelow = True)
        ax.set_xlabel("Time /days")
        ax.set_ylabel("Number")
        ax.set_ylim(0, 1.2)
        ax.set_xlim(0, 200)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which="major", c="w", lw=2, ls="-")
        for dx, elem in enumerate(params):
            ax.plot(self.t, params.get(elem)[0]/1000, self.colors[dx], alpha=0.5, lw=2, label = params.get(elem)[1])

        canvas = FigureCanvasTkAgg(fig, master=self.tab1) 
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.tab1)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.tabControl.add(self.tab1, text='Tab 1')      # Add the tab
        self.tabControl.add(self.tab2, text='Tab 2')
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible
        self.root.mainloop()
    def SIR(self, y, t):
        S, I, R = y
        N = int(self.N.get())
        dSdt = -self.beta * S * I / N
        dIdt = self.beta * S * I/N - self.gamma * I
        dRdt = self.gamma*I
        return dSdt, dIdt, dRdt
    
    def solve(self, model):
        if model == "SIR":
            ret = odeint(self.SIR, [self.S0, self.I0, self.R0], self.t) # Obliger de passer [S0, I0, R0] et de les utiliser en local car odeint() change leurs valeurs et on ne veut pas qu'elles soient changées en attributs
        elif model == "SEIHFR":
            ret = odeint(self.SEIHFR, [self.S0, self.E0, self.I0, self.H0, self.F0, self.R0], self.t)
        return ret.T

    def SEIHFR(self, y, t):
        S, E, I, H, F, R = y
        dSdt = -((self.betaI*S*I) + (self.betaH*S*H) + (self.betaF*S*F))/ self.N
        dEdt = (((self.betaI*S*I) + (self.betaH*S*H) + (self.betaF*S*F))/ self.N) - self.alpha*E
        dIdt = self.alpha*E-(self.gammaH*self.theta + self.gammaI*(1-self.theta)*(1-self.delta1) + self.gammaD*(1-self.theta)*self.delta1)*I
        dHdt = self.gammaH*self.theta*I - (self.gammaDH*self.delta2 + self.gammaIH*(1-self.delta2))*H
        dFdt = self.gammaD*(1-self.theta)*self.delta1*I + self.gammaDH*self.delta2*H - self.gammaF*F
        dRdt = self.gammaI*(1-self.theta)*(1-self.delta1)*I + self.gammaIH*(1-self.delta2)*H + self.gammaF*F
        return dSdt, dEdt, dIdt, dHdt, dFdt, dRdt

if __name__ == "__main__":
    SIR = Presentation(1001, 1, 0, 1000, 1000, {"beta" : 0.2, "gamma" : 1./10})
    S, I, R = SIR.solve("SIR")
    params = {"S" : [S, "(S)usceptible"], "I" : [I, "(I)nfected"], "R" : [R, "(R)ecovered"]}
    SIR.plot(params)

#S, I, R = SIR.solve("SIR")
#params = {"S" : [S, "(S)usceptible"], "I" : [I, "(I)nfected"], "R" : [R, "(R)ecovered"]}