import os
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo import osr
import numpy as np
import math

#Plot setup
fig= plt.figure(figsize=(10,8))

ax = plt.subplot(111,aspect = 'equal')
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0)

#Map setup
map = Basemap(resolution='f', projection='cyl', llcrnrlon=-75, llcrnrlat=-5, urcrnrlon=-46, urcrnrlat=0)

parallels = np.arange(-50,50,1.)
meridians = np.arange(0,360,1)

map.drawparallels(parallels,labels=[1,0,0,0],color='w', fontsize=10, fontweight='bold')
meri = map.drawmeridians(meridians,labels=[0,0,0,1],color='w', fontsize=10, fontweight='bold')

#Load colormap and setup elevation contour levels
cmap=plt.get_cmap("jet")
clevs = np.linspace(0, 305, 21)

# Load GeoTiff data
raster = 'geo_dem_v2_52-50.tif'

ds = gdal.Open(raster)

#Get the dimentions of column and row
nc   = ds.RasterXSize
nr   = ds.RasterYSize

#Read elevation data
data = ds.ReadAsArray()

#Get Longitude and Latitude info
geotransform = ds.GetGeoTransform()
xOrigin      = geotransform[0]
yOrigin      = geotransform[3]
pixelWidth   = geotransform[1]
pixelHeight  = geotransform[5]

#Generate Longitude and Latitude array
lons = xOrigin + np.arange(0, nc)*pixelWidth
lats = yOrigin + np.arange(0, nr)*pixelHeight

#Contour plot
x, y = map(*np.meshgrid(lons, lats))
cs=map.contourf(x, y, data, clevs, cmap=cmap)

map.drawparallels(parallels,labels=[1,0,0,0],color='k', fontsize=10, fontweight='bold')
meri = map.drawmeridians(meridians,labels=[0,0,0,1],color='k', fontsize=10, fontweight='bold')

cb = map.colorbar(cs, 'bottom', size='5%', pad='10%')

cb.set_label('Elevation (m)', fontsize=12, fontweight='bold')
cb.ax.tick_params(labelsize=10)

plt.show()