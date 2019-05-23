#! /usr/bin/env python
# file: ncwrapper.py
# $id: $

"""
SYNOPSIS:
Receives input from readnc.py and allows user to visualize customized input.

REQUIRES:
readnc.py subroutine
Python netCDF module. See:
http://code.google.com/p/netcdf4-python/

USAGE:
% ncwrapper.py -f <filename>

****************************************************************
Note: some systems may require the following usage variations:

% python ./ncwrapper.py -f <filename>

... or ...

% ./ncwrapper.py -f <filename>
****************************************************************
"""

#import
from optparse import OptionParser
import readnc
from netCDF4 import Dataset

# authorship
__author__     = "David Moroni"
__copyright__  = "Copyright 2012, California Institute of Technology"
__credits__    = ["Ed Armstrong and David Moroni"]
__license__    = "none"
__version__    = "1.0"
__maintainer__ = "David Moroni"
__email__      = "david.m.moroni at jpl dot nasa dot gov"
__status__     = "Release Candidate"

# Read command line using optparse module
print " ---- Print Variable and Global Attributes of a NetCDF file ---- \n"
parser = OptionParser( )
parser.add_option( "-f", "--file", dest="filename",
                  help="filename to validate metadata and structure", metavar="FILE",
		  type = 'string' )
(options, args) = parser.parse_args()

if not options.filename :
    parser.error("Specify a NetCDF file name!")
else :
    ncfile = options.filename

# -----------------------------
# Open netCDF4 file for reading
# -----------------------------
try:
    nc_file = Dataset( ncfile, 'r' )
except IOError:
    print 'not a valid netCDF file'

# ---------------------------
# read and print global_atts
# ---------------------------
print 'Global attributes:'
[attr_list, global_attr] = readnc.readGlobalAttrs( nc_file )
natts = len(attr_list)
for n in range(0, natts):
     print attr_list[n]," = ",global_attr[n]

# --------------------------------------------------
# read and print variables and their attributes 
# --------------------------------------------------
print '----------'
print 'Variables:' 
[vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )
nvars = len(vars)
print 'Number of variables = ', nvars
for i in range(0, nvars):
#    print vars[i], ': ', var_attr_list[i]
#    var = nc_file.createVariable(vars[i],'S1',(vars[i],))
#    print nc_file.variables[var]
    vardata = var_data_list[i]
    print '----------'
    print var_attr_list[i]
    print vars[i], '[0:10] =\n', vardata[0:10]

# close the file
nc_file.close()
