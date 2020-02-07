import matplotlib.animation as animation #self.ani
import matplotlib as mpl #Couleurs
from matplotlib.backends.backend_qt5agg import FigureCanvas #Parent de PixelGrid

from matplotlib.figure import Figure #self.figure
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import sys

from Menu import Menu

from VaccineModel import VaccineModel

SUSCEPTIBLE = 0
INFECTED = 1
VACCINATED = 2
statesName = ['Susceptible', 'Infecté', 'Vacciné']
nbStates = len(statesName)


class PixelGridVaccined(FigureCanvas):
    """docstring for PixelGrid."""

    def __init__(self, parametres={}):
        self.figure = Figure()
        super().__init__(self.figure)
        self.modele=VaccineModel(parametres)


    def startInfection(self, I0=1):
        self.modele.startInfection()
        self.createGraph()

    def stepInfection(self):
        self.modele.spread()

    def createGraph(self):
        self.createHeatmap()
        self.createProgressStamp()



    def createHeatmap(self):
        #création graphe vide
        self.figure.clear()
        self.hm = self.figure.add_subplot()
        self.hm.set_title("Modélisation d'une infection.")
        self.hm.clear()
        #création colormap
        cmap = mpl.colors.ListedColormap(['white', 'red', 'blue'])
        #création heatmap avec colorbar
        self.image = self.hm.imshow(self.modele.population, cmap=cmap, vmin=0,vmax=nbStates)
        cbar = self.createColorBar()


    def createColorBar(self):
        cbar = self.figure.colorbar(self.image, ax=self.hm,ticks=[i for i in range(nbStates+1)])
        cbar.ax.set_yticklabels(statesName)
        return cbar

    def createProgressStamp(self):
        axtext = self.figure.add_axes([0,0.05,0.1,0.05])
        axtext.axis("off")
        self.timeStep = axtext.text(0.5,0.5, str(0), ha="left", va="top")

    def refreshHeatmap(self, frame):
        #Mise a jour de la matrice
        self.stepInfection()
        #Mise a jour du t =
        self.timeStep.set_text(str("t=") + str(frame))
        #mise a jour de la heatmap
        self.image.set_data(self.modele.population)

    def animate(self, stepTimeInterval=10, nbSteps=50):
        #Création de l'objet qui va appeller refreshmap tous les stepTimeInterval ms
        self.ani = animation.FuncAnimation(self.figure, self.refreshHeatmap,\
        interval=stepTimeInterval, frames=nbSteps, repeat=False)


class PixelGridWindowVaccined(QWidget):
    """docstring for window."""

    def __init__(self, parent=None):
        super(PixelGridWindowVaccined, self).__init__(parent)

        self.title = "Evolution d'une maladie avec vaccin"

        self.layout = QVBoxLayout(self)
        self.layout_but = QVBoxLayout(self)
        

        self.button = QPushButton('Lancer simulation', self)
        self.button.setToolTip('Relance la simulation')
        self.button.clicked.connect(self.new_plot)

        self.button2 = QPushButton('Menu', self)
        self.button2.setToolTip('reviens au menu pour choisir un autre modèle')
        self.button2.clicked.connect(self.back_menu)

        self.layout_but.addWidget(self.button)
        self.layout_but.addWidget(self.button2)

        self.canvas = PixelGridVaccined()
        
        self.layout.addLayout(self.layout_but)
        self.setLayout(self.layout)

        #Infecter des gens
        self.canvas.startInfection()
        #Démarrer le temps (big bang)
        self.canvas.animate()

        self.layout.addWidget(self.canvas)
        self.show()


    def new_plot(self):
        self.canvas.startInfection()
        self.canvas.animate()
    def back_menu(self):
        self.menu = Menu()
        self.close()



if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    InfectionWindow = PixelGridVaccined()
    InfectionWindow.show()
    qapp.exec_()
