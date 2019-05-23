The MODIS L3 dataset, such as the MODIS Terra Level 3 SST Mid-IR Daily dataset, has no time variable. Therefore it is impossible to aggregate the data files with time. In this post, we will show you how to create time variable using NCO utility, and how to aggregate the files. In the end, we will put the NCO command into python script.

Let's take MODIS Terra Level 3 SST Mid-IR Daily data file T2017001.L3m_DAY_SST4_sst4_4km.nc on January 1, 2017 as example, and we will extract the global attribute time_coverage_end as the time value and convert it to second since since 1981-01-01 00:00:00.

The time value is 1136116209 after converted to second since 1981-01-01 00:00:00. We will show how to calculate the seconds in the python script later.

Next, we create the time variable and assign the necessary attributes to it.


