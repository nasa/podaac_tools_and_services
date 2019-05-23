#! /usr/bin/env python
#
# a skeleton script to download a set of L2 files using w10n.
#
#
#   2016.08.20  Yibo Jiang, version 0

##################################
# user parameters to be editted: #
##################################

# Caution: This is a Python script, and Python takes indentation seriously.
# DO NOT CHANGE INDENTATION OF ANY LINE BELOW!

# Example:
# % ./subset_w10n.py -s 20100101 -f 20100205 -b -30 -20 -40 0 -x AMSRE-REMSS-L2P-v7a
# Subset the data from 1 Jan 2010 to 2 Jan 2010 in a box from -140 to -110 degrees longitude and 20 to 30 degrees latitude 
# for shortName AMSRE-REMSS-L2P-v7a.

import sys,os
import commands
import time
from datetime import date, timedelta
from optparse import OptionParser
import urllib

from xml.dom import minidom

#####################
# Global Parameters #
#####################

itemsPerPage = 10
PODAAC_WEB = 'http://podaac.jpl.nasa.gov'
w10n_root = "http://podaac-w10n.jpl.nasa.gov/w10n/"

###############
# subroutines #
###############

def today():
  import datetime
  todays=datetime.date.today()
  return str(todays.year)+str(todays.month).zfill(2)+str(todays.day).zfill(2)

def yesterday():
  import datetime
  yesterdays=datetime.date.today() - timedelta(days=1)
  return str(yesterdays.year)+str(yesterdays.month).zfill(2)+str(yesterdays.day).zfill(2)

def yearday(day,month,year):
  months=[0,31,28,31,30,31,30,31,31,30,31,30,31]
  if isLeap(year):
    months[2]=29
  for m in range(month):
    day=day+months[m]
  return(day)

def parseoptions():
  usage = "Usage: %prog [options]"
  parser = OptionParser(usage)
  parser.add_option("-x", "--shortname", help="product short name", dest="shortname")
  
  parser.add_option("-s", "--start", help="start date: Format yyyymmdd (eg. -s 20140502 for May 2, 2014) [default: yesterday %default]", dest="date0", default=yesterday())
  parser.add_option("-f", "--finish", help="finish date: Format yyyymmdd (eg. -f 20140502 for May 2, 2014) [default: today %default]", dest="date1", default=today())
  parser.add_option("-b", "--subset", help="limit the domain to a box given by lon_min,lon_max,lat_min,lat_max (eg. -r -140 -110 20 30) [default: %default]", 
			type="float", nargs=4, dest="box", default=(-180.,180.,-90.,90.))
  
  # Parse command line arguments
  (options, args) = parser.parse_args()

  # print help if no arguments are given
  if(len(sys.argv) == 1):
    parser.print_help()
    exit(-1)

  if options.shortname == None:
    print('\nShortname is required !\nProgram will exit now !\n')
    parser.print_help()
    exit(-1)

  return( options )

def standalone_main():
  # get command line options:

  options=parseoptions()

  shortname = options.shortname

  date0 = options.date0
  if options.date1==-1:
    date1 = date0
  else:
    date1 = options.date1

  if len(date0) != 8:
    sys.exit('\nStart date should be in format yyyymmdd !\nProgram will exit now !\n')
    
  if len(date1) != 8:
    sys.exit('\nEnd date should be in format yyyymmdd !\nProgram will exit now !\n')

  year0=date0[0:4]; month0=date0[4:6]; day0=date0[6:8];
  year1=date1[0:4]; month1=date1[4:6]; day1=date1[6:8];

  timeStr = '&startTime='+year0+'-'+month0+'-'+day0+'&endTime='+year1+'-'+month1+'-'+day1

  box = list( options.box )

  print '\nPlease wait while program searching for the granules ...\n' 

  wsurl = PODAAC_WEB+'/ws/search/granule/?shortName='+shortname+timeStr+'&itemsPerPage=1&sortBy=timeAsc&format=atom'
  response = urllib.urlopen(wsurl)
  data = response.read()

  if (len(data.splitlines()) == 1):
    sys.exit('No granules found for dataset: '+shortname+'\nProgram will exit now !\n')
    
  numGranules = 0
  doc = minidom.parseString(data)
  for arrays in doc.getElementsByTagName('link'):
   names = arrays.getAttribute("title")
   if names == 'OPeNDAP URL':
      numGranules = numGranules + 1
      href = arrays.getAttribute("href")

  if numGranules == 0 and len(data.splitlines()) < 30:
    sys.exit('No granules found for dataset: '+shortname+'\nProgram will exit now !\n')
  elif numGranules == 0 and len(data.splitlines()) > 30:
    sys.exit('No OpenDap access for dataset: '+shortname+'\nProgram will exit now !\n')

  samplefile = href.rsplit( ".", 1 )[ 0 ] + '.ddx'

  variable_list = []
  lon_order = 'X'
  lat_order = 'Y'
  nt = 1 #time dimension
  nd = 1 #depth dimension

  doc = minidom.parse(urllib.urlopen(samplefile))

  for arrays in doc.getElementsByTagName('Array'):
   names = arrays.getAttribute("name")
   if names == 'lat' or names == 'latitude':
     for dimensions in arrays.getElementsByTagName("dimension"):
       size = dimensions.getAttribute("size")
       name = dimensions.getAttribute("name")
       ni = int(size)
     for attrs in arrays.getElementsByTagName("Attribute"):
       aname = attrs.getAttribute("name")
       if aname == 'axis':
         for nodes in attrs.getElementsByTagName("value"):
           for cn in nodes.childNodes:
              lat_order = cn.nodeValue
   elif names == 'lon' or names == 'longitude':
     for dimensions in arrays.getElementsByTagName("dimension"):
       size = dimensions.getAttribute("size")
       name = dimensions.getAttribute("name")
       nj = int(size)
     for attrs in arrays.getElementsByTagName("Attribute"):
       aname = attrs.getAttribute("name")
       if aname == 'axis':
         for nodes in attrs.getElementsByTagName("value"):
           for cn in nodes.childNodes:
              lon_order = cn.nodeValue
   else:
     variable_list.append(names)

  try:
     ni # does a exist in the current namespace
  except NameError:
    sys.exit('Granule file format may not be in netcdf or no latitude or longitude info for dataset: '+shortname+'\n')

  #************************************************************************************
  # download size information:
  print ' '
  print 'Longitude range: %f to %f'%(box[0],box[1])
  print 'Latitude range: %f to %f'%(box[2],box[3])
  print ' '

  r=raw_input('OK to download?  [yes or no]: ')
  if len(r)==0 or (r[0]!='y' and r[0]!='Y'):
    print '... no download'
    sys.exit(0)

  # main loop:
  start = time.time()
  bmore = 1
  while (bmore > 0):
   if (bmore == 1):
       urllink = PODAAC_WEB+'/ws/search/granule/?shortName='+shortname+timeStr+'&itemsPerPage=%d&sortBy=timeAsc'%itemsPerPage
   else:
       urllink = PODAAC_WEB+'/ws/search/granule/?shortName='+shortname+timeStr+'&itemsPerPage=%d&sortBy=timeAsc&startIndex=%d'%(itemsPerPage, (bmore-1)*itemsPerPage)
   bmore = bmore + 1
   response = urllib.urlopen(urllink)
   data = response.read()
   doc = minidom.parseString(data)

   numGranules = 0
   for arrays in doc.getElementsByTagName('link'):
    names = arrays.getAttribute("title")
    if names == 'FTP URL':
      numGranules = numGranules + 1
      href = arrays.getAttribute("href")
      aindex = href.find("allData");
      str_temp = w10n_root + href[aindex:]
      ncfile = str_temp.rsplit( ".", 1 )[ 0 ]
      head, tail = os.path.split(str_temp)
      ncout = tail
      if ncout.endswith('.bz2') or ncout.endswith('.gz'):
        ncout = ncout.rsplit( ".", 1 )[ 0 ]
      ncout = ncout.rsplit( ".", 1 )[ 0 ]+'_subset.'+ncout.rsplit( ".", 1 )[ 1 ]
      cmd=ncfile+'.nc/{'
      cmd = cmd + 'sea_surface_temperature,lat,lon}'

      cmd=cmd+"/[%s<lat<%s,%s<lon<%s]?output=nc.4" % (box[2],box[3],box[0],box[1])

      status_curl, result = commands.getstatusoutput("which curl")
      status_wget, result = commands.getstatusoutput("which wget")

      if status_curl == 0:
        cmd='curl -g "'+cmd+'" -o '+ ncout
      elif status_wget == 0:
        cmd='wget "'+cmd+'" -O '+ ncout
      else:
        sys.exit('\nThe script will need curl or wget on the system, please install them first before running the script !\nProgram will exit now !\n')

      os.system( cmd )
      print ncout + ' download finished !'

   if numGranules < itemsPerPage:
     bmore = 0 

  end = time.time()
  print 'Time spend = ' + str(end - start) + ' seconds'

if __name__ == "__main__":
        standalone_main()
  

