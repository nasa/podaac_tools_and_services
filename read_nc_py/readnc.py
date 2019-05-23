#! /usr/bin/env python
# file: readnc.py
# $id: $

"""
SYNOPSIS:
Contains two functions which read and return
netCDF variables, variable attributes, and global
attributes to main program.

REQUIRES:
Python netCDF4 module. See:
http://code.google.com/p/netcdf4-python/

USAGE:
Requires usage of main program as follows:
% ncwrapper.py -f <filename>

"""

#import
from optparse import OptionParser
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

# ---------------------------
# read and return global_atts
# ---------------------------
def readGlobalAttrs( nc_file ):
  attr_list = []
  global_attr = []
  #print 'Global attributes:'
  for attr_name in nc_file.ncattrs():
      #print attr_name, '=', getattr(nc_file, attr_name)
      attr_list.append( attr_name )
      atts = getattr( nc_file, attr_name )
      global_attr.append( atts )
  return attr_list, global_attr 

# --------------------------------------------------
# read and return variables and their attributes 
# --------------------------------------------------
var_list = []
var_attr_list = []
var_data_list = []
def readVars ( nc_file ):
#print 'Variables:' 
#dictionary of variables:values
  vars =  nc_file.variables.keys()
  for var_name in vars:
      attr = nc_file.variables[var_name]
      vardata = nc_file.variables[var_name][:]
      var_attr_list.append( attr )
      var_data_list.append( vardata)
#      print var_name, ':', attr
#      print var_name, ' data sample[0:10]:', vardata[0:10]
  return vars, var_attr_list, var_data_list
