#!/usr/bin/env python3

import subprocess

for year in range (0,50):
    for month in range(1,13):
        print(month)
        subprocess.call(f"cdo remapnn,MJ_eORCA.nc zos/r1i1p1f1_zos_y19{year:02}_m{month:02}.nc zos/remapnn_19{year:02}{month:02}_zos.nc",shell=True)
     #  subprocess.call(f"cdo remapnn,MJ_eORCA.nc ice/r1i1p1f1_sithick_y19{year:02}_m{month:02}.nc ice/remapnn_19{year:02}{month:02}_sithick.nc",shell=True)
     #  subprocess.call(f"cdo remapnn,MJ_eORCA.nc ice/r1i1p1f1_sisnthick_y19{year:02}_m{month:02}.nc ice/remapnn_19{year:02}{month:02}_sisnthick.nc",shell=True)
     #  subprocess.call(f"cdo remapnn,MJ_eORCA.nc ice/r1i1p1f1_siconc_y19{year:02}_m{month:02}.nc ice/remapnn_19{year:02}{month:02}_siconc.nc",shell=True)

        subprocess.call(f"ncks -d x,2,1441 -d y,451 zos/remapnn_19{year:02}{month:02}_zos.nc zos/transfer/zos_y19{year:02}m{month:02}.nc",shell=True)
     #  subprocess.call(f"ncks -d x,2,1441 -d y,451 ice/remapnn_19{year:02}{month:02}_sithick.nc ice/transfer/sithick_y19{year:02}m{month:02}.nc",shell=True)
     #  subprocess.call(f"ncks -d x,2,1441 -d y,451 ice/remapnn_19{year:02}{month:02}_sisnthick.nc ice/transfer/sisnthick_y19{year:02}m{month:02}.nc",shell=True)
     #  subprocess.call(f"ncks -d x,2,1441 -d y,451 ice/remapnn_19{year:02}{month:02}_siconc.nc ice/transfer/siconc_y19{year:02}m{month:02}.nc",shell=True)
