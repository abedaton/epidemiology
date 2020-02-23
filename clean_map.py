# -*- coding: utf-8 -*-
# GUI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLabel

# Geocoding / Map
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import fiona
from shapely.geometry import Point
import shapely.geometry as sgeom
from shapely.prepared import prep
import reverse_geocoder as rg
import country_converter as coco
import geopandas as gp

import random
import time
import threading
from cython.parallel import prange

from Menu import Menu


def uselessLoad():
    rg.search((0, 0), verbose=False)


class Map(QDialog):
    def __init__(self, proj=ccrs.PlateCarree(), parent=None):
        super(Map, self).__init__(parent)
        thread = threading.Thread(target=uselessLoad)
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
        self.button.clicked.connect(self.plot)


        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()



    def launch(self):
        country = self.waitForStart()
        self.run = True
        self.infect(0.0000001, coco.convert(names=country, to="ISO3"))

    def end(self):
        self.run = False
        plt.ioff()

    def plot(self):
        print("pouette")

    def updateSusceptible(self, infected_names: list, susceptibles: list, country: str, df: gp.geodataframe.GeoDataFrame) -> list:
        trash = ["Democratic People's Republic of"]
        neighborsList = df.loc[df["ISO3"] == country]["neighbors"].tolist()
        if len(neighborsList) == 0:
            return list(set(susceptibles))
        else:
            neighborsList = neighborsList[0]
        if neighborsList is not None:
            neighborsList = neighborsList.split(", ")
            for i in trash:
                if i in neighborsList:
                    neighborsList.remove(i)
            for neighbor in neighborsList:
                neighbor = coco.convert(names=neighbor, to="ISO3")
                if neighbor not in infected_names:
                    susceptibles.append(neighbor)
        return list(set(susceptibles))

    def infect(self, timeInterval: (int, float), Thecountry: str, startNum: int = 0, endNum: float = float("inf")) -> None:  # The country in ISO3
         #df = gp.read_file("shapes/myShapeISO.shp")  # contient tous les voisins de chaques pays
        df = gp.read_file("shapes/useShape/useShape.shp")
        infected = df.loc[df["ISO3"] == Thecountry]["geometry"].tolist()
        infected_names = [Thecountry]
        susceptibles = self.updateSusceptible(infected_names, [], Thecountry, df)

        while self.run and startNum < endNum:
            print("sus = ", susceptibles)
            count = 0
            while count < len(susceptibles):
                sus = susceptibles[count]
                prob = random.randint(0, 100)
                if prob >= 90:
                    print(coco.convert(names=sus, to="short_name"), "IS NOW INFECTED")
                    infected_names.append(sus)
                    infected.append(df.loc[df["ISO3"] == sus]["geometry"].tolist()[0])
                    susceptibles.remove(sus)
                    susceptibles = self.updateSusceptible(infected_names, susceptibles, sus, df)
                    plt.title(coco.convert(names=sus, to="short_name") + " IS NOW INFECTED", fontsize=50)
                else:
                    count += 1

            for i in prange(len(infected)):
                points = self.findPoints(infected[i])
                plt.scatter(points.x, points.y, color="red", marker=".", transform=ccrs.Geodetic())
                #time.sleep(timeInterval)
            startNum += 1
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()

    def findPoints(self, country) -> Point:
        minx, miny, maxx, maxy = country.bounds
        while True:
            points = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if country.contains(points):
                return points

    def transformToCountry(self, x: float, y: float) -> str:
        geoms = fiona.open(
            shpreader.natural_earth(resolution='50m',
                                    category='physical', name='land'))


        land_geom = sgeom.MultiPolygon([sgeom.shape(geom['geometry'])
                                        for geom in geoms])

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

    def waitForStart(self) -> str:
        while not self.go:
            location = plt.ginput(1, timeout=0)
            country = self.transformToCountry(location[0][0], location[0][1])
        return country


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
    #qapp = QApplication(sys.argv)
    Map = Map()
    #Map.infect(0.0000001, 1000, "China")
    #plt.waitforbuttonpress(0)
