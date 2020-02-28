from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
                            QPushButton, QSlider,QHBoxLayout,QVBoxLayout,QTabWidget,QSpinBox, QLabel,\
                            QDoubleSpinBox,QComboBox

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys

from SIR import SIR
from SEIRS import SEIRS
from SEIHFR import SEIHFR
from SEIHFBR import SEIHFBR

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider,QHBoxLayout,QVBoxLayout,QTabWidget,QSpinBox, QLabel,QDoubleSpinBox,QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt

from GUI_pyqt import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QImage



class Menu(QWidget):

    def __init__(self, option=None):
        super().__init__()

        self.combo = QComboBox(self)
        self.combo.addItem("SIR")
        self.combo.addItem("SEIHFR")
        self.combo.addItem("SEIHFBR")
        self.combo.addItem("SEIRS")
        self.combo.addItem("Dispersion spatiale")
        self.combo.addItem("Effet du vaccin")
        self.combo.addItem("Map")

        self.comboMap = QComboBox(self)
        self.comboMap.addItem("PlateCarree")
        self.comboMap.addItem("Miller")
        self.comboMap.addItem("Mollweide")
        self.comboMap.addItem("EckertIII")
        self.comboMap.addItem("EuroPP")
        self.comboMap.hide()

        self.combo.currentIndexChanged.connect(lambda: self.showNewCombo() if self.combo.currentIndex() == 6 else self.comboMap.hide() if not self.comboMap.isHidden() else None)

        self.button = QPushButton("GO",self)
        self.button.clicked.connect(self.choose_model)
        self.button.keyPressEvent = self.keyPressEvent

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button)
        self.hbox.addWidget(self.combo)
        self.hbox.setAlignment(Qt.AlignCenter)

        #  vbox = QVBoxLayout(self)
        #  vbox.addStretch(1)
        #  vbox.addWidget(self.button2)
        #  vbox.addLayout(hbox)
        self.setLayout(self.hbox)

        if option is not None:
            if option == "SIR":
                self.choose_model(model_name="SIR")
            elif option == "SEIRS":
                self.choose_model(model_name="SEIRS")
            elif option == "SEIHFR":
                self.choose_model(model_name="SEIHFR")
            elif option == "SEIHFBR":
                self.choose_model(model_name="SEIHFBR")
            elif option == "spa":
                self.choose_model(model_name="Dispersion spatiale")
            elif option == "vac":
                self.choose_model(model_name="Effet du vaccin")
            elif option == "map":
                self.choose_model(model_name="Map")
            else:
                self.showMaximized()
        else:
            self.showMaximized()

    def setBackground(self, aimage, width = None, height = None):
        image = aimage.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        sImage = image.scaled(QSize(width, height))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            print("hey")
            self.choose_model()

    def choose_model(self, notUsed=None, model_name=None):
        from GUI_pyqt import App

        if model_name is None:
            model_name = self.combo.currentText()

        self.close()
        if model_name == "SIR":
            from GUI_pyqt import SIR
            self.app2 = App(SIR())
        elif model_name == "SEIRS":
            from GUI_pyqt import SEIRS
            self.app2 = App(SEIRS())
        elif model_name == "SEIHFR":
            from GUI_pyqt import SEIHFR
            self.app2 = App(SEIHFR())
        elif model_name == "SEIHFBR":
            from GUI_pyqt import SEIHFBR
            self.app2 = App(SEIHFBR())
        elif model_name == "Dispersion spatiale":
            from PixelGrid import PixelGridWindow
            self.app2 = PixelGridWindow()
        elif model_name == "Effet du vaccin":
            from VaccineGrid import PixelGridWindowVaccined
            self.app2 = PixelGridWindowVaccined()
        elif model_name == "Map":
            from map import MapWindow

            self.app2 = MapWindow("ccrs."+self.comboMap.currentText()+"()")

    def showNewCombo(self):
        self.hbox.addWidget(self.comboMap)
        self.comboMap.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        var = sys.argv.pop(1)
        menu = Menu(var)
    else:
        menu = Menu()
    sys.exit(app.exec_())
