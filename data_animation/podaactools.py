# Copyright 2017 California Institute of Technology.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def mcolorbar(imgh, ax, location="horizontal", width="5%", height="100%", offset="-15%", vticks=[], ticksize=10, label_offset="5", label="", labelsize=10):
  """
  Add a multiple colormap colorbar to a plot.

  Parameters
  ----------
  imgh         : list of image hangle returned from contour or img funtions
  ax           : current Axes instance, usually ax = plt.gca()
  location     : horizontal or vertical
  width        : in percentage
  height       : in percentage
  offset       : offset from the main plot in percentage
  ticksize     : tick size
  vticks       : tick value labels
  labelsize    : label size
  label        : colorbar label
  label_offset : offset from the main plot in percentage
  """

  bmargin=(1.0-float(height.strip('%'))/100.0)*0.5
  fheight = 1.0/len(imgh)
  cheight_float = (1.0-2.0*bmargin)*fheight
  cheight = "%.2f%%" % (cheight_float*100.0)
  offset=float(offset.strip('%'))/100.0
  label_offset=float(label_offset.strip('%'))/100.0
  for i in range(0,len(imgh)):
    if location == "horizontal":
       axins = inset_axes(ax, cheight, width, loc=3,
                   bbox_to_anchor=(bmargin+cheight_float*i, offset, 1, 1),
                   bbox_transform=ax.transAxes,
                   borderpad=0,
                   )
       cb = plt.colorbar(imgh[i], cax=axins, orientation="horizontal")
    elif location == "vertical":
       axins = inset_axes(ax, width, cheight, loc=3,
                   bbox_to_anchor=(1.0+offset, bmargin+cheight_float*i, 1, 1),
                   bbox_transform=ax.transAxes,
                   borderpad=0,
                   )
       cb = plt.colorbar(imgh[i], cax=axins)
    cb.ax.tick_params(labelsize=ticksize)
    # Customize colorbar tick labels
    cb.set_ticks(vticks)

  if location == "horizontal":
    plt.text(bmargin+cheight_float*len(imgh)*0.5, offset+label_offset, label,
       horizontalalignment='center',
       verticalalignment='center',
       fontsize=labelsize,
       transform = ax.transAxes)
  else:
    plt.text(1.0+offset+label_offset, bmargin+cheight_float*len(imgh)*0.5, label,
       horizontalalignment='center',
       verticalalignment='center',
       rotation=90,
       fontsize=labelsize,
       transform = ax.transAxes)

