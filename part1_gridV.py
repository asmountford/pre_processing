#!/usr/bin/env python3

import subprocess

for year in range (80,90):
    for month in range(1,13):
        print(month)
        #subprocess.call(f"cdo setctomiss,0 thetao/r1i1p1f1_thetao_y19{year:02}_m{month:02}.nc thetao/tmp_19{year:02}{month:02}_thetao.nc",shell=True) 
        #subprocess.call(f"cdo setctomiss,0 so/r1i1p1f1_so_y19{year:02}_m{month:02}.nc so/tmp_19{year:02}{month:02}_so.nc",shell=True) 
        #subprocess.call(f"cdo remapnn,MJ_eORCA.nc thetao/tmp_19{year:02}{month:02}_thetao.nc thetao/remapnn_19{year:02}{month:02}_thetao.nc",shell=True)
        #subprocess.call(f"cdo remapnn,MJ_eORCA.nc so/tmp_19{year:02}{month:02}_so.nc so/remapnn_19{year:02}{month:02}_so.nc",shell=True)
        #subprocess.call(f"cdo setmisstonn thetao/remapnn_19{year:02}{month:02}_thetao.nc thetao/ready_19{year:02}{month:02}_thetao.nc",shell=True)
        #subprocess.call(f"cdo setmisstonn so/remapnn_19{year:02}{month:02}_so.nc so/ready_19{year:02}{month:02}_so.nc",shell=True)

        #subprocess.call(f"cdo setctomiss,0 ./uo/r1i1p1f1_uo_y19{year:02}{month:02}.nc ./uo/r1i1p1f1_uo_y19{year:02}_m{month:02}.nc",shell=True) 
        #subprocess.call(f"cdo selvar,uo ./uo/r1i1p1f1_uo_y19{year:02}_m{month:02}.nc ./uo/tmp_19{year:02}{month:02}_gridU.nc",shell=True)
        #subprocess.call(f"cdo remapnn,MJ_eORCA.nc ./uo/tmp_19{year:02}{month:02}_gridU.nc ./uo/remapnn_19{year:02}{month:02}_gridU.nc",shell=True)
        #subprocess.call(f"cdo setmisstonn ./uo/remapnn_19{year:02}{month:02}_gridU.nc ./uo/ready_19{year:02}{month:02}_gridU.nc",shell=True)

        subprocess.call(f"cdo setctomiss,0 vo/r1i1p1f1_vo_y19{year:02}_m{month:02}.nc vo/tmp_vo_y19{year:02}_m{month:02}.nc",shell=True) 
        subprocess.call(f"cdo remapnn,MJ_eORCA.nc vo/tmp_vo_y19{year:02}_m{month:02}.nc vo/remapnn_19{year:02}{month:02}_gridV.nc",shell=True)
        subprocess.call(f"cdo setmisstonn vo/remapnn_19{year:02}{month:02}_gridV.nc vo/ready_19{year:02}{month:02}_gridV.nc",shell=True)
