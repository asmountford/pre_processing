#!/usr/bin/env python3

import subprocess

for year in range (0,10):
    for month in range(1,13):
        print(year,month)
        subprocess.call(f"ncwa -a time,time_counter thetao/19{year:02}{month:02}_thetao.nc thetao/19{year:02}{month:02}_thetao_time.nc",shell=True) 
        subprocess.call(f"ncwa -a time,time_counter so/19{year:02}{month:02}_so.nc so/19{year:02}{month:02}_so_time.nc",shell=True) 
        subprocess.call(f"ncwa -a time,time_counter uo/19{year:02}{month:02}_gridU.nc uo/19{year:02}{month:02}_gridU_time.nc",shell=True)
        subprocess.call(f"ncwa -a time,time_counter vo/19{year:02}{month:02}_gridV.nc vo/19{year:02}{month:02}_gridV_time.nc",shell=True)
        
        subprocess.call(f"ncrename -v __xarray_dataarray_variable__,thetao -O thetao/19{year:02}{month:02}_thetao_time.nc thetao/19{year:02}{month:02}_thetao_time.nc",shell=True)
        subprocess.call(f"ncrename -v __xarray_dataarray_variable__,so -O so/19{year:02}{month:02}_so_time.nc so/19{year:02}{month:02}_so_time.nc",shell=True)
        subprocess.call(f"ncrename -v __xarray_dataarray_variable__,uo -O uo/19{year:02}{month:02}_gridU_time.nc uo/19{year:02}{month:02}_gridU_time.nc",shell=True)
        subprocess.call(f"ncrename -v __xarray_dataarray_variable__,vo -O vo/19{year:02}{month:02}_gridV_time.nc vo/19{year:02}{month:02}_gridV_time.nc",shell=True)

        subprocess.call(f"cdo setctomiss,0 thetao/19{year:02}{month:02}_thetao_time.nc thetao/y19{year:02}{month:02}_Thetao.nc",shell=True) 
        subprocess.call(f"cdo setctomiss,0 so/19{year:02}{month:02}_so_time.nc so/y19{year:02}{month:02}_So.nc",shell=True) 
        subprocess.call(f"cdo setctomiss,0 uo/19{year:02}{month:02}_gridU_time.nc uo/y19{year:02}{month:02}_grid-U.nc",shell=True)
        subprocess.call(f"cdo setctomiss,0 vo/19{year:02}{month:02}_gridV_time.nc vo/y19{year:02}{month:02}_grid-V.nc",shell=True)

        subprocess.call(f"cdo setmisstoc,9999 thetao/y19{year:02}{month:02}_Thetao.nc thetao/transfer/thetao_y19{year:02}m{month:02}.nc",shell=True) 
        subprocess.call(f"cdo setmisstoc,9999 so/y19{year:02}{month:02}_So.nc so/transfer/so_y19{year:02}m{month:02}.nc",shell=True) 
        subprocess.call(f"cdo setmisstoc,9999 uo/y19{year:02}{month:02}_grid-U.nc uo/transfer/gridU_y19{year:02}m{month:02}.nc",shell=True)
        subprocess.call(f"cdo setmisstoc,9999 vo/y19{year:02}{month:02}_grid-V.nc vo/transfer/gridV_y19{year:02}m{month:02}.nc",shell=True)

