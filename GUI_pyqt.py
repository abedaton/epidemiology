import sys
from SEIRS import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider,QHBoxLayout,QVBoxLayout,QTabWidget,QSpinBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

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

        print(self.model.initial)
        print(self.model.vars)
        self.box = []
        self.population_name = QLabel()
        self.population_name.setText("Population totale")

        # out of tab
        self.population = QSpinBox()
        self.population.setRange(0,1000000)
        self.population.setValue(1000)
        self.population.setSingleStep(1000)

        self.layout_pop.addWidget(self.population_name)
        self.layout_pop.addWidget(self.population)

        self.layout_param_init.addLayout(self.layout_pop)


        for i in self.model.initial.keys():
            layout_box = QVBoxLayout()
            
            text = QLabel()
            text.setText(model.initial[i])

            but = QSpinBox()
            but.setRange(0,1000000)
            print(i)
            print(model.get(i))
            but.setValue(model.get(i))

            layout_box.addWidget(text)
            layout_box.addWidget(but)
            self.box.append((text,but))
            self.layout_param_init.addLayout(layout_box)

        for i in self.model.vars.keys():
            layout_box = QVBoxLayout()
            
            text = QLabel()
            text.setText(model.vars[i])

            but = QSpinBox()
            but.setRange(0,1)
            print(i)
            print(model.get(i))
            but.setValue(model.get(i))

            layout_box.addWidget(text)
            layout_box.addWidget(but)
            self.box.append((text,but))
            self.layout_proba.addLayout(layout_box)

        

        

        self.button = QPushButton('Lancer simulation', self)
        self.button.setToolTip('créer les nouveaux graphiques aves les nouvelles valeurs')
        self.button.clicked.connect(self.plop)

        self.layout_but.addWidget(self.button)


        
        self.layout_param_init.addLayout(self.layout_but)

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
        

        self.graph = PlotCanvas(self, width=5, height=4)

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
    def plop(self):
        print("hello")


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()


    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title(self.model.name) # à regarder
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = SEIRS() 
    ex = App(model) # prend la classe à créer en paramètre
    sys.exit(app.exec_())
