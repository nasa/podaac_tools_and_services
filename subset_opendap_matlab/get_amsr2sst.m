function [data,geo] = get_amsr2sst(dataurl,latmin,latmax,lonmin,lonmax,varname)
% Read AMSR2 data from PO-DAAC opendap
%
% See get_amsr2sst_filelist.m which returns information required to
% build a set of data urls for any given day
%
%
% Optional inputs:
%     POLYBOX:  Matrix with columns of lon,lat defining a box
%     in which to extrct the AMSR2 data (e.g. created with
%     ginput)
%     VARNAME variable to extract - default sea_surface_temperature
%
% John Wilkin
% Feb 13, 2015

if nargin < 6
  varname = 'sea_surface_temperature';
end

%lon = nc_varget(dataurl,'lon');
lon = ncread(dataurl,'lon');
lat = ncread(dataurl,'lat');
if nargin > 4
  in = find((lon >= lonmin & lon <= lonmax) & (lat >= latmin & lat <= latmax));
else
  in = ~isnan(lon);
end

if ~isempty(in)
  lon = lon(in);
  lat = lat(in);
  data = ncread(dataurl,varname);
  data = data(in);
  time = ncread(dataurl,'time')/86400+datenum(1981,1,1);
  geo.lon = lon;
  geo.lat = lat;
  geo.time = time;
else
  warning('No data found in the granule')
  data = [];
  geo = [];
end