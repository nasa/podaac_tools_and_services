Dealing with large gridded datasets is challenging from the perspective of storage and access. Instead of downloading and storing large datasets locally it is often preferable to spatially subset them on a server side and store smaller pieces, or even use the pieces dynamically for an analysis and discard them. OPeNDAP is a popular service to extract subsets from data in netCDF and HDF.

Many GHRSST Level 4 datasets fit this characteristic of large volumes and the PO.DAAC OPeNDAP server (http://podaac-opendap.jpl.nasa.gov/opendap/allData/) can be used in a subsetting framework to extract subsets as needed from these granules. But OPeNDAP requires a granule (file) specific URL service call including variables and their proper grid index range to correctly perform the subsetting operation. This can be a tedious operation.

The python script opendayL4.pyis wrapper to OPeNDAP subsetting requests for GHRSST Level 4 datasets. In its current iteration it is “tuned” to the MUR dataset (http://podaac.jpl.nasa.gov/dataset/JPL-L4UHfnd-GLOB-MUR), but can be easily modified for others. For example, to extract MUR data from 2010-01-01 to 2010-01-05 for a region bounded by -140 to -110 degrees longitude and 10 to 50 degrees latitude, this request can be made on the UNIX command line:

% opendapL4.py --start 2010 01 01 --finish 2010 01 05 --region -140 -110 10 50

The program will first determine if it can find granules for the temporal period chosen and report the subsetted output grid dimensions. It will ask for download confirmation:

~~~~ example of screen output ~~~~~~~

First file: 20100101-JPL-L4UHfnd-GLOB-v01-fv04-MUR.nc
Last file: 20100105-JPL-L4UHfnd-GLOB-v01-fv04-MUR.nc
files obtained at 1-day interval

Longitude range: -140.000000 to -110.000000
Latitude range: 10.000000 to 50.000000
every 1 pixel(s) is obtained

grid dimensions will be ( 2731 x 3641 )

OK to download? [yes or no]: yes

~~~~~~ end example ~~~~~~~~

Once the request is accepted, the subsetted granules are downloaded to the local directory via a curl or wget system call. The output format is netCDF.

The program has dependencies on the python netCDF library and the aforementioned curl and wget system commands.

To modify this program for other datasets including non-GHRSST pay careful attention to parameters() subroutine and the root path defined by variable ‘L4URL’