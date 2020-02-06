from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
                            QPushButton, QSlider,QHBoxLayout,QVBoxLayout,QTabWidget,QSpinBox, QLabel,\
                            QDoubleSpinBox,QComboBox

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys

from GUI_pyqt import *


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        
        
        self.combo = QComboBox(self)
        self.combo.addItem("SIR",)
        self.combo.addItem("SEIHFR")
        self.combo.addItem("SEIHFBR")
        self.combo.addItem("SEIRS")
        self.combo.addItem("Dispersion spatiale")
        
        #fond = 
        #Penser à rajouter une image de fond

        self.button = QPushButton("GO",self)
        self.button.clicked.connect(self.choose_model)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button)
        hbox.addWidget(self.combo)
        
        
        #vbox = QVBoxLayout(self)
        #vbox.addStretch(1)
        #vbox.addWidget(self.button2)
        
        #vbox.addLayout(hbox)
        self.setLayout(hbox)
        
        

        
        self.showMaximized()
    def choose_model(self):
        from GUI_pyqt import App,SIR,SEIRS,SEIHFR,SEIHFBR
        model_name = self.combo.currentText()
        if (model_name == "SIR"):
            model = SIR()
            self.app2 = App(model)
        elif (model_name == "SEIRS"):
            model = SEIRS()
            self.app2 = App(model)
        elif (model_name == "SEIHFR"):
            model = SEIHFR()
            self.app2 = App(model)
        elif (model_name == "SEIHFBR"):
            model = SEIHFBR()
            self.app2 = App(model)
        elif (model_name == "Dispersion spatiale"):
            self.disp = PixelGrindWindow()
        self.close()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    sys.exit(app.exec_())