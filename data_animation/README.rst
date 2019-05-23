

data_animation_1.py
====================

Data animation is an efficient way to visaulize the dataset quickly and may sometime inspire the new ideas from it.

Next we will show how to create the animation of global sea surface salinity (SSS) over the period 27-03-2015 to 16-04-2018 based on the 8-day running mean version 3.0 SMAP product from Remote Sensing Systems at a spatial resolution of 70km. The animation is published in PODAAC YouTube channel at https://www.youtube.com/watch?v=wadOEbvjl9s. 

The dataset can be downloaded from PODAAC Portal at 
https://podaac.jpl.nasa.gov/dataset/SMAP_RSS_L3_SSS_SMI_8DAY-RUNNINGMEAN_V3_70KM.

The python code creates all the animation frames from the downloaded SSS data files. Each frame represents one day of data for this dataset.

data_animation_2.py
====================

In this script, we'll explore another useful animation routine called FuncAnimation tool, which is used widely when the animation data is calculated in each iteration.

Here is the sample code. It uses one day global SST data, and the animation scans through the longitude and displays the SST latitudinal variation for each longitude.


data_animation_3.py
====================

In this final part, we will show you how to create picture frames using a python script and how to generate an animation from these picture frames.

The following python script shows the generation of each picture frame by using CMC0.1deg L4 SST dataset on July 24, 2016. 


mcolorbar_test.py and podaactools.py
====================================

In the python matlibplot package and other graphic producing packages such as IDL and Matlab, the colorbar function can only use one single colormap which may make it difficult to visualize or focus on the data in certain ranges.

We are currently in the process of developing the python podaactools package which will include many functions related to datasets. mcolorbar is one of them which we created to implement the colorbar with arbitrary number of colormaps.