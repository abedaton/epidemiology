import matplotlib.animation as animation #self.ani
import matplotlib as mpl #Couleurs
from matplotlib.backends.backend_qt5agg import FigureCanvas #Parent de PixelGrid

from matplotlib.figure import Figure #self.figure
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QPushButton,QSlider,QLabel,QSpinBox,QMessageBox
from PyQt5.QtCore import Qt
import sys
import random

from Menu import Menu

from VaccineModel import VaccineModel


statesName = ['Susceptible', 'Infecté', 'Vacciné', 'Guéri']
nbStates = len(statesName)


class PixelGridVaccined(FigureCanvas):
    """docstring for PixelGrid."""

    def __init__(self, parametres={}, parent=None):
        self.parent = parent
        self.figure = Figure()
        super().__init__(self.figure)
        self.modele=VaccineModel(parametres, parent=self)
        self.spreadingIsRunning = True
        self.ani = None

    def clear(self):
        self.modele.clear()
        self.ani.new_frame_seq()


    def startInfection(self, I0=1):
        self.spreadingIsRunning = True
        self.modele.buildFirstFrame()
        self.createGraph()

    def stepInfection(self):
        self.modele.spread()

    def createGraph(self):
        self.createHeatmap()



    def createHeatmap(self):
        #création graphe vide
        self.figure.clear()
        self.hm = self.figure.add_subplot()
        self.hm.set_title("Modélisation d'une infection.")
        self.hm.clear()
        #création colormap
        cmap = mpl.colors.ListedColormap(['white', 'red', 'blue','lime'])
        #création heatmap avec colorbar
        self.image = self.hm.imshow(self.modele.population, cmap=cmap, vmin=0,vmax=nbStates)
        cbar = self.createColorBar()


    def createColorBar(self):
        cbar = self.figure.colorbar(self.image, ax=self.hm,ticks=[i for i in range(nbStates+1)])
        cbar.ax.set_yticklabels(statesName)
        return cbar



    def refreshHeatmap(self, frame):
        #Si on a fini
        if not self.spreadingIsRunning:
            self.ani.event_source.stop()

        else:
            self.stepInfection()
            #mise a jour de la heatmap
            self.image.set_data(self.modele.population)


    def animate(self, stepTimeInterval=10, nbSteps=51):
        #Création de l'objet qui va appeller refreshmap tous les stepTimeInterval ms
        self.ani = animation.FuncAnimation(self.figure, self.refreshHeatmap,\
        interval=stepTimeInterval, frames=nbSteps, repeat=True)




class PixelGridWindowVaccined(QWidget):
    """docstring for window."""

    def __init__(self, parent=None):
        super(PixelGridWindowVaccined, self).__init__(parent)

        self.title = "Évolution d'une maladie dans une population vacciné à un certain pourcentage"

        self.layout = QVBoxLayout(self)

        buttonsLayout = self.createButtons()

        vaccLayout = self.createVaccLayout()
        tranLayout = self.createTranLayout()
        initLayout = self.createInitLayout()
        cureLayout = self.createCureLayout()

        paramLayout = self.createParamLayout([vaccLayout, cureLayout, tranLayout, initLayout, buttonsLayout])
        self.layout.addLayout(paramLayout)

        self.setLayout(self.layout)

        self.canvas = PixelGridVaccined(parent=self)
        self.resetParam()
        self.layout.addWidget(self.canvas)

        self.canvas.startInfection()
        self.canvas.animate()

        self.showMaximized()

    def setInputsToDefault(self):
        #Pour modifier les valeurs par défaut plus facilement
        self.vaccinSlider.setValue(50)
        self.transmissionSlider.setValue(100)
        self.I0SpinBox.setValue(1)
        self.cureSlider.setValue(13)

    def randomParam(self):
        self.vaccinSlider.setValue(random.randrange(self.vaccinSlider.minimum(), self.vaccinSlider.maximum()))
        self.transmissionSlider.setValue(random.randrange(self.transmissionSlider.minimum(), self.transmissionSlider.maximum()))
        self.I0SpinBox.setValue(random.randrange(self.I0SpinBox.minimum(), self.I0SpinBox.maximum()))
        self.cureSlider.setValue(random.randrange(self.cureSlider.minimum(), self.cureSlider.maximum()))


################################################################################
#Méthodes de créations des layout, bouttons, sliders, etc                      #
################################################################################
    def createButtons(self):
        layout = QVBoxLayout()

        #Boutton "Démarrer"
        startButton = QPushButton('Démarrer', self)
        startButton.setToolTip('Relancer la simulation')
        startButton.clicked.connect(self.new_plot)
        layout.addWidget(startButton)

        #Boutton "Appliquer les paramètres"
        self.randomButton = QPushButton('Paramètres aléatoires', self)
        self.randomButton.setToolTip('Randomiser tous les paramètres')
        self.randomButton.clicked.connect(self.randomParam)
        layout.addWidget(self.randomButton)

        #Button "Reset les paramètres"
        self.resetButton = QPushButton('Appliquer paramètres par défaut', self)
        self.resetButton.setToolTip('Réinisitalise les paramètres à leur valeur d\'origine')
        self.resetButton.clicked.connect(self.resetParam)
        layout.addWidget(self.resetButton)


        #Button "Retour au Menu"
        menuButton = QPushButton('Menu', self)
        menuButton.setToolTip('Retourner au menu')
        menuButton.clicked.connect(self.back_menu)
        layout.addWidget(menuButton)

        return layout



    def createVaccLayout(self):
        layout = QVBoxLayout()

        self.vaccinLabel = QLabel("50 % de la population est vaccinée")
        layout.addWidget(self.vaccinLabel)

        self.vaccinSlider = QSlider(Qt.Horizontal)
        self.vaccinSlider.setRange(0,99)
        self.vaccinSlider.valueChanged.connect(self.vaccineChanged)
        layout.addWidget(self.vaccinSlider)

        return layout



    def createTranLayout(self):
        layout = QVBoxLayout()

        self.transmissionLabel = QLabel("100 % de chance d'infecter 1 de ses 8 voisins")
        layout.addWidget(self.transmissionLabel)

        self.transmissionSlider = QSlider(Qt.Horizontal)
        self.transmissionSlider.setRange(0,100)
        self.transmissionSlider.valueChanged.connect(self.transmissionChanged)
        layout.addWidget(self.transmissionSlider)

        return layout



    def createInitLayout(self):
        layout = QVBoxLayout()

        I0Text = QLabel("Nombre d'infectés au temps 0")
        layout.addWidget(I0Text)

        self.I0SpinBox = QSpinBox()
        self.I0SpinBox.setRange(1,25)
        layout.addWidget(self.I0SpinBox)

        return layout



    def createCureLayout(self):
        layout = QVBoxLayout()

        self.cureLabel = QLabel("13 % de chance de devenir immunisé")
        layout.addWidget(self.cureLabel)

        self.cureSlider = QSlider(Qt.Horizontal)
        self.cureSlider.setRange(0,100)
        self.cureSlider.valueChanged.connect(self.curedChanged)
        layout.addWidget(self.cureSlider)

        return layout

    def createParamLayout(self, layoutList):
        returnLayout = QHBoxLayout()

        for layout in layoutList:
            returnLayout.addLayout(layout)

        return returnLayout



    def changeParam(self):
        parametres = {}
        parametres['probVaccine'] = self.vaccinSlider.value()/100
        parametres['probInfect'] = self.transmissionSlider.value()/100
        parametres['probCure'] = self.cureSlider.value()/100
        parametres['I0'] = self.I0SpinBox.value()
        #A rajouter : autres param
        self.canvas.modele.changeParam(parametres)
        #Les paramètres viennent d'être appliqués donc on peut bloquer appliquer
        self.resetButton.setDisabled(False)

    def resetParam(self):
        self.setInputsToDefault()
        self.canvas.modele.changeParam()

    def setEndMessage(self, message):
        self.canvas.ani.event_source.stop()
        self.text_fin = QMessageBox()
        self.text_fin.setWindowTitle("Simulation finie")
        self.text_fin.setText(message) # mettre le bon texte d'une canvas
        self.text_fin.show()

    def vaccineChanged(self,value):
        self.resetButton.setDisabled(False)
        self.vaccinLabel.setText(str(value) + " % de la population est vaccinée")

    def curedChanged(self,value):
        self.resetButton.setDisabled(False)
        self.cureLabel.setText(str(value) + " % de chance de devenir immunisé")

    def transmissionChanged(self,value):
        self.resetButton.setDisabled(False)
        self.transmissionLabel.setText(str(value) + " % de chance d'infecter 1 de ses 8 voisins")


    def new_plot(self):
        self.changeParam()
        self.canvas.clear()
        self.canvas.ani.event_source.start()
        self.canvas.startInfection()


    def back_menu(self):
        self.menu = Menu()
        self.canvas.ani.event_source.stop()
        self.close()




if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    InfectionWindow = PixelGridWindowVaccined()
    InfectionWindow.show()
    qapp.exec_()
