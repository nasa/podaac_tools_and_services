This directory contains Python read software for:
Generic netCDF Datasets.

Python Subroutine:
 read.nc.py 	    : function to read netCDF variables and global attributes.

Python Main Program:
 ncwrapper.py	    : reads netCDF file, calls above subroutine and retrieves 
 		      all file contents.

USAGE:
 Primary: % ncwrapper.py -f <sample_file.nc>
 Alternate: % python ./ncwrapper.py -f <sample_file.nc>

Notes:
 Please check to verify that the permissions for ncwrapper.py have been set for 
executable for the primary user. 

Last modifed on 18 December 2012.

For questions or comments, please contact us at: podaac@podaac.jpl.nasa.gov.
