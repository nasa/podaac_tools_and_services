
#! /usr/bin/env python
#
# Caution: This is a Python script, and Python takes indentation seriously.
# DO NOT CHANGE INDENTATION OF ANY LINE BELOW!

from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import matplotlib
import os.path
from os import path
import os
import glob
import datetime

# Data Files Directory
data_dir = './8day_running/70KM/'

# set up map projection
parallels = np.arange(-90,90+30,30)
meridians = np.arange(0,360+60,60)

# setup contour levels and colarmap
clevs = np.linspace(32, 40, 101)
cmap=plt.get_cmap("jet")

cmap.set_under("black")
cmap.set_over("DarkViolet")

# setup figure object
plt.figure(figsize=(6, 3.375), dpi=300)

# read each data file in the list
nf = 0
for k in range(2015, 2019):
 for j in range(1, 367):
  strtemp = data_dir+str(k)+'/'+"{0:0>3}".format(j)+'/RSS_smap_SSS_L3_8day_running*v03.0.nc'
  for filename in glob.glob(strtemp):
    print(filename)
    ncin = Dataset(filename, 'r')
    lon = ncin.variables['lon'][:]
    lat = ncin.variables['lat'][:]
    data = ncin.variables['sss_smap'][:]
    ncin.close()
    lons,lats = np.meshgrid(lon,lat)

    m = Basemap(projection='cyl', llcrnrlon=0.0, llcrnrlat=-90.0,
        urcrnrlon=360, urcrnrlat=90.0)
    m.bluemarble()
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=6)
    meri = m.drawmeridians(meridians,labels=[1,0,0,1],fontsize=6)

    xx, yy = m(lons, lats)

    cs=m.contourf(lons,lats, data, clevs, cmap=cmap, extend='both')
    cb = m.colorbar(cs, 'right', size='2%', pad='0.5%')
    cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=6)
    cb.set_label('SSS (PSU)', fontsize=7,fontweight="bold")
    cb.set_ticks(range(32,41,1))

    d = datetime.date(k,1,1) + datetime.timedelta(j-1)

    plt.title(str(k)+"-"+'{0:02d}'.format(d.month) + "-"+'{0:02d}'.format(d.day)+" (RSS SMAP 70km 8Day)", fontsize=8, fontname="Times New Roman",fontweight="bold")

    nf = nf + 1

    plt.subplots_adjust(left=0.05, right=0.92, top=0.95, bottom=0.01)

    plt.savefig("frame{0}".format(str(nf).rjust(4, "0")), dpi = 300)

    plt.clf()