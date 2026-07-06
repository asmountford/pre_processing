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
        source_thetao = xr.open_dataset(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/thetao/ready_19{year:02}{month:02}_thetao.nc').rename({'lev':'deptht'})
        source_so = xr.open_dataset(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/so/ready_19{year:02}{month:02}_so.nc').rename({'lev':'deptht'})
        nemo_mask = xr.open_dataset('/home/users/asmou/nemo_files/mesh_mask.nc').rename({'nav_lev':'deptht'})

        source_thetao    = source_thetao.isel(x=slice(0,1440))
        source_so        = source_so.isel(x=slice(0,1440))
        source_thetao    = source_thetao.isel(y=slice(451,452))
        source_so        = source_so.isel(y=slice(451,452))
        nemo_mask        = nemo_mask.isel(y=slice(451,452)) ### for bdyT and bdyU files

        source_thetao = source_thetao.regrid.linear(nemo_mask)
        source_so = source_so.regrid.linear(nemo_mask)

        source_thetao.thetao[:,0,:,:] = source_thetao.thetao[:,1,:,:].copy()
        source_so.so[:,0,:,:] = source_so.so[:,1,:,:].copy()

        ##### TEOS10 CONVERSION
        AbsSal = gsw.SA_from_SP(source_so.so,source_so.deptht,source_so.nav_lon,source_so.nav_lat)
        ConsTemp = gsw.CT_from_pt(AbsSal.values,source_thetao.thetao)
        source_so = source_so.assign(AbsSal=AbsSal)
        source_thetao = source_thetao.assign(ConsTemp=ConsTemp)

        source_so = source_so.AbsSal*nemo_mask.tmask
        source_thetao = source_thetao.ConsTemp*nemo_mask.tmask

        source_thetao.to_netcdf(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/thetao/19{year:02}{month:02}_thetao.nc')
        source_so.to_netcdf(f'/gws/nopw/j04/raspwork/bdy_hist/r1i1p1f1/so/19{year:02}{month:02}_so.nc')
