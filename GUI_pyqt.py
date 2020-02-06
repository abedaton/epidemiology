import sys

from SIR import SIR
from SEIRS import SEIRS
from SEIHFR import SEIHFR
from SEIHFBR import SEIHFBR

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider,QHBoxLayout,QVBoxLayout,QTabWidget,QSpinBox, QLabel,QDoubleSpinBox,QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Menu import Menu

class App(QWidget):

    def __init__(self,model):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = "Simulation d'épidémie"
        self.width = 640
        self.height = 400
        self.model = model

        self.layout = QVBoxLayout(self)
        self.layout_param_init = QHBoxLayout(self)
        self.layout_proba = QHBoxLayout(self)
        self.layout_pop = QVBoxLayout(self)
        self.layout_but = QVBoxLayout(self)
        self.layout_time = QVBoxLayout(self)

        print(self.model.initial)
        print(self.model.vars)
        self.box = []

        # out of tab

        ##set time
        text = QLabel()
        text.setText("limite de temps")
        self.time = QSpinBox()
        self.time.setRange(10,1000)
        self.time.setValue(100)
        self.layout_time.addWidget(text)
        self.layout_time.addWidget(self.time)

        for i in self.model.initial.keys():
            layout_box = QVBoxLayout()

            text = QLabel()
            text.setText(self.model.initial[i])

            but = QSpinBox()
            but.setRange(0,1000000)
            print(i)
            print(self.model.get(i))
            but.setValue(self.model.get(i))

            layout_box.addWidget(text)
            layout_box.addWidget(but)
            self.box.append((i,but))
            self.layout_param_init.addLayout(layout_box)

        for i in self.model.vars.keys():
            layout_box = QVBoxLayout()

            text = QLabel()
            text.setText(model.vars[i])

            but = QDoubleSpinBox()
            but.setRange(0,1)
            but.setSingleStep(0.01)
            print(i)
            print(model.get(i))
            but.setValue(model.get(i))

            layout_box.addWidget(text)
            layout_box.addWidget(but)
            self.box.append((i,but))
            self.layout_proba.addLayout(layout_box)





        self.button = QPushButton('Lancer simulation', self)
        self.button.setToolTip('créer les nouveaux graphiques aves les nouvelles valeurs')
        self.button.clicked.connect(self.new_plot)

        self.button2 = QPushButton('Menu', self)
        self.button2.setToolTip('reviens au menu pour choisir un autre modèle')
        self.button2.clicked.connect(self.back_menu)

        self.layout_but.addWidget(self.button)
        self.layout_but.addWidget(self.button2)



        self.layout_param_init.addLayout(self.layout_time)
        self.layout_param_init.addLayout(self.layout_but)



        self.layout.addLayout(self.layout_param_init)

        self.layout.addLayout(self.layout_proba)


        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Graphe")
        self.tabs.addTab(self.tab2,"Tableau de valeurs")

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.tableau = tableau(model)
        self.tab2.layout.addWidget(self.tableau.Mat)
        self.tab2.setLayout(self.tab2.layout)

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)


        self.graph = PlotCanvas(self, self.model, width=5, height=4)
        self.graph.plot(self.time)


        self.tab1.layout.addWidget(self.graph)



        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.showMaximized()

    def new_plot(self):
        for i in range (len(self.box)):
            self.model.set(self.box[i][0],self.box[i][1].value())
        self.graph.plot(self.time)

    def back_menu(self):
        self.menu = Menu()
        self.close()

class PlotCanvas(FigureCanvas):

    def __init__(self,parent=None,model = None, width=5, height=4, dpi=100):
        self.model = model
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def plot(self,time,Color=['b','y','r','g','m',"c","k"]):
        print(self.model.get("S0"))
        self.model.solveDifferential()
        ax = self.figure.add_subplot(111)
        ax.clear()
        for index, elem in enumerate(self.model.initial.keys()):
            var = self.model.get(elem[0])
            name = self.model.initial[elem]
            name = '('+name[0].upper()+')'+name[1:]
            ax.plot(self.model.timeVector,var,Color[index],label=name)
        ax.set_title(self.model.name)
        ax.set_xlabel('Time (in days)')
        ax.set_ylabel('Populaton (in person)')

        ax.set_xlim(0,time.value())
        legend = ax.legend()
        ax.grid(True)
        self.draw()


class tableau(object):
    def __init__(self,model):
        self.get_m(model)
        self.t=len(self.m[0])
        self.n_states=len(self.m)
        self.Mat=QWidget()
        Horizontal=QHBoxLayout(self.Mat)
        colonne=QWidget(self.Mat)
        Qcol=QVBoxLayout(colonne)
        Horizontal.addWidget(colonne)
        self.temp=self.creer_wid()
        self.actualiser(self.m)
        Qcol.addWidget(self.temp)
        
    def get_m(self,model):
        model.solveDifferential()
        Color=['b','y','r','g','m',"c","k"]

        #Obtention infos matrice
        self.names=[]
        for index, elem in enumerate(model.initial.keys()):
            name = model.initial[elem]
            self.names.append(name)
        t=len(model.timeVector)
        
        #Création matrice
        self.m=[[None for j in range (t)] for i in range (len(self.names))]
        
        #Remplissage matrice
        compteur=0
        for index, elem in enumerate(model.initial.keys()):
            var = model.get(elem[0])

            for c in range (len(var)):
            	self.m[compteur][c]=int(var[c])

            compteur=compteur+1


    def creer_wid(self):
        temp=QTableWidget()
        temp.setColumnCount(self.t)
        temp.setRowCount(self.n_states)
        temp.setVerticalHeaderLabels(self.names)
        return temp

    def actualiser(self,mat):
        for i in range (self.n_states):
            for j in range (self.t):
                self.temp.setItem(i,j,QTableWidgetItem(str(mat[i][j])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = SEIRS()
    ex = App(model) # prend la classe à créer en paramètre
    sys.exit(app.exec_())
