class TwoDiseasesModel(object):
    """docstring for TwoDiseasesModel."""

    def __init__(self, parametres):
        #H=100,L=100,n=6,I0=37,mwm=1,mmw=1,mww=0,mmm=0,bw=2,aw=1,R0w=2,bm=7.2,am=4,R0m=1.8,gl=False,loc=True
        defaultParam = {'nbRow' = 50, 'nbCol' = 20,'n' = 6, 'I0' = 37, 'mwm' = 1\
                        , 'mmw' = 1, 'mww' = 1, 'mmm' = 1, 'bw2' = 2, 'aw1' = 1,\
                         'R0w' = 2, 'bm' = 7.2, 'am' = 4, 'R0m' = 1.8,\
                         'gl' = False, 'local' = True}
        self.param = parametres

        for par in requiredParam:
            if par not in self.param:
                self.param[par] = defaultParam[par]


        lc=int(I0**0.5)

		i0=H//2-lc//2
		j0=L//2-lc//2

        i0 = rd.randrange(0, self.param['nbRow'])
        j0 = rd.randrange(0, self.param['nbCol'])

		for i in range (I0):
			self.mat[i0][j0]=1
			j0=j0+1
			if j0>int(H/2)+int(lc/2):
				j0=int(H/2)-int(lc/2)
				i0=i0+1
		if showMe:
			self.heatmap()

    def createGraph(self):
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
        self.image = hm.imshow(self.pixels, cmap=cmap, vmin=0,vmax=nbStates)
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
        self.image.set_data(self.pixels)

    def animate(self, stepTimeInterval=50, nbSteps=100):
        ani = animation.FuncAnimation(self.figure, self.refreshHeatmap,\
        interval=stepTimeInterval, frames=nbSteps, repeat=False)
        plt.show()
