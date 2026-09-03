import xarray as xr
import numpy as np
import xarray_regrid

vas = xr.open_dataset('/home/users/asmou/bias_correct/vas_Amon_UKESM1-2-LL_esm-hist_r1i1p1f1_gn_195001-201412.nc').rename({'lat':'latitude'}).rename({'lon':'longitude'})
uas = xr.open_dataset('/home/users/asmou/bias_correct/uas_Amon_UKESM1-2-LL_esm-hist_r1i1p1f1_gn_195001-201412.nc').rename({'lat':'latitude'}).rename({'lon':'longitude'})
u10 = xr.open_dataset('/home/users/asmou/bias_correct/u10_era5_1979-2014.nc')
v10 = xr.open_dataset('/home/users/asmou/bias_correct/v10_era5_1979-2014.nc')

ukesm_vas_clim = vas.sel(time=slice("1979","2014")).groupby("time.month").mean(dim="time")
ukesm_uas_clim = uas.sel(time=slice("1979","2014")).groupby("time.month").mean(dim="time")

era5_u10_clim = u10.groupby("valid_time.month").mean(dim="valid_time")
era5_v10_clim = v10.groupby("valid_time.month").mean(dim="valid_time")

ukesm_uas_regrid = ukesm_uas_clim.regrid.linear(era5_u10_clim)
ukesm_vas_regrid = ukesm_vas_clim.regrid.linear(era5_u10_clim)

magnitude_ukesm = np.sqrt(ukesm_uas_regrid.uas.isel(month=11)**2 + ukesm_vas_regrid.isel(month=11)**2)
angle_ukesm = np.arctan2(ukesm_vas_regrid.isel(month=11),ukesm_uas_regrid.uas.isel(month=11)) # angle in radians (because arctan2)
magnitude_era5 = np.sqrt(era5_u10_clim.u10.isel(month=11)**2 + era5_v10_clim.v10.isel(month=11)**2)
angle_era5 = np.arctan2(era5_v10_clim.v10.isel(month=11),era5_u10_clim.u10.isel(month=11)) # angle in radians (because arctan2)

tmp = xr.open_dataset('/home/users/asmou/bias_correct/mask2.nc').rename({'lat':'latitude'}).rename({'lon':'longitude'}).rename({'mrro':'mask'}) # using this as a mask as i couldn't find a land/sea mask for era5
era_mask = tmp.regrid.linear(era5_u10_clim)

era_mask['mask'] = era_mask['mask'].where(np.isnan(era_mask['mask']),0).fillna(1)
open_ocean = (era_mask.mask ==1)
land_ice = ~open_ocean

def neighbours (data, missing_val=-9999, use_1d=False):

    # Find the value to the west, east, south, north of every point
    # Just copy the boundaries
    data_w          = np.empty(data.shape)
    data_w[...,1:]  = data[...,:-1]
    data_w[...,0]   = data[...,0]
    data_e          = np.empty(data.shape)
    data_e[...,:-1] = data[...,1:]
    data_e[...,-1]  = data[...,-1]
    if not use_1d:
        data_s            = np.empty(data.shape)
        data_s[...,1:,:]  = data[...,:-1,:]
        data_s[...,0,:]   = data[...,0,:]
        data_n            = np.empty(data.shape)
        data_n[...,:-1,:] = data[...,1:,:]
        data_n[...,-1,:]  = data[...,-1,:]

    # Arrays of 1s and 0s indicating whether these neighbours are non-missing
    valid_w = ((data_w != missing_val)*~np.isnan(data_w)).astype(float)
    valid_e = ((data_e != missing_val)*~np.isnan(data_e)).astype(float)
    data_w[np.isnan(data_w)] = 10000 # because 0*NaN = NaN
    data_e[np.isnan(data_e)] = 10000
    if use_1d:
        # Number of valid neighoburs of each point
        num_valid_neighbours = valid_w + valid_e
        # Finished
        return data_w, data_e, valid_w, valid_e, num_valid_neighbours

    valid_s = ((data_s != missing_val)*~np.isnan(data_s)).astype(float)
    valid_n = ((data_n != missing_val)*~np.isnan(data_n)).astype(float)
    data_s[np.isnan(data_s)] = 10000
    data_n[np.isnan(data_n)] = 10000

    num_valid_neighbours = valid_w + valid_e + valid_s + valid_n

    return data_w, data_e, data_s, data_n, valid_w, valid_e, valid_s, valid_n, num_valid_neighbours

num_coast_neighbours = neighbours(land_ice, missing_val=0)[-1]
coast_mask = (open_ocean*(num_coast_neighbours > 0)).astype(bool)


scale_cap = 3
scale = np.minimum(magnitude_era5 / magnitude_ukesm, scale_cap)

rotate = (angle_era5 - angle_ukesm) # in radians ---> definitely want to keep this way round

rotate = xr.where(rotate < -np.pi, rotate + 2*np.pi, rotate) # radians
rotate = xr.where(rotate > np.pi, rotate - 2*np.pi, rotate) # radians

ocean_mask = era_mask['mask'].values[0,:] == 1 
land_mask = ~ocean_mask[0,:]

rotate_masked = rotate.vas.where(ocean_mask)

from scipy.ndimage import gaussian_filter

def smooth_xy(data, sigma=2):
    """
    Apply a Gaussian filter over the 'x' and 'y' dimensions of an xarray DataArray,
    leaving other dimensions (e.g. time) untouched.
    """
    return xr.apply_ufunc(
        gaussian_filter,
        data,
        kwargs={"sigma": sigma},
        input_core_dims=[["latitude", "longitude"]],
        output_core_dims=[["latitude", "longitude"]],
        vectorize=True,   # loops over any extra dims (time, etc.)
        dask="parallelized",
#        output_dtypes=[data.dtype],
    )

scale = smooth_xy(scale, sigma=2)

scale_masked = scale.where(ocean_mask)

rEarth = 6.371e6
deg2rad = np.pi/180.0

def distance_btw_points (point0, point1):
    
    [lon0, lat0] = point0
    [lon1, lat1] = point1
    
    dx = rEarth*np.cos((lat0+lat1)/2*deg2rad)*(lon1-lon0)*deg2rad
    dy = rEarth*(lat1-lat0)*deg2rad
    
    return np.sqrt(dx**2 + dy**2)

scale_dist = 150
lon_coast = np.ravel(coast_mask.longitude)
lat_coast = np.ravel(coast_mask.latitude)

# Make 2D lon/lat grids
lon_2d, lat_2d = np.meshgrid(coast_mask['longitude'].values, coast_mask['latitude'].values)

# Extract coastal point coordinates
coastmask = coast_mask.values
coast_lons = lon_2d[coastmask[0,:] == 1]
coast_lats = lat_2d[coastmask[0,:] == 1]

xmin = 0
xmax = 360
ymin = -90
ymax = 90

# Initialise min_dist as an array of infinities, same shape as coast_lons
min_dist = None

# Loop over all the coastal points
for i in range(coast_lons.size):
    # Skip over any points that are out of bounds
    if coast_lons[i] < xmin or coast_lons[i] > xmax or coast_lats[i] < ymin or coast_lats[i] > ymax:
        continue
    # Calculate distance of every point in the model grid to this specific coastal point, in km
    dist_to_pt = distance_btw_points([coast_lons[i], coast_lats[i]], [lon_2d, lat_2d])*1e-3
    # Figure out which cells have this coastal point as the closest one yet, and update the array
    if min_dist is None:
    # Initialise the array
        min_dist = dist_to_pt
    else:
        # Figure out which cells have this coastal point as the closest one yet, and update the array
        index = dist_to_pt < min_dist
        min_dist[index] = dist_to_pt[index]

# Cosine function moving from scaling factor to 1 over distance of scale_dist km offshore
scale_tapered = (min_dist < scale_dist)*(scale_masked - 1)*np.cos(np.pi/2*min_dist/scale_dist) + 1
# For the rotation, move from scaling factor to 0
rotate_tapered = (min_dist < scale_dist)*rotate_masked*np.cos(np.pi/2*min_dist/scale_dist)   

rotate_tapered.to_netcdf('/gws/ssde/j25b/raspwork/rasp_atmos/bias_correct/monthly/angle_m12.nc')
scale_tapered.to_netcdf('/gws/ssde/j25b/raspwork/rasp_atmos/bias_correct/monthly/magnitude_m12.nc')
