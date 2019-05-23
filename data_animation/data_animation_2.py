#! /usr/bin/env python
#
# a skeleton script to animate one day of L4 file using python matplotlib library.
#
##################################
# user parameters to be editted: #
##################################

# Caution: This is a Python script, and Python takes indentation seriously.
# DO NOT CHANGE INDENTATION OF ANY LINE BELOW!

from matplotlib import animation
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

#Read init data
filename1 = '20160724120000-CMC-L4_GHRSST-SSTfnd-CMC0.1deg-GLOB-v02.0-fv03.0.nc'
ncin = Dataset(filename1, 'r')
lons = ncin.variables['lon'][:]
lats = ncin.variables['lat'][:]
sst = ncin.variables['analysed_sst'][:]
ncin.close()

# setup figure object
parallels = np.arange(-90,90+30,30.)
meridians = np.arange(-180,180+60,60)
cmap=plt.get_cmap("jet")


fig = plt.figure(figsize=(4, 5.0), dpi=100)

ax1 = fig.add_subplot(2,1,1)

m = Basemap(projection='cyl', llcrnrlon=min(meridians), llcrnrlat=min(parallels),
        urcrnrlon=max(meridians), urcrnrlat=max(parallels))
x, y = m(*np.meshgrid(lons, lats))
clevs = np.linspace(270, 310, 21)

cs=m.contourf(x, y, sst[0,:,:].squeeze(), clevs, cmap=cmap)
m.drawcoastlines()
m.fillcontinents(color='#000000',lake_color='#99ffff')
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=8)
meri = m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=8)
scan_line, = m.plot([lons[0], lons[0]], [-90, 90], color='g', linewidth=5)

cb = m.colorbar(cs, 'right', size='5%', pad='2%')
cb.set_label('SST (K)', fontsize=8)
cb.ax.tick_params(labelsize=8)

ax2 = fig.add_subplot(2,1,2)

sst_line, = ax2.plot([],[], label='SST (K)', color='b', linewidth=2)
ax2.legend(loc='upper right',fontsize=10)
ax2.set_xlabel('SST (K)')
ax2.set_ylabel('Latitude (degree)')
ax2.set_xlim(270, 320)
ax2.set_ylim(-90, 90)

for item in ([ax2.title, ax2.xaxis.label, ax2.yaxis.label] +
             ax2.get_xticklabels() + ax2.get_yticklabels()):
    item.set_fontsize(10)

plt.tight_layout()

# Animate plot
def init():
    scan_line.set_data([], [])
    sst_line.set_data([], [])

    return sst_line, scan_line,


def animate(i,x,y,z,line,map_line):
    line.set_data(x[0,:,i], y)
    map_line.set_data([z[i], z[i]], [-90, 90])

    return line, map_line,

# call the animator.  blit=True means only re-draw the parts that have changed.
#anim = animation.FuncAnimation(fig, animate, init_func=init,
anim = animation.FuncAnimation(fig, animate, init_func=init, fargs=[sst,lats,lons,sst_line, scan_line],
                               frames=len(lons), interval=1, blit=True)


plt.show()
