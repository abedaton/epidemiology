from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
import sys
from PixelGrid import PixelGrid
import random as rd

SUSCEPTIBLE = 0
INFECTED = 1
TOBEINFECTED = 100
RECOVERED = 2
DEAD = 3
statesName = ['Susceptible', 'Infected', 'Recovered', 'Dead']
COLORS = [Qt.white, Qt.red, Qt.blue, Qt.black]
nbStates = len(statesName)


def luckCheck(lowerThan):
    return rd.uniform(0,1) <= lowerThan


class Cell(QWidget):
    """docstring for Cell."""

    def __init__(self, x, y, grid):
        super(Cell, self).__init__()
        self.x, self.y, self.grid = x, y, grid
        self.state = SUSCEPTIBLE
        self.setMinimumSize(20,20)
        self.setColor()

    def mousePressEvent(self, QMouseEvent):
        self.changeState(INFECTED)

    def setColor(self):
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), COLORS[0])
        self.setPalette(self.p)

    def refreshColor(self):
        self.p.setColor(self.backgroundRole(), COLORS[self.state])
        self.setPalette(self.p)

    def changeState(self, state):
        if (self.state == SUSCEPTIBLE and state == INFECTED) or\
           (self.state == INFECTED and state == RECOVERED)   or\
           (self.state == INFECTED and state == DEAD):
            self.state = state
        self.refreshColor()



class WidgetPixelGrid(QWidget):
    """docstring for WidgetPixelGrid."""

    def __init__(self, sizeX, sizeY, seed=None, infectNeighbourProb=0.2, cureProb=0.1, dieProb=0.05):
        super(WidgetPixelGrid, self).__init__()
        self.X, self.Y = sizeX, sizeY
        self.seed = seed
        self.infectNeighbourProb, self.cureProb = infectNeighbourProb, cureProb
        self.dieProb = dieProb
        self.createVars()
        self.createPixels()
        self.createButtonLayout()
        self.show()

    def createVars(self):
        self.cells = []
        self.susceptible = set()
        self.infected = set()
        self.recovered = set()
        self.dead = set()

    def createPixels(self):
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        for i in range(self.X):
            self.cells.append([])
            for j in range(self.Y):
                cell = Cell(i,j, self)
                self.cells[-1].append(cell)
                self.susceptible.add((i,j))
                self.layout.addWidget(self.cells[-1][-1], i, j)
        self.setLayout(self.layout)

    def createButtonLayout(self):
        self.buttonLayout = QGridLayout()
        self.layout.addLayout(self.buttonLayout, self.X, self.Y)
        self.step1Button = QPushButton("Etape(1)")
        self.step1Button.clicked.connect(self.tick)
        self.step5Button = QPushButton("Etape(5)")
        self.step5Button.clicked.connect(self.tick5)
        self.step10Button = QPushButton("Etape(10)")
        self.step10Button.clicked.connect(self.tick10)
        self.buttonLayout.addWidget(self.step1Button)
        self.buttonLayout.addWidget(self.step5Button)
        self.buttonLayout.addWidget(self.step10Button)

    def getNeighbors(self, i, j):
        res = [(i-1, j-1), (i-1,j), (i-1,j+1), \
               (i,j-1),               (i,j+1), \
               (i+1, j-1), (i+1,j), (i+1,j+1)  ]
        return [self.cells[i][j] for i,j in res if 0 <= i < self.X and 0 <= j < self.Y]

    def IGotInfected(self, pos):
        self.infected.add(pos)
        if pos in self.susceptible:
            self.susceptible.remove(pos)

    def tick5(self):
        for i in range(5):
            self.tick()

    def tick10(self):
        for i in range(10):
            self.tick()

    def tick(self):
        changeState = {}
        for i in range(self.X):
            for j in range(self.Y):

                if self.cells[i][j].state == INFECTED:
                    for n in self.getNeighbors(i,j):
                        if luckCheck(self.infectNeighbourProb):
                            changeState[(n.x, n.y)] = INFECTED
                    if luckCheck(self.cureProb):
                        changeState[(i,j)] = RECOVERED
                    elif luckCheck(self.dieProb):
                        changeState[(i,j)] = DEAD
        for i,j in changeState.keys():
            self.cells[i][j].changeState(changeState[(i,j)])


    def __getitem__(self, pos):
        return self.cells[pos[0]][pos[1]]


if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = WidgetPixelGrid(20,30)

    sys.exit(app.exec_())
