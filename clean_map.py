# GUI
#import matplotlib.pyplot as plt
from matplotlib.pyplot import ion, axes, title, waitforbuttonpress, scatter, pause, ginput
from matplotlib.figure import Figure
#from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
from test import MapDia


class Map(FigureCanvas):
    def __init__(self, projectionType="ccrs.PlateCarree()"):
        self.figure = Figure()
        super().__init__(self.figure)
        self.go = False
        self.startCountry = None
        self.cc = coco.CountryConverter()

        ion()  # mets en mode interactif
        self.ax = axes(projection=eval(projectionType))  # dis quel type de map on veut
        self.ax.stock_img()  # Ajoute l'image au graph
        self.x0, self.x1, self.y0, self.y1 = self.ax.get_extent()

        title("Choose somewhere to start", fontsize=50)
        self.draw()
        #country = self.waitForStart()

        #self.infect(0.0000001, 1000, coco.convert(names=country, to="ISO3"))
        #waitforbuttonpress(0)

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
                scatter(x, y, color="red", marker=".", transform=ccrs.Geodetic())
                pause(timeInterval)

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
                title("Starting in " + str(country), fontsize=50)
                self.go = True
                return country
            else:
                print("Mer")
                title("Please choose a location on land !", fontsize=50)


    def waitForStart(self):
        while not self.go:
            location = ginput(1, timeout=0)
            country = self.transformToCountry(location[0][0], location[0][1])
        return country


class MapWindow(QWidget):
    def __init__(self,argMap, parent=None):
        super(MapWindow, self).__init__(parent)

        self.title = "Map Game"
        self.layout = QVBoxLayout(self)
        self.layout_but = QVBoxLayout(self)

        self.button = QPushButton('Lancer simulation', self)
        self.button.setToolTip('Relance la simulation')
        self.button.clicked.connect(self.new_plot)

        self.button2 = QPushButton('Menu', self)
        self.button2.setToolTip('reviens au menu pour choisir un autre modèle')
        self.button2.clicked.connect(self.back_menu)

        self.layout_but.addWidget(self.button)
        self.layout_but.addWidget(self.button2)

        self.layout.addLayout(self.layout_but)
        
        self.setLayout(self.layout)

        self.canvas = MapDia()
        self.layout.addWidget(self.canvas)

        
        
        self.showMaximized()
    
    def new_plot(self):
        pass
    def back_menu(self):
        self.menu = Menu()
        self.close()





if __name__ == "__main__":
    #qapp = QApplication(sys.argv)
    Map = Map()
    #Map.infect(0.0000001, 1000, "China")
    #plt.waitforbuttonpress(0)
