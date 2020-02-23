# -*- coding: utf-8 -*-

# GUI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLabel

# Geocoding / Map
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import fiona
from shapely.geometry import Point, LineString
import shapely.geometry as sgeom
from shapely.prepared import prep
import reverse_geocoder as rg
import country_converter as coco
import geopandas as gp
from cython.parallel import prange

import random
import time
import threading
from math import tanh, floor  # hyperbolic tangent

from Menu import Menu


class Map(QDialog):
    def __init__(self, proj = ccrs.PlateCarree(), parent = None):
        super(Map, self).__init__(parent)
        thread = threading.Thread(target=Map.uselessLoad)
        thread.start()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.go = False
        self.startCountry = None
        self.cc = coco.CountryConverter()

        plt.ion()
        self.ax = plt.axes(projection=proj)
        self.ax.stock_img()
        
        self.button = QPushButton("Commencer l'épidemie")
        # self.button.clicked.connect(self.plot)


        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()
        
    def launch(self):
        df = gp.read_file("shapes/useShape/useShape.shp")
        country = self.waitForStart()
        Propagation(df, coco.convert(names=country, to="ISO3"))

    def waitForStart(self) -> str:
        while not self.go:
            location = plt.ginput(1, timeout=0)
            country = self.transformToCountry(location[0][0], location[0][1])
        return country

    def transformToCountry(self, x: float, y: float) -> str:
        geoms = fiona.open(
            shpreader.natural_earth(resolution='50m', category='physical', name='land'))

        land_geom = sgeom.MultiPolygon([sgeom.shape(geom['geometry']) for geom in geoms])

        land = prep(land_geom)
        if x is not None and y is not None:
            on = land.contains(sgeom.Point(x, y))
            if on:
                result = rg.search((y, x))
                country_full = self.cc.convert(names=result[0]["cc"], to="name_short")
                country = self.cc.convert(names=result[0]["cc"], to="ISO3")
                print("Starting in", country_full)
                plt.title("Starting in " + str(country_full), fontsize=50)
                plt.scatter(x, y, color="black", marker=".", transform=ccrs.Geodetic())
                self.go = True
                return country
            else:
                print("Mer")
                plt.title("Please choose a location on land !", fontsize=50)
                return ""

    @staticmethod
    def uselessLoad():
        rg.search((0, 0), verbose=False)
    
    



class Country():
    def __init__(self, fullname : str , name : str, shape):
        self.fullname = fullname
        self.name = name
        self.shape = shape
        self.narea = self.normalizeArea()
        self.maxPoint = self.calcMaxPoints()
        self.nbrPoints = 0
        

    def normalizeArea(self) -> float:
        # Normalize Area betweeen 0 and 1
        # min of oldRange is 0.09251 and max is 2924.8
        oldRange = 2924.8 - 0.09251 
        newRange = 1
        newValue = (((self.shape.area - 0.09251) * newRange) / oldRange) + 0
        return newValue

    def calcMaxPoints(self) -> int:
        return floor(100*(tanh(self.narea + 0.10)))

    
    def printPoints(self) -> bool:
        if self.nbrPoints >= self.maxPoint: 
            return False
        else:
            points = self.findPoints()
            plt.scatter(points.x, points.y, color="red", marker=".", transform=ccrs.Geodetic())
            self.nbrPoints += 1
            return True

    def findPoints(self) -> Point:
        minx, miny, maxx, maxy = self.shape.bounds
        while True:
            points = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if self.shape.contains(points):
                return points


class Infection():
    def __init__(self):
        self.infected = []
        self.on = True
        thread = threading.Thread(target=self.infect)
        thread.start()
    
    def __del__(self):
        self.on = False
    
    def add(self, country : Country):
        self.infected.append(country)
        
    def infect(self):
        while self.on:
            i = 0
            while i < len(self.infected):
                if random.randint(1,10) < 4:
                    if not self.infected[i].printPoints():
                        self.infected.pop(i)
                        i -= 1
                    i += 1

class Susceptible():
    pass
                        

class Propagation():
    def __init__(self, df : gp.geodataframe.GeoDataFrame, startCountry : str): # StartCountry in ISO3
        self.df = df
        self.healthy = []

        self.initAll()
        
        self.succeptible = [startCountry]
        self.done = []

        self.infect = Infection()
        self.update(self.finde(startCountry, self.healthy))
        self.run = True
        thread = threading.Thread(target=self.spreading)
        thread.start()

    def initAll(self):
        for i in self.df.iterrows():
            self.healthy.append(self.makeContry(i[1][2]))
        

    def __del__(self):
        self.run = False

    def makeContry(self, name : str) -> Country:
        shape = self.df.loc[self.df["ISO3"] == name]["geometry"].tolist()[0]
        return Country(coco.convert(names=name, to="short_name"), name, shape)

    @staticmethod
    def finde(obj, list):
        for o in list:
            if o.name == obj:
                return o

    def spreading(self):
        #exemple
        while self.run:
            if random.randint(1,15) == 1:
                #global
                pass
            else:
                #local
                if len(self.succeptible) != 0: 
                    newInfected = random.choice(self.succeptible)
                    print(newInfected)
                    self.update(self.finde(newInfected, self.healthy))

    def update(self, country = Country):
        self.healthy.remove(country)
        self.infect.add(country)
        self.succeptible.remove(country.name)
        self.done.append(country.name)
 
        trash = ["Democratic People's Republic of"]
        neighborsList = self.df.loc[self.df["ISO3"] == country.name]["neighbors"].tolist()
        if len(neighborsList) != 0:
            neighborsList = neighborsList[0]
            if neighborsList is not None:
                neighborsList = neighborsList.split(", ")
                for i in trash:
                    if i in neighborsList:
                        neighborsList.remove(i)
                for neighbor in neighborsList:
                    neighbor = coco.convert(names=neighbor, to="ISO3")
                    if neighbor not in  self.succeptible + self.done:
                        self.succeptible.append(neighbor)



class MapWindow(QWidget):
    def __init__(self, argMap, parent=None):
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

        self.canvas = Map()

        self.layout.addWidget(self.canvas)

        
        
        self.showMaximized()
        self.canvas.launch()
    
    def new_plot(self):
        pass

    def back_menu(self):
        self.canvas.end()
        self.menu = Menu()
        self.close()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
                            QPushButton, QSlider,QHBoxLayout,QVBoxLayout,QTabWidget,QSpinBox, QLabel,\
                            QDoubleSpinBox,QComboBox

    app = QApplication(sys.argv)
    MapWindow("ccrs.()")
