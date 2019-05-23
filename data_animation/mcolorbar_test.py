from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

import podaactools

ncin = Dataset('201210.ERSST.anomaly.nc', 'r')
sst = ncin.variables['sst'][:]
lons = ncin.variables['lon'][:]
lats = ncin.variables['lat'][:]
ncin.close()

sst = np.squeeze(sst)

print(sst.shape)

nlon = len(lons)
nlat = len(lats)

map = Basemap(resolution='c', projection='cyl', llcrnrlon=0, llcrnrlat=-90, urcrnrlon=360, urcrnrlat=90)
#map = Basemap(resolution='c', projection='robin',lon_0=0)


parallels = np.arange(-90,90,30.)
meridians = np.arange(0,360,60)

map.drawcoastlines(linewidth=0.25)
map.fillcontinents(color='black')

map.drawparallels(parallels,labels=[1,0,0,0],color='w', fontsize=10, fontweight='bold')
meri = map.drawmeridians(meridians,labels=[0,0,0,1],color='w', fontsize=10, fontweight='bold')

x, y = map(*np.meshgrid(lons, lats))

clevs = np.linspace(-1.0, 0.0, 11)
cmap=plt.get_cmap("winter")
cs1=map.contourf(x, y, sst, clevs, cmap=cmap)

clevs = np.linspace(0.0, 1.0, 11)
cmap=plt.get_cmap("cool")
cs2=map.contourf(x, y, sst, clevs, cmap=cmap)

clevs = np.linspace(1.0, 2.0, 11)
cmap=plt.get_cmap("Wistia")
cs3=map.contourf(x, y, sst, clevs, cmap=cmap)

clevs = np.linspace(2.0, 3.0, 11)
cmap=plt.get_cmap("Reds")
cs4=map.contourf(x, y, sst, clevs, cmap=cmap)

imgh = [cs1, cs2, cs3, cs4]

ax = plt.gca()

podaactools.mcolorbar(imgh, ax, location="horizontal", width="5%", height="100%", offset="-15%", 
                      vticks=range(-3,4,1), ticksize=10,
                      label='SST Anomaly (defreeF)', labelsize=12, label_offset="-8%")
podaactools.mcolorbar(imgh, ax, location="vertical", width="3%", height="100%", offset="3%", 
                      vticks=range(-3,4,1), ticksize=10,
                      label='SST Anomaly (defreeF)', labelsize=12, label_offset="6%")

plt.show()

