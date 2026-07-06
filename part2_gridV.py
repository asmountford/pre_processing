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
        source_var = xr.open_dataset(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/vo/ready_19{year:02}{month:02}_gridV.nc').rename({'lev':'depthv'})
        nemo_mask = xr.open_dataset('/home/users/asmou/nemo_files/mesh_mask.nc').rename({'nav_lev':'depthv'})

        source_var      = source_var.isel(x=slice(0,1440))
        source_var      = source_var.isel(y=slice(451,452))
        nemo_mask       = nemo_mask.isel(y=slice(450,451)) ### need to do this for the bdyV files!

        source_var = source_var.regrid.linear(nemo_mask)
        source_var.vo[:,0,:,:] = source_var.vo[:,1,:,:].copy()
        source_var = source_var.vo*nemo_mask.vmask

        source_var.to_netcdf(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/vo/19{year:02}{month:02}_gridV.nc')
