import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pycristoforo as pyc
from shapely.geometry import Point

import random
import sys

from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvas


class Map(FigureCanvas):
    def __init__(self):
        self.figure = Figure()
        super().__init__(self.figure)
        plt.ion()  # mets en mode interactif
        self.ax = plt.axes(projection=ccrs.PlateCarree())  # dis quel type de map on veut
        self.ax.stock_img()  # Ajoute l'image au graph
        plt.show()
        self.infect(0.0000001, 1000, "China")
        plt.waitforbuttonpress(0)

    def infect(self, timeInterval, num, Thecountry):
        liste = [pyc.get_shape(Thecountry)]
        for i in range(num):
            rand = random.randint(0, 100)
            if rand <= 5:
                liste += pyc.get_shape("France")
            for country in liste:
                points = self.findPoints(country)
                x = points.x
                y = points.y
                plt.scatter(x, y, color="red", marker=".", transform=ccrs.Geodetic())
                plt.pause(timeInterval)


    def findPoints(self, country):
        minx, miny, maxx, maxy = country.bounds
        while True:
            points = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if country.contains(points):
                return points

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    Map = Map()
    Map.infect(0.0000001, 1000, "China")
    plt.waitforbuttonpress(0)
