import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pycristoforo as pyc
from shapely.geometry import Point
import random

def init(projectionType):
    plt.ion()  # mets en mode interactif
    ax = plt.axes(projection=projectionType)  # dis quel type de map on veut
    ax.stock_img()  # Ajoute l'image au graph
    plt.show()


def infect(timeInterval, num, Thecountry):
    liste = [pyc.get_shape(Thecountry)]
    for i in range(num):
        rand = random.randint(0, 100)
        if rand <= 5:
            liste += pyc.get_shape("France")
        for country in liste:
            points = test(country)
            x = points.x
            y = points.y
            plt.scatter(x, y, color="red", marker=".", transform=ccrs.Geodetic())
            plt.pause(timeInterval)


def test(country):
    minx, miny, maxx, maxy = country.bounds
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if country.contains(p):
            return p

if __name__ == "__main__":
    init(ccrs.PlateCarree())
    infect(0.0000001, 1000, "China")
    plt.waitforbuttonpress(0)
