import sys

from SIR import SIR
from SEIRS import SEIRS
from SEIHFR import SEIHFR
from SEIHFBR import SEIHFBR

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider,QHBoxLayout,QVBoxLayout,QTabWidget,QSpinBox, QLabel,QDoubleSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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
        #self.layout_time = QVBoxLayout(self)

        print(self.model.initial)
        print(self.model.vars)
        self.box = []
        #self.population_name = QLabel()
        self.population_name.setText("Population totale")

        # out of tab

        ##set time
        #text = QLabel()
        #text.setText(self.model.initial[i])
        #self.time = QSpinBox()
        #self.time.setRange(10,10000)
        #self.layout_time.addWidget(text)
        #self.layout_time.addWidget(self.time)

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



        
        self.layout_param_init.addLayout(self.layout_but)
        #self.layout_param_init.addLayout(self.layout_time)
        

        self.layout.addLayout(self.layout_param_init)
        
        self.layout.addLayout(self.layout_proba)
        

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        

        self.graph = PlotCanvas(self, self.model, width=5, height=4)

        #self.slider = QSlider(Qt.Horizontal, self)
        #self.slider.setTickPosition(QSlider.TicksBothSides)
        #self.slider.setTickInterval(10)
        #self.slider.setSingleStep(1)

        #self.tab1.layout.addWidget(self.slider)
        self.tab1.layout.addWidget(self.graph)

        

        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        
        self.layout.addWidget(self.tabs)
        
        self.setLayout(self.layout)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()
    def new_plot(self):
        print("hello")
        for i in range (len(self.box)):
            self.model.set(self.box[i][0],self.box[i][1].value())
        self.graph.plot()
    def back_menu(self):
        self.menu = Menu()
        self.menu.show()
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
        self.plot()


    def plot(self,Color=['b','y','r','g','m',"c","k"]):
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

        ax.set_xlim(0,100)
        legend = ax.legend()
        ax.grid(True)
        self.draw()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = SEIRS() 
    ex = App(model) # prend la classe à créer en paramètre
    sys.exit(app.exec_())
