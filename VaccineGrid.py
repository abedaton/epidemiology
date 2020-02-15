import matplotlib.animation as animation #self.ani
import matplotlib as mpl #Couleurs
from matplotlib.backends.backend_qt5agg import FigureCanvas #Parent de PixelGrid

from matplotlib.figure import Figure #self.figure
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QPushButton,QSlider,QLabel,QSpinBox,QMessageBox
from PyQt5.QtCore import Qt
import sys

from Menu import Menu

from VaccineModel import VaccineModel


statesName = ['Susceptible', 'Infecté', 'Vacciné', 'Guéri']
nbStates = len(statesName)


class PixelGridVaccined(FigureCanvas):
    """docstring for PixelGrid."""

    def __init__(self, parametres={}):
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
        self.createProgressStamp()



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

    def createProgressStamp(self):
        axtext = self.figure.add_axes([0,0.05,0.1,0.05])
        axtext.axis("off")

    def refreshHeatmap(self, frame):
        #Mise a jour de la matrice
        if self.spreadingIsRunning:
            self.stepInfection()
        #Mise a jour du t =
        #mise a jour de la heatmap
            self.image.set_data(self.modele.population)
        else:
            print("END")
            self.ani.event_source.stop()

    def animate(self, stepTimeInterval=10, nbSteps=51):
        #Création de l'objet qui va appeller refreshmap tous les stepTimeInterval ms
        self.ani = animation.FuncAnimation(self.figure, self.refreshHeatmap,\
        interval=stepTimeInterval, frames=nbSteps, repeat=True)




class PixelGridWindowVaccined(QWidget):
    """docstring for window."""

    def __init__(self, parent=None):
        super(PixelGridWindowVaccined, self).__init__(parent)

        self.title = "Evolution d'une maladie avec vaccin"

        self.layout = QVBoxLayout(self)
        self.layout_but = QVBoxLayout(self)
        self.layout_param_init = QHBoxLayout(self)
        self.layout_vaccin = QVBoxLayout(self)
        self.layout_transmission = QVBoxLayout(self)
        self.layout_I0 = QVBoxLayout(self)
        self.layout_cured = QVBoxLayout(self)


        self.button = QPushButton('Lancer simulation', self)
        self.button.setToolTip('Relance la simulation')
        self.button.clicked.connect(self.new_plot)

        self.button2 = QPushButton('Menu', self)
        self.button2.setToolTip('reviens au menu pour choisir un autre modèle')
        self.button2.clicked.connect(self.back_menu)

        self.text_vaccin = QLabel("Pourcentage de vaccinés : 50")

        self.text_transmission = QLabel("Pourcentage de transmission : 100")

        self.text_cured = QLabel("Pourcentage de chance de guérir : 13")

        self.vaccin = QSlider(Qt.Horizontal)
        self.vaccin.setRange(0,99)
        self.vaccin.setValue(50)
        self.vaccin.valueChanged.connect(self.vaccineChanged)

        self.transmission = QSlider(Qt.Horizontal)
        self.transmission.setRange(0,100)
        self.transmission.setValue(100)
        self.transmission.valueChanged.connect(self.transmissionChanged)

        self.cured = QSlider(Qt.Horizontal)
        self.cured.setRange(0,100)
        self.cured.setValue(13)
        self.cured.valueChanged.connect(self.curedChanged)

        self.I0_but = QSpinBox()
        self.I0_but.setRange(0,25)
        self.I0_but.setValue(1)

        self.I0_text = QLabel("Nombre d'infectés")

        self.layout_I0.addWidget(self.I0_text)
        self.layout_I0.addWidget(self.I0_but)

        self.layout_but.addWidget(self.button)
        self.layout_but.addWidget(self.button2)

        self.layout_vaccin.addWidget(self.text_vaccin)
        self.layout_vaccin.addWidget(self.vaccin)

        self.layout_transmission.addWidget(self.text_transmission)
        self.layout_transmission.addWidget(self.transmission)

        self.layout_cured.addWidget(self.text_cured)
        self.layout_cured.addWidget(self.cured)


        self.layout_param_init.addLayout(self.layout_vaccin)
        self.layout_param_init.addLayout(self.layout_cured)
        self.layout_param_init.addLayout(self.layout_transmission)
        self.layout_param_init.addLayout(self.layout_I0)
        self.layout_param_init.addLayout(self.layout_but)
        self.layout.addLayout(self.layout_param_init)
        self.setLayout(self.layout)

        self.canvas = PixelGridVaccined()
        self.layout.addWidget(self.canvas)
        #self.PopUpEnd()

        self.canvas.startInfection()
        self.canvas.animate()

        self.showMaximized()

    def PopUpEnd(self):
        self.text_fin = QMessageBox()
        self.text_fin.setWindowTitle("Simulation finie")
        self.text_fin.setText("Bob") # mettre le bon texte d'une canvas
        self.text_fin.show()

    def vaccineChanged(self,value):
        self.text_vaccin.setText("Pourcentage de vaccinés : "+ str(value))
        #effectue le changement de parametres
        parametres = {'probVaccine' : value/100}
        self.canvas.modele.changeParam(parametres)

    def curedChanged(self,value):
        self.text_cured.setText("Pourcentage de chance de guérir : " + str(value))
        parametres = {'probCure' : value/100}
        self.canvas.modele.changeParam(parametres)

    def transmissionChanged(self,value):
        self.text_transmission.setText("Pourcentage de transmission : "+ str(value))
        #effectue le changement de parametres
        parametres = {'probInfect' : value/100}
        self.canvas.modele.changeParam(parametres)

    def getInputValue(self):
        parametres = {}
        parametres['probVaccine'] = self.vaccin.value()/100
        parametres['probInfect'] = self.transmission.value()/100
        parametres['I0'] = self.I0_but.value() # faut check lui il change mais pas dans le modele
        parametres['probCure'] = self.cured.value()/100
        #A rajouter : autres param
        return parametres

    def new_plot(self):
        parametres = self.getInputValue()
        self.canvas.modele.changeParam(parametres)
        self.canvas.clear()
        self.canvas.ani.event_source.start()
        self.canvas.startInfection()


    def back_menu(self):
        self.menu = Menu()
        self.close()




if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    InfectionWindow = PixelGridWindowVaccined()
    InfectionWindow.show()
    qapp.exec_()
