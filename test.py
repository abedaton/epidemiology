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



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MapDia()
    main.show()

    sys.exit(app.exec_())
