import sys
import time

import numpy as np

from modele_graph import modele


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow,\
    QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ApplicationWindow(QWidget):
    def __init__(self, N=100, M=100, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        layout.addWidget(dynamic_canvas)

        #Création bouton start stop
        startStopButton = QPushButton("Démarrer", self)
        startStopButton.clicked.connect(self.startStop)

        self.modele = modele()


        self.canvas = dynamic_canvas.figure.subplots()
        self.timer = dynamic_canvas.new_timer(
            1, [(self.update_matrix, (), {})])
        self.timerRunning = False

    def startStop(self):
        if self.timerRunning:
            self.timer.stop()
        else:
            self.timer.start()
        self.timerRunning = not self.timerRunning

    def update_matrix(self):
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(self.modele.mat)
        fig.canvas.draw()
        #magie a faire ici


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
