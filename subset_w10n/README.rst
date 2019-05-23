Webification (W10n; https://podaac.jpl.nasa.gov/podaac_labs) for science is ReSTful web service technology providing simplified access to PODAAC data and metadata via HTTP/HTTPS protocols. W10n-sci supports major Earth science data formats like NetCDF and HDF 4/5, and abstracts an arbitrary data store as a hierarchical tree of nodes for each associated attributes which can be individually interrogated. Direct access to the inner components of the tree is made via HTTP requests from either a web browser, script or similar client. Results of w10n-sci calls return specified measurement arrays (or metadata elements) via subset by array value (v.s. subset by array index), and output in formats such as JSON, HTML, or netCDF as specified in the URL request.

In this recipe, the multiple array selector w10n API is used to subset level 2, level 3 and level 4 data granules:

http://host:port/path/store/.../{array0,array1,array2,...}/[selector]?output=format 

For example, to extract AMSR-E Level 2 Sea Surface Temperature (SST) data from 2011-01-01 to 2011-01-31 for a region bounded by -30 to -20 degrees longitude and -40 to 0 degrees latitude, this request can be made on the UNIX command line:

% ./subset_w10n.py -s 20110101 -f 20110131 -b -30 -20 -40 0 -x AMSRE-REMSS-L2P-v7a

where 'AMSRE-REMSS-L2P-v7a' is the shortname for the dataset. The shortname is a required field for the script to run. Without it the script will print out a help menu. 

The shortname can be found at the PO.DAAC dataset information page for each product