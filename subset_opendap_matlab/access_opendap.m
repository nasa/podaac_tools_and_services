clear
format compact
format long

%*** Input Parametr

shortName='AMSR2-REMSS-L2P-v7.2';

%Read/Write data****************************************************************
datanum = datenum(2014,10,1);
[opendap,flist] = get_amsr2sst_filelist(datanum, shortName, 'final');
[nfile lz]=size(flist);
for i=1:nfile
 [data,geo] = get_amsr2sst([opendap flist(i,:)], -20, 20, -60, 60);
 if (length(data) > 1)
   disp(sprintf('\n*** Writing File %s ***', flist(i,:)));
   nccreate( flist(i,:), 'sea_surface_temperature', 'Dimensions',{'r' length(data)}, 'Datatype','double');
   ncwrite ( flist(i,:), 'sea_surface_temperature', data); 
   nccreate ( flist(i,:), 'time'); 
   ncwrite ( flist(i,:), 'time', geo.time); 
   nccreate ( flist(i,:), 'lon', 'Dimensions',{'r' length(geo.lon)}, 'Datatype','double'); 
   ncwrite ( flist(i,:), 'lon', geo.lon); 
   nccreate ( flist(i,:), 'lat', 'Dimensions',{'r' length(geo.lat)}, 'Datatype','double'); 
   ncwrite ( flist(i,:), 'lat', geo.lat); 
 end
end
%End****************************************************************

