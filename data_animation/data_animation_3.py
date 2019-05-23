#! /usr/bin/env python
#
# a skeleton script to animate one day of L4 file using python matplotlib library.
#
##################################
# user parameters to be editted: #
##################################

# Caution: This is a Python script, and Python takes indentation seriously.
# DO NOT CHANGE INDENTATION OF ANY LINE BELOW!

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.backends import backend_agg as agg # raster backend
from netCDF4 import Dataset

#Read init data
filename1 = '20160724120000-CMC-L4_GHRSST-SSTfnd-CMC0.1deg-GLOB-v02.0-fv03.0.nc'
ncin = Dataset(filename1, 'r')
lons = ncin.variables['lon'][:]
lats = ncin.variables['lat'][:]
sst = ncin.variables['analysed_sst'][:]
ncin.close()

#Setup figure object
parallels = np.arange(-90,90+30,30.)
meridians = np.arange(-180,180+60,60)
cmap=plt.get_cmap("jet")

plt.figure(figsize=(3.86, 3.86), dpi=100)

#Loop all frames
for alon in xrange(-180,180,2):
  # Set up the map
  # lat_ts is the latitude of true scale.
  # resolution = 'c' means use crude resolution coastlines.

  m = Basemap(projection='ortho', lon_0=alon, lat_0=20, resolution='c')
  m.shadedrelief(scale=0.1)
  m.drawcoastlines(color='0.4')
  m.drawcountries(color='0.4')
  m.drawparallels(np.arange(-90.,91.,30.))
  m.drawmeridians(np.arange(0., 360., 60.))
  m.drawmapboundary(fill_color='0.8')

  x, y = m(*np.meshgrid(lons, lats))
  clevs = np.linspace(270, 310, 21)

  cs=m.contourf(x, y, sst[0,:,:].squeeze(), clevs, cmap=cmap)
  cb = m.colorbar(cs, 'right', size='5%', pad='2%')
  cb.set_label('SST (K)', fontsize=12)

  m.fillcontinents(color='gray',lake_color='gray')

  plt.tight_layout()
  plt.savefig("frame{0}".format(str(alon+180).rjust(4, "0")))
  plt.clf()