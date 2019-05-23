#! /usr/bin/env python
#
import sys,os
import time
from datetime import datetime, date, timedelta
from math import floor,ceil
from optparse import OptionParser
import subprocess

import numpy as np

###############
# subroutines #
###############
def diffdates(d1, d2):
    #2007-12-31T08:50:07.000Z
    #Date format: %Y-%m-%dT%H:%M:%S:%Z
    #return (time.mktime(time.strptime(d2,"%Y-%m-%dT%H:%M:%S.%fZ")) -
    #           time.mktime(time.strptime(d1, "%Y-%m-%dT%H:%M:%S.%fZ")))
    td=datetime.strptime(d2,"%Y-%m-%dT%H:%M:%S.%fZ")-datetime.strptime(d1,"%Y-%m-%dT%H:%M:%S.%fZ")
    return int(round(td.total_seconds()))

def standalone_main():

    filename = "T2017001.L3m_DAY_SST4_sst4_4km.nc"
    fcmd = "ncks -M -m "+filename+" | grep -E 'time_coverage_end' | cut -f 11 -d ' '"
    date_str = os.popen(fcmd).readlines()
    p = subprocess.Popen(fcmd, stdout=subprocess.PIPE, shell=True)
    (date_str, err) = p.communicate()
    adate_str = date_str.rstrip()
    print adate_str
    bdate_str = "1981-01-01T00:00:00.000Z"
    adiff = diffdates(bdate_str, adate_str)
    acmd = "ncap2 -O -s 'time="+str(int(adiff)) + "' "+filename+" "+filename
    os.system(acmd)
    os.system("ncatted -O -a long_name,time,c,c,'reference time of sst field' "+filename)
    os.system("ncatted -O -a axis,time,c,c,'T' "+filename)
    os.system("ncatted -O -a units,time,c,c,'seconds since 1981-01-01 00:00:00 UTC' "+filename)
    os.system("ncatted -O -a comment,time,c,c,'Nominal time of analyzed fields' "+filename)

if __name__ == "__main__":
        standalone_main()