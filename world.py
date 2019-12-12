import cartopy.crs as ccrs
import matplotlib.pyplot as plt 

import random
import time

plt.ion()

ax = plt.axes(projection = ccrs.PlateCarree())
ax.stock_img()

ny_lon, ny_lat = -75, 43
delhi_lon, delhi_lat = 77.23, 28.61
plt.show()

for i in range(5000):
    x = random.randint(-90, 90)
    y = random.randint(-180, 180)
    infected = bool(random.getrandbits(1))
    if infected:
        plt.scatter(x, y, color = "red" , marker='o', transform=ccrs.Geodetic())
    plt.pause(0.5)

