#!/usr/bin/env python3

import xarray as xr
import numpy as np
import dask.distributed
import os
import tqdm
import cftime
import pandas
import xarray_regrid
import numpy.ma as ma
import matplotlib.pyplot as plt
import xgcm
import gsw

for year in range (0,10):
    print(year)
    for month in range (1,13):
        print(month)
        source_var = xr.open_dataset(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/uo/ready_19{year:02}{month:02}_gridU.nc').rename({'lev':'depthu'})
        nemo_mask = xr.open_dataset('/home/users/asmou/nemo_files/mesh_mask.nc').rename({'nav_lev':'depthu'})

        source_var      = source_var.isel(x=slice(0,1440))
        source_var      = source_var.isel(y=slice(451,452))
        nemo_mask        = nemo_mask.isel(y=slice(451,452)) ### for bdyT and bdyU files

        source_var = source_var.regrid.linear(nemo_mask)
        source_var.uo[:,0,:,:] = source_var.uo[:,1,:,:].copy()
        source_var = source_var.uo*nemo_mask.umask

        source_var.to_netcdf(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/uo/19{year:02}{month:02}_gridU.nc')
