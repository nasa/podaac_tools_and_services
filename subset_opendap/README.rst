The script combines the PODAAC web granule spatial and temporal search service, and the OPeNDAP to subset and download most of the Level 3 and Level 4 datasets from PODAAC server.

The current version only works with Level 3 and Level 4 gridded datasets in netcdf format. Subsetting for level 2 datasets and hdf format is currently in progress and will be posted here once it is available.

Please note that you have to have the python software, wget or curl installed on the computer.


For example, to extract MUR data from 2010-01-01 to 2010-02-05 for a region bounded by -140 to -110 degrees longitude and 20 to 30 degrees latitude, this request can be made on the UNIX command line:

% ./subset_dataset.py -s 20100101 -f 20100205 -b -140 -110 20 30 -x MUR-JPL-L4-GLOB-v4.1

where JPL-L4UHfnd-GLOB-MUR is the short name for MUR dataset. Shortname is the required field for the script to run and the script will print out the help menu without the shortname. Shortname can be found from PODAAC web portal.