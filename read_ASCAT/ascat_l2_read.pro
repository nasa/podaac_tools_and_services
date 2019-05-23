;******************************************************************************
; Filename:   ascat_l2_read.pro
; --------
; Program Usage:
;
;   This procedure/subroutine is called by "ascat_l2_main.pro"
;
; --------
; Program Description:
;  
;   Reads Level 2 ASCAT 25 km and 12.5 km NetCDF version 4 data files produced 
;   by the Ocean and Sea Ice Satellite Application Facilities (www.osi-saf.org) 
;   through the European Organization for the Exploitation of Meteorological 
;   Satellites (www.eumetsat.int). The Level 2 ASCAT granules are converted from
;   the native BUFR format and repackaged into single-orbit granules in NetCDF 
;   version 4 format and provided to PO.DAAC by the Royal Netherlands 
;   Meteorolgical Institute (www.knmi.nl).
;
;   1. ncdf_open: a function to enable read-access a NetCDF file.
;
;   2. ncdf_varid: a function to return the variable id of a NetCDF file.
;
;   3. ncdf_varget: a procedure to retrieve values from a variable from a
;      NetCDF file.
;
;   4. ncdf_attget: a procedure to retrieve the value of an attribute from a
;      NetCDF file.
;
;   5. ascat_l2_read: the running procedure.
; --------
; Glossary of parameters passed from main program to "ascat_l2_read.pro":
;
;   1. "infile" - contains the unzipped filename to be read.
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
;   Copyright (c) 2015, California Institute of Technology
;==================================================================		
; Notes:
;
; 1. This code was developed and tested using IDL Version 6.4 (c) 2007, 
;    ITT Visual Information Solutions.
;
; 2. This code is freely modifiable for customized and unlimited use.
;
; 3. Please direct all inquiries regarding this code to:
;    podaac@podaac.jpl.nasa.gov.
; --------
; Revisions: 		Date		Author		Description
;		    1/18/2010	     D. Moroni	        Created.
;
;		    3/8/2010	     D. Moroni		a) Bug fixes to NetCDF
;							array offsets, time
;							parameter passing and
;							parameter scaling.
;							b) Cleaned up user
;							interface.
;							c) Added new time
;							structure containing 
;							the converted time 
;							fields. 
;							d) Added the subsetted 
;							swath wind vector cell 
;							row and column 
;							dimensions to the list 
;							of procedure arguments. 
;							e) Adjusted scaling of 
;							parameters to be 
;							all-inclusive. 
;							f) Added glossary of I/O
;							parameters.
;
;		    3/16/2010	     D. Moroni	        a) Added bit flag
;							interpretter for 
;							'wvc_quality' flag.
;							b) Added structure to
;							store arrays of 
;							set vs. unset bits
;							referenced to wvc
;							quality flag.	
;
;		    4/2/2015	     D. Moroni	        a) Bug fix, corrected name of 
;							data array called 'time',
;							previously called 'time_ss',
;							which is passed onto the main
;							program called
;							'ascat_l2_main.pro'.
;******************************************************************************

pro ascat_l2_read,infile,fillval,valid_min,valid_max,time,lat,lon, $
	model_spd, model_dir, ice_prob, ice_age, wvc_quality, $
	wvc_quality_struc, wspd, dir, bs_dist, timestruc, sum_wvcs, sum_rows
 
; Open the source NetCDF File
 ncid = NCDF_OPEN(infile, /NOWRITE)
 
; Obtain Dimensions
 NCDF_DIMINQ,ncid,0,numrows,nrows		;Along-track data rows
 NCDF_DIMINQ,ncid,1,numcells,ncells		;Cross-track data cells

 rows_limit = STRING(nrows-1, FORMAT='(I4)')
 cells_limit = STRING(ncells-1, FORMAT='(I2)')

; Select wind vector cell rows to be written to the screen
 print,'Valid range of Along-Track wind vector cell rows is 0 to '+rows_limit
 read,'Enter the first wind vector cell row number to be read: ',irow0
 read,'Enter the final wind vector cell row number to be read: ',irow1 
 IF (irow0 GT irow1) THEN BEGIN
   itmp=irow0
   irow0=irow1
   irow1=itmp
 ENDIF
 print,'Valid range of Cross-Track wind vector cells is 0 to ',+cells_limit 
 read,'Enter the first cross-track wind vector cell to be read: ',iwvc0
 read,'Enter the final cross-track wind vector cell to be read: ',iwvc1
 IF (iwvc0 GT iwvc1) THEN BEGIN
   itmp=iwvc0
   iwvc0=iwvc1
   iwvc1=itmp
 ENDIF
 
;Create NetCDF Counts and Offsets based on User Input
 
 sum_rows = (irow1-irow0)+1
 sum_wvcs = (iwvc1-iwvc0)+1
 count=[sum_wvcs,sum_rows]
 offset=[iwvc0,irow0]
 
; Create string array to store NetCDF variable names
 var_name = STRARR(12)
 var_name[0]  = "time"
 var_name[1]  = "lat"
 var_name[2]  = "lon"
 var_name[3]  = "wvc_index"
 var_name[4]  = "model_speed"
 var_name[5]  = "model_dir"
 var_name[6]  = "ice_prob"
 var_name[7]  = "ice_age"
 var_name[8]  = "wvc_quality_flag"
 var_name[9]  = "wind_speed"
 var_name[10] = "wind_dir"
 var_name[11] = "bs_distance"                           

; Identify the variables   
 time_id = NCDF_VARID(ncid, var_name[0])
 lat_id = NCDF_VARID(ncid, var_name[1])
 lon_id = NCDF_VARID(ncid, var_name[2])
 wvc_index_id = NCDF_VARID(ncid, var_name[3])
 model_spd_id = NCDF_VARID(ncid, var_name[4])
 model_dir_id = NCDF_VARID(ncid, var_name[5])
 ice_prob_id = NCDF_VARID(ncid, var_name[6])
 ice_age_id = NCDF_VARID(ncid, var_name[7])
 wvc_quality_id = NCDF_VARID(ncid, var_name[8])
 wspd_id = NCDF_VARID(ncid, var_name[9])
 dir_id  = NCDF_VARID(ncid, var_name[10])
 bs_dist_id = NCDF_VARID(ncid, var_name[11])

; Read and store the data from each variable
 NCDF_VARGET, ncid, time_id, time,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, lat_id, lat,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, lon_id, lon,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, wvc_index_id, wvc_index,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, model_spd_id, model_spd,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, model_dir_id, model_dir,COUNT=count,OFFSET=offset      
 NCDF_VARGET, ncid, ice_prob_id, ice_prob,COUNT=count,OFFSET=offset      
 NCDF_VARGET, ncid, ice_age_id, ice_age,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, wvc_quality_id, wvc_quality,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, wspd_id, wspd,COUNT=count,OFFSET=offset
 NCDF_VARGET, ncid, dir_id, dir,COUNT=count,OFFSET=offset            
 NCDF_VARGET, ncid, bs_dist_id, bs_dist,COUNT=count,OFFSET=offset

 fillval = DBLARR(12)
 valid_min = DBLARR(12)
 valid_max = DBLARR(12)
 scale_factor = DBLARR(12)

; Obtain the Scale Factor for each variable 
 scale_factor[0] = 1.0
 NCDF_ATTGET, ncid, lat_id, "scale_factor", val
 scale_factor[1] = val
 NCDF_ATTGET, ncid, lon_id, "scale_factor", val
 scale_factor[2] = val
 scale_factor[3] = 1.0
 NCDF_ATTGET, ncid, model_spd_id, "scale_factor", val 
 scale_factor[4] = val
 NCDF_ATTGET, ncid, model_dir_id, "scale_factor", val
 scale_factor[5] = val 
 NCDF_ATTGET, ncid, ice_prob_id, "scale_factor", val
 scale_factor[6] = val
 NCDF_ATTGET, ncid, ice_age_id, "scale_factor", val
 scale_factor[7] = val
 scale_factor[8] = 1.0
 NCDF_ATTGET, ncid, wspd_id, "scale_factor", val
 scale_factor[9] = val
 NCDF_ATTGET, ncid, dir_id, "scale_factor", val
 scale_factor[10] = val                           
 NCDF_ATTGET, ncid, bs_dist_id, "scale_factor", val
 scale_factor[11] = val    

; Obtain the Fill (i.e., Missing) value for each variable   
; Apply Scale Factor Corrections   
 NCDF_ATTGET, ncid, time_id, "_FillValue", val
 fillval[0] = DOUBLE(val)*scale_factor[0]
 NCDF_ATTGET, ncid, lat_id, "_FillValue", val
 fillval[1] = DOUBLE(val)*scale_factor[1]
 NCDF_ATTGET, ncid, lon_id, "_FillValue", val
 fillval[2] = DOUBLE(val)*scale_factor[2]
 NCDF_ATTGET, ncid, wvc_index_id, "_FillValue", val
 fillval[3] = DOUBLE(val)*scale_factor[3]
 NCDF_ATTGET, ncid, model_spd_id, "_FillValue", val
 fillval[4] = DOUBLE(val)*scale_factor[4]
 NCDF_ATTGET, ncid, model_dir_id, "_FillValue", val
 fillval[5] = DOUBLE(val)*scale_factor[5]
 NCDF_ATTGET, ncid, ice_prob_id, "_FillValue", val
 fillval[6] = DOUBLE(val)*scale_factor[6]
 NCDF_ATTGET, ncid, ice_age_id, "_FillValue", val
 fillval[7] = DOUBLE(val)*scale_factor[7]
 NCDF_ATTGET, ncid, wvc_quality_id, "_FillValue", val
 fillval[8] = val
 NCDF_ATTGET, ncid, wspd_id, "_FillValue", val
 fillval[9] = DOUBLE(val)*scale_factor[9]
 NCDF_ATTGET, ncid, dir_id, "_FillValue", val
 fillval[10] = DOUBLE(val)*scale_factor[10]             
 NCDF_ATTGET, ncid, bs_dist_id, "_FillValue", val 
 fillval[11] = DOUBLE(val)*scale_factor[11]
 
; Obtain the Valid Minimum Value for each variable
; Apply Scale Factor Corrections 
 NCDF_ATTGET, ncid, time_id, "valid_min", val
 valid_min[0] = DOUBLE(val)*scale_factor[0]
 NCDF_ATTGET, ncid, lat_id, "valid_min", val
 valid_min[1] = DOUBLE(val)*scale_factor[1]
 NCDF_ATTGET, ncid, lon_id, "valid_min", val
 valid_min[2] = DOUBLE(val)*scale_factor[2]
 NCDF_ATTGET, ncid, wvc_index_id, "valid_min", val
 valid_min[3] = DOUBLE(val)*scale_factor[3]
 NCDF_ATTGET, ncid, model_spd_id, "valid_min", val
 valid_min[4] = DOUBLE(val)*scale_factor[4]
 NCDF_ATTGET, ncid, model_dir_id, "valid_min", val
 valid_min[5] = DOUBLE(val)*scale_factor[5]
 NCDF_ATTGET, ncid, ice_prob_id, "valid_min", val
 valid_min[6] = DOUBLE(val)*scale_factor[6]
 NCDF_ATTGET, ncid, ice_age_id, "valid_min", val
 valid_min[7] = DOUBLE(val)*scale_factor[7]
 NCDF_ATTGET, ncid, wvc_quality_id, "valid_min", val
 valid_min[8] = val
 NCDF_ATTGET, ncid, wspd_id, "valid_min", val
 valid_min[9] = DOUBLE(val)*scale_factor[9]
 NCDF_ATTGET, ncid, dir_id, "valid_min", val
 valid_min[10] = DOUBLE(val)*scale_factor[10]                          
 NCDF_ATTGET, ncid, bs_dist_id, "valid_min", val
 valid_min[11] = DOUBLE(val)*scale_factor[11]

; Obtain the Valid Maximum Value for each variable 
; Apply Scale Factor Corrections where applicable
 NCDF_ATTGET, ncid, time_id, "valid_max", val
 valid_max[0] = DOUBLE(val)*scale_factor[0]
 NCDF_ATTGET, ncid, lat_id, "valid_max", val
 valid_max[1] = DOUBLE(val)*scale_factor[1]
 NCDF_ATTGET, ncid, lon_id, "valid_max", val
 valid_max[2] = DOUBLE(val)*scale_factor[2]
 NCDF_ATTGET, ncid, wvc_index_id, "valid_max", val
 valid_max[3] = DOUBLE(val)*scale_factor[3]
 NCDF_ATTGET, ncid, model_spd_id, "valid_max", val
 valid_max[4] = DOUBLE(val)*scale_factor[4]
 NCDF_ATTGET, ncid, model_dir_id, "valid_max", val
 valid_max[5] = DOUBLE(val)*scale_factor[5]
 NCDF_ATTGET, ncid, ice_prob_id, "valid_max", val
 valid_max[6] = DOUBLE(val)*scale_factor[6]
 NCDF_ATTGET, ncid, ice_age_id, "valid_max", val
 valid_max[7] = DOUBLE(val)*scale_factor[7]
 NCDF_ATTGET, ncid, wvc_quality_id, "valid_max", val
 valid_max[8] = val
 NCDF_ATTGET, ncid, wspd_id, "valid_max", val
 valid_max[9] = DOUBLE(val)*scale_factor[9]
 NCDF_ATTGET, ncid, dir_id, "valid_max", val
 valid_max[10] = DOUBLE(val)*scale_factor[10]                          
 NCDF_ATTGET, ncid, bs_dist_id, "valid_max", val
 valid_max[11] = DOUBLE(val)*scale_factor[11]

; Close the NetCDF File 
 ncdf_close, ncid

; Create structure to store indices of set bit flags
 wvc_quality_struc = {wvc_quality_bit_structure,$
 	excess_dist_to_gmf:0S, $
 	redundant_data:0S, $
 	no_met_background:0S, $
	rain_detected:0S, $
	rain_flag_not_usable:0S, $
	wspd_lte_3:0S, $
	wspd_gt_30:0S, $
	no_wind_inversion:0S, $
	ice:0S, $
	land:0S, $
	var_qc_fails:0S, $
	knmi_qc_fails:0S, $
	prod_monit_flag:0S, $
	no_prod_monit:0S, $
	excess_beam_noise:0S, $
	poor_azimuth_diversity:0S, $
	not_enough_good_sigma0:0S }

; Transform structure into an array of structures
  wvc_quality_struc = replicate(wvc_quality_struc,sum_wvcs,sum_rows)

; Convert Seconds to GMT Time of Contemporaneous Day
 day_secs = 3600.
 j_day_start = julday(1,1,1990,0,0,0)
 n_times = SIZE(time, /N_ELEMENTS)
; Create a structure to store time parameters 
 timestruc = {mo:0S,day:0S,year:0S,hh:0S,mm:0S,ss:0S}
 timestruc = replicate(timestruc,sum_wvcs,sum_rows)
 FOR t=0L, n_times-1L DO BEGIN
  time_a = DOUBLE(time[t])/(DOUBLE(day_secs)*DOUBLE(24.))
  new_j_day = j_day_start+time_a
  caldat,new_j_day,mo,day,year,hh,mm,ss
  timestruc[t].mo = mo		;Month
  timestruc[t].day = day	;Day of Month
  timestruc[t].year = year	;Year
  timestruc[t].hh = hh		;Hour of day
  timestruc[t].mm = mm		;Minute of hour
  timestruc[t].ss = ss		;Seconds of minute
  
; Determine number of wvc_quality bits which have been set for each wvc  
  n_bits_set = bit_population(wvc_quality[t])

; If there are wvc quality issues, then proceed  
  IF n_bits_set GT 0 AND wvc_quality[t] NE fillval[8] THEN BEGIN
   bitarr = INTARR(n_bits_set)
   bitval = LONARR(n_bits_set)
   first_bit = bit_ffs(wvc_quality[t]) - 1

; Store set vs. unset bits into an array of structures  
; Set bits = 1
; Unset bits = 0
   bitsum = 0
   FOR i=0, n_bits_set-1 DO BEGIN
    IF i EQ 0 THEN BEGIN   
     bitarr[i] = first_bit
     bitval[i] = wvc_quality[t]
     wvc_quality_struc[t].(first_bit-6) = 1
    ENDIF ELSE IF i GT 0 THEN BEGIN
     bitval[i] = bitval[i-1] - 2L^bitarr[i-1]
     bitarr[i] = bit_ffs(bitval[i]) - 1
     wvc_quality_struc[t].(bitarr[i]-6) = 1    
    ENDIF
   ENDFOR
  ENDIF
  
 ENDFOR

; Fill in correct missing values into new time structures
 i_bad_time = where(time EQ fillval[0])
 IF i_bad_time NE -1 THEN BEGIN
  FOR s=0, 5 DO timestruc[i_bad_time].(s) = time[i_bad_time]
 ENDIF

; Fill in correct missing values into new wvc_quality structures
 i_miss_quality = where(wvc_quality EQ fillval[8])
 IF i_miss_quality NE -1 THEN BEGIN
  FOR s=0, 16 DO $
  wvc_quality_struc[i_miss_quality].(s) = wvc_quality[i_miss_quality]
 ENDIF
 
; Apply Scale Factor Correction to ALL Geo-referenced Parameters
 lat = FLOAT(lat)*scale_factor[1]
 lon= FLOAT(lon)*scale_factor[2]
 model_spd = FLOAT(model_spd)*scale_factor[4]
 model_dir = FLOAT(model_dir)*scale_factor[5]
 ice_prob = FLOAT(ice_prob)*scale_factor[6]
 ice_age = FLOAT(ice_age)*scale_factor[7]
 wspd = FLOAT(wspd)*scale_factor[9]
 dir = FLOAT(dir)*scale_factor[10]
 bs_dist = FLOAT(bs_dist)*scale_factor[11]
 
end
