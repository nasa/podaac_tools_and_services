#! /usr/bin/env python
#
# a skeleton script to download a set of GHRSST L4 file using OPeNDAP.
#   mike.chin@jpl.nasa.gov
#
#   2011.04.06  mike chin, version 0
#   2011.04.25  mike chin, version 1
#   2012.08.29  mike chin, version 2
#   2013.10.30  mike chin, version 2 (bug fix)
#   2015.08.07  ricardo romanowski, version 3


##################################
# user parameters to be editted: #
##################################

# Caution: This is a Python script, and Python takes indentation seriously.
# DO NOT CHANGE INDENTATION OF ANY LINE BELOW!


# Here is the web-address (URL) for the GHRSST L4 file OPeNDAP server.
# You probably do not need to change this URL.  In fact, you can
# use this URL to search for the filename of the product you want to download.

#L4URL='http://podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/L4/'
L4URL='http://opendap.jpl.nasa.gov/opendap/hyrax/allData/ghrsst/data/L4/'
#L4URL='http://seastore.jpl.nasa.gov/opendap/hyrax/allData_nc4/ghrsst/data/L4/'

# Here you set the product names in 3 parts:
#   ncHead = main directory of the product.
#   ncBody = main file name of the product (file name minus "yyyymmdd").
#   ncTail = the part that indicates the compression method.
#
# You also specify the grid dimension of the product, which you need to
# know in advance, by setting the following 6 variables:
#   nlon = x-grid (longitudes) dimension in integer.
#   nlat = y-grid (latitudes) dimension in integer. 
#   dint = grid interval in degrees in float (assuming it's the same for x & y).
#   lon0 = the smallest longitude of the grid, in degrees in float.
#   lat0 = the smallest latitude of the grid, in degrees in float.
#   order = how "time" ,"lon", "lat" dimensions are ordered in the L4 file,
#           in array of three integers where 0=time, 1=lon, 2=lat.
#
# The code below might look complex, but it's only setting these 
# 3 names (strings) and 6 variables listed above.

logFileName='opendapL4.log'

def strmatch(a,b):
  return (a in b) and (b in a)

def parameters(product):

  productlist=[ \
  'mur/v4gds2', \
  'mur/v4', \
  'mur/v3', \
  'mur/ncamerica', \
  ]


  if strmatch( productlist[0], product.lower() ):
    ncHead='GLOB/JPL/MUR/'
    ncBody='090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv03.nc'
    ncTail='4'
    nlon=36000; nlat=17999 
    dint=0.01; lon0=-180.; lat0=-90.+dint
    order=[0,2,1]

  elif strmatch( productlist[1], product.lower() ):
    ncHead='GLOB/JPL/MUR/'
    ncBody='-JPL-L4UHfnd-GLOB-v01-fv04-MUR.nc'
    ncTail='.bz2'
    nlon=32768; nlat=16384 
    dint=45./(2**12); lon0=-180.+dint/2; lat0=-90.+dint/2
    order=[0,2,1]

  elif strmatch( productlist[2], product.lower() ):
    ncHead='GLOB/JPL/MUR/'
    ncBody='-JPL-L4UHfnd-GLOB-v01-fv03-MUR.nc'
    ncTail='.bz2'
    nlon=32768; nlat=16384 
    dint=45./(2**12); lon0=-180.+dint/2; lat0=-90.+dint/2
    order=[0,2,1]

  elif strmatch( productlist[3], product.lower() ):
    ncHead='NCAMERICA/JPL/MUR/'
    ncBody='-JPL-L4UHfnd-NCAMERICA-v01-fv02-MUR.nc'
    ncTail='.gz'
    nlon=13501; nlat=8201; 
    dint=0.01; lon0=-165.; lat0=-20. 
    order=[0,2,1]

  else:
    msg='\nNo such "product".\nAvailable products are:\n'
    for i in range(len(productlist)):
      msg=msg+'   '+productlist[i]+'\n'
    import sys
    sys.exit(msg)

  return(ncHead,ncBody,ncTail,nlon,nlat,dint,lon0,lat0,order)


# Done!!  
#
# Now get out of the editor and issue the command
#   opendapL4.py -h
# or
#   python opendapL4.py --help
# to see how you could specify
# the dates of the files and lon-lat box from the command line.

#############################################
# You're done.  No need to edit lines below #
#############################################


import sys,os
from math import floor,ceil
from optparse import OptionParser
from time import strftime # for adding a timestamp to the logfile

###############
# subroutines #
###############

def ncname(body,year,yday):
  (day,month)=calday(yday,year)
  return('%04d%02d%02d%s'%(year,month,day,body))  # for GDS1.x and GDS2.0

def pathname(head,body,tail,y,d):
  return( '%s%04d/%03d/%s%s' %(head,y,d,ncname(body,y,d),tail) )

def yearday(day,month,year):
  months=[0,31,28,31,30,31,30,31,31,30,31,30,31]
  if isLeap(year):
    months[2]=29
  for m in range(month):
    day=day+months[m]
  return(day)

def span(i1,i2,i3=1):
   return range(i1,i2+i3/abs(i3),i3)

def isLeap(year):
  flag = ( (year%4)==0) and ( not ( (year%100)==0 and (year%400)!=0 ))
  return(flag)

def calday(yday,year):
  months=[0,31,28,31,30,31,30,31,31,30,31,30,31]
  if isLeap(year):
    months[2]=29
  for m in span(1,12):
    months[m]=months[m]+months[m-1]
  for m in span(1,12):
    if (yday-1)/months[m]==0:
      month=m
      day=yday-months[m-1]
      return (day,month)
  import sys
  sys.exit('ERROR calday: yearday value out of range')

def cal2mjd(year,month,day):
  import math
  a = (14 - month) // 12
  y = year + 4800 - a
  m = month + (12 * a) - 3
  p = day + (((153 * m) + 2) // 5) + (365 * y)
  q = (y // 4) - (y // 100) + (y // 400) - 32045
  return int( math.floor(p + q - 2400000.5) )

def mjd2cal(mjd):
  y=(mjd-409)//366+1860
  while cal2mjd(y+1,1,1)<=mjd:
      y=y+1
  m=1
  while cal2mjd(y,m+1,1)<=mjd:
      m=m+1
  d=1
  while cal2mjd(y,m,d+1)<=mjd:
      d=d+1
  return(y,m,d)

def today(daysago=0):
  import datetime
  thisday=datetime.date.fromordinal(datetime.date.today().toordinal()-daysago)
  return( thisday.year, thisday.month, thisday.day )


def parseoptions(L4URL):
  usage = "usage: %prog [options] "
  parser = OptionParser(usage)
  parser.add_option("-p", "--product", help="product name [default: %default]",
                    dest="product", default="MUR/v4")
  parser.add_option("-s", "--start",
                    help="start date: yyyy mm dd [default: yesterday %default]",
                    type="int", nargs=3, dest="date0", default=today(1))
  parser.add_option("-f", "--finish",
                    help="finish date: yyyy mm dd [default: yesterday %default]",
                    type="int", nargs=3, dest="date1", default=today(1))
  parser.add_option("-d", "--dayspan",
                    help="sampling period in days [default: %default]",
                    type="int", dest="period", default=1)
  parser.add_option("-r", "--region", "-b", "--subset",
    help="limit the domain to a box given by lon_min,lon_max,lat_min,lat_max",
         type="float", nargs=4, dest="box", default=(-180.,180.,-90.,90.))
  parser.add_option("-g", "--gridspan",
                    help="sampling interval over grid [default: %default]",
                    type="int", dest="gridpoints", default=1)
  parser.add_option("-e", "--error", help="include uncertainty error field",
                    action="store_true", dest="includeError",default=False)
  parser.add_option("-l", "--landmask", help="include landmask field",
                    action="store_true", dest="includeLandMask",default=False)
  parser.add_option("-i", "--ice", help="include ice concentration field",
                    action="store_true", dest="includeIce",default=False)
  parser.add_option("-n", "--noSST", help="exclude SST field",
                    action="store_false", dest="includeSST",default=True)
  parser.add_option("-w", "--wget", help="use wget instead of curl",
                    action="store_true", dest="useWget",default=False)
  parser.add_option("-L", "--logfile", help="write log to file instead of stdout",
		    dest="useLogFile", metavar="FILE")
  parser.add_option("-q", "--quiet", help="suppress all output",
		    action="store_true", dest="quiet", default=False)
  parser.add_option("-T", "--target", help="target directory for downloaded files",
		   dest="targetDir", metavar="DIR")
  parser.add_option("-u", "--url", help="URL for GHRSST L4 OPeNDAP server [default: %default]", dest="URL", default=L4URL)
  parser.add_option("-t", "--test", help="only prints, without issuing, the OPeNDAP commands.",
                    action="store_true", dest="testing",default=False)
  (options, args) = parser.parse_args()
  if len(args) != 0:
        parser.error("incorrect number of arguments")
  return( options )



# get command line options:

options=parseoptions(L4URL)

L4URL = options.URL

date0 = options.date0
if options.date1==-1:
    date1 = date0
else:
    date1 = options.date1
year0=date0[0]; month0=date0[1]; day0=date0[2];
year1=date1[0]; month1=date1[1]; day1=date1[2];

dday = options.period

box = list( options.box )

ig = options.gridpoints

product = options.product
p=parameters(product)
ncHead=p[0];ncBody=p[1];ncTail=p[2]
nlon=p[3];nlat=p[4];dint=p[5];lon0=p[6];lat0=p[7];order=p[8]

# some path validation for TARGET and LOG options

if options.useLogFile: #in theory if someone would enter just "1", it could fail...
    logFile=os.path.abspath(options.useLogFile)
    if not options.quiet: print("All problems will be written to: "+logFile)

if options.targetDir:
    targetDir=os.path.abspath(options.targetDir)
    if not options.quiet: print("All downloaded files will be written to: "+targetDir+'/')

    if (not os.path.isdir(targetDir) or not os.path.exists(targetDir)):
        if not options.quiet:
            r=raw_input(targetDir+' does not exist yet. OK to create?  [yes or no]: ')
    	    if len(r)==0 or (r[0]!='y' and r[0]!='Y'):
	        print('... no target DIR....Aborting!')
	        sys.exit(0)
	    if os.makedirs(targetDir):
	        print('Error creating target DIR')
        else:
            if os.makedirs(targetDir):
	        sys.exit(1)
    targetDir+='/'
else: 
    options.targetDir=''
    targetDir=options.targetDir

# find index set based on the given "box":
def boundingindex(dmin,dint,length,boundary0,boundary1):
  inx0=max(int(ceil((boundary0-dmin)/dint)),0)
  inx1=min(int(floor((boundary1-dmin)/dint)),length-1)
  return [inx0,inx1]

[i0,i1]=boundingindex(lon0,dint,nlon,box[0],box[1])
[j0,j1]=boundingindex(lat0,dint,nlat,box[2],box[3])
if i0>i1 or j0>j1:
  sys.exit('No grid point in your domain box.')

# modify the max grid indices, as necessary:
if ig>1:
  i1=max(span(i0,i1,ig))
  j1=max(span(j0,j1,ig))

# modify the finish day, as necessary:
if dday>1:
  maxmjd=max(span(cal2mjd(year0,month0,day0),cal2mjd(year1,month1,day1),dday))
  (year1,month1,day1)=mjd2cal(maxmjd)


# download size information:
if not options.quiet:
	print(' ')
	print('First file: '+ncname(ncBody,year0,yearday(day0,month0,year0)))
	print('Last file:  '+ncname(ncBody,year1,yearday(day1,month1,year1)))
	print('  files obtained at %d-day interval'%(dday))
	print(' ')
	print('Longitude range: %f to %f'%(box[0],box[1]))
	print('Latitude range: %f to %f'%(box[2],box[3]))
	print('  every %d pixel(s) is obtained'%(ig))
	print(' ')
	print('grid dimensions will be ( %d x %d )'%(len(span(i0,i1,ig)),len(span(j0,j1,ig))))
	print(' ')

	r=raw_input('OK to download?  [yes or no]: ')
	if len(r)==0 or (r[0]!='y' and r[0]!='Y'):
	  print('... no download')
	  sys.exit(0)


# form the index set for the command line:
inx=[[0,1,0],[i0,ig,i1],[j0,ig,j1]]
index=''
for i in order:
  index=index+'[%d:%d:%d]'%(inx[i][0],inx[i][1],inx[i][2])

errorList=""
errorCount=0
if options.useLogFile:
	try:
	    log=open(logFile, "ab")
	except:
	    if not options.quiet: print("failed to open logfile "+logFile+" for writing! Aborting!")
            sys.exit(1)
# main loop:
for mjd in span(cal2mjd(year0,month0,day0),cal2mjd(year1,month1,day1),dday):

    (year,month,day)=mjd2cal(mjd)
    yday=yearday(day,month,year)

    cmd=L4URL+pathname(ncHead,ncBody,ncTail,year,yday)
    cmd=cmd+'.nc?'
    if options.includeSST:
      cmd=cmd+'analysed_sst'+index+','
    if options.includeError:
      cmd=cmd+'analysis_error'+index+','
    if options.includeLandMask:
      cmd=cmd+'mask'+index+','
    if options.includeIce:
      cmd=cmd+'sea_ice_fraction'+index+','
    cmd=cmd[0:(len(cmd)-1)]  # remove the extra "," at the end.

    if options.useWget:
	if not options.quiet: cmd='wget -c "'+cmd+'" -O '+targetDir+ncname(ncBody,year,yday)
	else: cmd='wget -q -c "'+cmd+'" -O '+targetDir+ncname(ncBody,year,yday)
    else:
        if not options.quiet: cmd='curl -f -g "'+cmd+'" -o '+targetDir+ncname(ncBody,year,yday)
	else: cmd='curl -silent -f -g "'+cmd+'" -o '+targetDir+ncname(ncBody,year,yday)

    if options.testing:  # just test command:
	if not options.quiet:  print(cmd)
    else:  # run opendap
        exitcode=os.system( cmd )
	if exitcode:
	    errorList+=ncname(ncBody,year,yday)+"\n"
	    errorCount+=1
	    if options.useWget: # remove the created output file, if wget was used (curl suppresses already by invoking -f)
                os.system( 'rm '+targetDir+ncname(ncBody,year,yday) )
	if exitcode==2: #if ctrl-c was pressed during execution, stop script!
	    if options.useLogFile: 
		log.write(strftime("%Y-%m-%d %H:%M:%S")+ "\n" + str(errorCount) + ' files failed to download: \n' +errorList+'\n\n')
	        log.close()
	    if not options.quiet: print('\n\n' + str(errorCount) + ' files failed to download: \n' +errorList)
	    exit()
if options.useLogFile:
    log.write(strftime("%Y-%m-%d %H:%M:%S")+ "\n" + str(errorCount) + ' files failed to download: \n' +errorList+ '\n\n')
    log.close()
if not options.quiet:
    if errorList: print('\n\n' + str(errorCount)+ ' files failed to download: \n' +errorList)
