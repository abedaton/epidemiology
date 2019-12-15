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
        self.combo.addItem("SIER")
        self.combo.addItem("SIERS")
        
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
        
        

        
        self.show()
    def choose_model(self):
        from GUI_pyqt import App,SIR,SEIRS,SEIHFR,SEIHFBR
        model_name = self.combo.currentText()
        if (model_name == "SIR"):
            model = SIR()
        elif (model_name == "SEIRS"):
            model = SEIRS()
        elif (model_name == "SEIHFR"):
            model = SEIHFR()
        elif (model_name == "SEIHFBR"):
            pass
            #model = SEIHFBR()
        elif (model_name == "SIER"):
            pass
            #model = SIER()
        else:
            model = SEIRS()
        self.app2 = App(model)
        self.app2.show()
        self.close()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    sys.exit(app.exec_())