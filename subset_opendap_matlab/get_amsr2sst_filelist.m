function [opendap,flist] = get_amsr2sst_filelist(day,shortName, version)
% [opendap,flist] = get_amsr2sst_filelist(day,version)
% Get list of Level-2 pass files (FLIST) for AMSR2 microwave SST data
% and the path to the files in the PO-DAAC opendap catalog (OPENDAP)
%
% The data url for an opendap query is the string [opendap flist(k,:)]
%
% Optional input VERSION ('final' or 'realtime','nearrealtime','nrt')
%
% See also get_amsr2sst.m 
%
% John Wilkin
% Feb 13, 2015

if nargin<2
  version = 'final';
end
switch version
  case 'final'
    grepstr = ' grep FTP | grep v07.2 | cut -c100-180 ';
  case {'realtime','nearrealtime','nrt'}
    grepstr = ' grep FTP | grep rt | cut -c100-177 ';
end

% 
[year,~] = datevec(day);
yday = floor(day-datenum(year,1,1))+1;
startTime = datestr(floor(day),30);
endTime = datestr(1+floor(day),30);

% query the PO-DAAC granule data base for names of the L2 files
query = ['curl "http://podaac.jpl.nasa.gov/ws/search/granule',...
  '/?shortName=' shortName,...
  '&startTime=' startTime,...
  '&endTime=' endTime,...
  '&itemsPerPage=100" | ' grepstr ' | sort'];
[~,flist] = unix(query);

% parse the result of the curl query by finding the file names (which all
% start with the year string)
k = strfind(flist,int2str(year));
if isempty(k)
  disp(['No ' upper(version) ' files found for day ' startTime])
  opendap = [];
  flist = [];
  return
end

% trim off the preamble text not excluded by grep
flist = flist(k(1):end);

% reshape 
N = length(k);
flist = reshape(flist,[length(flist)/N N])';

% remove the trailing linefeed
flist(:,end) = [];

% PO-DAAC acknowledge that for some reason the database gives one file at
% the beginning of the list that belongs in the preceding day -
% remove it. I'm not if this means we miss a pass in the successive days.
flist(1,:) = [];

% String giving the path in the opendap catalog to files for this
% day to be used to build the fulll data url in function get_amsr_sst.m
opendap = ['http://podaac-opendap.jpl.nasa.gov:80/opendap/allData/',...
  'ghrsst/data/GDS2/L2P/AMSR2/REMSS/v7.2/',...
  int2str(year) '/' sprintf('%03d',yday) '/'];