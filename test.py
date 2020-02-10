# GUI
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton


# Geocoding / Map
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import pycristoforo as pyc
import fiona
from shapely.geometry import Point
import shapely.geometry as sgeom
from shapely.prepared import prep
import reverse_geocoder as rg
import country_converter as coco

import numpy as np
import random
import sys
from Menu import Menu

class MapDia(QDialog):
    def __init__(self, parent=None):
        super(MapDia, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.go = False
        self.startCountry = None
        self.cc = coco.CountryConverter()

        #plt.ion()
        self.ax = plt.axes(projection=ccrs.PlateCarree())
        self.ax.stock_img()

        self.button = QPushButton("Commencer l'épidemie")
        self.button.clicked.connect(self.plot)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()
        
    def launch(self):
        country = self.waitForStart()

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

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

    def transformToCountry(self, x, y):
        geoms = fiona.open(
            shpreader.natural_earth(resolution='50m',
                                    category='physical', name='land'))

        land_geom = sgeom.MultiPolygon([sgeom.shape(geom['geometry'])
                                        for geom in geoms])

        land = prep(land_geom)
        if x != None and y != None:
            on = land.contains(sgeom.Point(x, y))
            if on:
                result = rg.search((y, x))
                country = self.cc.convert(names=result[0]["cc"], to="name_short")
                print("Starting in", country)
                plt.title("Starting in " + str(country), fontsize=50)
                self.go = True
                return country
            else:
                print("Mer")
                plt.title("Please choose a location on land !", fontsize=50)

    def waitForStart(self):
        while not self.go:
            location = plt.ginput(1, timeout=0)
            country = self.transformToCountry(location[0][0], location[0][1])
        return country

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MapDia()
    main.show()

    sys.exit(app.exec_())