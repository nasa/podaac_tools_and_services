#!  /usr/bin/env python2
#

"""
This example shows how to read and create netCDF files.
"""

from netCDF4 import Dataset
import numpy as np
import os

### Read in sample netCDF file ##################################################################   

infilename='data/20160101-NCDC-L4LRblend-GLOB-v01-fv02_0-AVHRR_OI.nc'
ncin = Dataset(infilename, 'r')
lons = ncin.variables['lon'][:]
lats = ncin.variables['lat'][:]
sst = ncin.variables['analysed_sst'][:]
ncin.close()

nlat = lats.size
nlon = lons.size

### Write into netCDF file ######################################################################   

# Open the new file
outfilename = 'test.nc'
fid = Dataset(outfilename,'w', format='NETCDF3_64BIT')
# Define the dimensions
lat = fid.createDimension('lat', nlat) # Unlimited        
lon = fid.createDimension('lon', nlon) # Unlimited

fid.title = "This is a test file"
fid.institution = "PODAAC of JPL"
fid.summary = "One day of SST data"
fid.acknowledgment = "The data from PODAAC"
fid.date_created = "20151026" 

nc_var = fid.createVariable('lats', 'f8',('lat'))
fid.variables['lats'][:] = lats
fid.variables['lats'].standard_name='latitude'
fid.variables['lats'].units='degrees_north'
fid.variables['lats'].comment='Latitude'

nc_var = fid.createVariable('lons', 'f8',('lon'))
fid.variables['lons'][:] = lons
fid.variables['lons'].standard_name='longitude'
fid.variables['lons'].units='degrees_east'
fid.variables['lats'].comment='Longitude'

nc_var = fid.createVariable('sst', 'f8',('lon', 'lat'))
fid.variables['sst'][:] = sst
fid.variables['sst'].units='Kelvin'
fid.variables['sst'].comment='analysed_sst'

fid.close()
