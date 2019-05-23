;******************************************************************************
; Filename:   ascat_l2_main.pro
; --------
; Program Usage:
;
;   To run this program, use the following command:
;
;   IDL> ascat_l2_main
; --------
; Program Description:
;  
;   Calls the "ascat_l2_read.pro" procedure to read ASCAT L2 data.
;
;   1. ascat_l2_main: the main procedure.
;
; --------
; Glossary of parameters passed from main program to "ascat_l2_read.pro":
;
;   1. "workable" - contains the unzipped filename to be read.
;
; --------
; Glossary of parameters passed from "ascat_l2_read.pro" to main program:
;
;   1. "fillval" - missing value array or each geo-referenced parameter.
;   2. "valid_min" - absolute minimum value with respect to current NetCDF file.
;   3. "valid_max" - absolute maximum value with respect to current NetCDF file.
;   4. "time" - seconds elapsed since 1 January 1900 0000 UTC.
;   5. "lat" - degrees of latitude for each wind vector cell.
;   6. "lon" - degrees of longitude for each wind vector cell.
;   7. "model_spd" - ECMWF wind speed (m/s) used for ambiguity removal.
;   8. "model_dir" - ECMWF wind direction (degrees) used for ambiguity removal.
;   9. "ice_prob" - probability (from 0 to 1) of sea ice or continental ice
;		present in a wind vector cell.
;   10. "ice_age" - provides equivalent instrument backscatter power (dB) at 40 
;		degrees incidence angle to determine the geophysical condition
;		of ice in a wind vector cell.
;   11. "wvc_quality" - provides quality bit flag values relating to the
;		measurement quality in each wind vector cell.
;   12. "wvc_quality_struc" - provides bit flag interpretation for each
;		bit flag provided in "wvc_quality. Values are either 0 or 1,
;		where 1 indicates a particular bit flag has been activated.
;   13. "wspd" - the geophysically derived scatterometer wind speed (m/s)
;		retrieval.
;   14. "dir" - the retrieved scatterometer wind direction (degrees)
;   15. "bs_dist" - the normalized distance between observed vs. retrieved
;   16. "timestruct" - an arrayed structure of the complete UTC time record:
;	{ month, day, year, hour, minute, second }
;   17. "nwvcs" - number of subsetted wind vector cell columns
;   18. "nrows" - number of subsetted wind vector cell rows
; --------
; Program Language: Interactive Data Language (IDL)
; --------
; Program Author:	David F. Moroni
;==================================================================
;   Copyright (c) 2011, California Institute of Technology
;==================================================================		
; Notes:
;
; 1. The directory on your local system which contains the source NetCDF file
;    must be correctly applied using the variable 'indir'.
;
; 2. All parameters passed into the main program have been properly scaled using
;    the applicable scale factor as supplied in the NetCDF files.
;
; 3. This code was developed and tested using IDL Version 6.4 (c) 2007, 
;    ITT Visual Information Solutions.
;
; 4. This code is freely modifiable for customized and unlimited use.
;
; 5. Please direct all inquiries regarding this code to:
;    podaac@podaac.jpl.nasa.gov.
; --------
; Revisions: 		Date		Author		Description
;		    1/18/2010	     D. Moroni	        Created.
;
;		    3/8/2010	     D. Moroni	        a) Bug fixes applied to
;							"ascat_l2_read.pro".
;							b) Added new time
;							structure containing 
;							the converted time 
;							fields. 
;							c) Added the subsetted 
;							swath wind vector cell 
;							row and	column 
;							dimensions. 
;							d) Added new note to 
;							clarify the scaling of 
;							parameters. 
;							e) Added glossary of I/O 
;							parameters.
;		    3/16/2010	     D. Moroni	        f) Added 'wvc_quality'
;							structure of
;							set vs. unset bits.
;		    5/19/2011        D. Moroni          g) Added capability to
;							read and recognize
;							the Level 2 Coastal
;							Dataset.		
;******************************************************************************

@ascat_l2_read.pro

pro ascat_l2_main

;***** Change data directory to suit your local system
 in_dir = '/home/your_directory/data_directory/'
 
;Select Coastal, 12.5-km or 25-km product
 print,'Please enter your choice of Level 2 ASCAT Data as:'
 print,'1 = Coastal 12.5-km Dataset'
 print,'2 = Standard 12.5-km Dataset'
 print,'3 = Standard 25-km Dataset'
 read,res,prompt='Enter your choice here: '
 res_dir = ['','coastal','12km','25km'] 
 data_dir = in_dir+res_dir[res]
 
 print,'Is your file GZIPPED or UNZIPPED?'
 read,gzflag,prompt='Enter ''1'' for GZIPPED or ''2'' for UNZIPPED:'
 gzstr = ['','.gz','']
 
 filename=dialog_pickfile(filter='ascat_*'+gzstr, PATH=data_dir, /READ)
 
 print,'You have just selected: ',filename
 
 charsize = STRLEN(filename)
 
 IF (gzflag EQ 1) THEN BEGIN
  filetrim = STRMID(filename,charsize-62)
  trimsize = STRLEN(filetrim) - 3
  workable = STRMID(filetrim,0,trimsize)
  SPAWN,'gunzip -c '+filename+' > '+workable
 ENDIF ELSE BEGIN
  filetrim = STRMID(filename,charsize-59)
  workable = filetrim
  SPAWN,'cp '+filename+' ./'
 ENDELSE
 
; Call L2 Read Subroutine
 ascat_l2_read,workable,fillval,valid_min,valid_max,time,lat,lon,model_spd, $
 	model_dir,ice_prob,ice_age,wvc_quality, wvc_quality_struc,$
	wspd,dir,bs_dist, timestruc, nwvcs, nrows
	
; Remove the NetCDF File 
 SPAWN,'rm '+workable	
 
stop			
end
