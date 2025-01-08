# [Contents](#Contents)
- [Copernicus Marine Toolbox](#Copernicus-Marine-Toolbox)
  - [Install](#install)
  - [Catalogue](#catalogue)
  - [Get / Subset](#get-subset)
- [Netcdf](#netcdf)
  - [h5tools / h5dump](#h5tools)
- [matplotlib](#matplotlib)
  - [basemap](#basemap)
- [References](#references)

## Copernicus Marine Toolbox

Access service either using a CLI or a Python wrapper to construct requests.

[New version 2.0](https://help.marine.copernicus.eu/en/articles/9978784-what-s-new-in-version-2-0-0-of-the-copernicus-marine-toolbox) out today (08/01/25) with breaking changes:


### Install 
```
pip3 install copernicusmarine
pip3 show copernicusmarine
...
Requires: aiohttp, boto3, cachier, click, dask, lxml, nest-asyncio, netCDF4, numpy, pystac, requests, semver, setuptools, tqdm, xarray, zarr
...
```

### Catalogue

The [describe.py](/copernicus_marine/describe.py) file in this repo downloads the entire catalogue into a file which can then be parsed.

The [catalogue.go](/copernicus_marine/catalogue.go) file decodes the downloaded json catalogue into a Go data structure for further processing and selection of dataset ids and object store URLs to be used in subsequent queries for data.

But there's now a new data type [copernicusmarine.CopernicusMarineCatalogue](https://toolbox-docs.marine.copernicus.eu/en/pre-releases-2.0.0a4/response-types.html#copernicusmarine.CopernicusMarineCatalogue) in the 2.0 release for the output of `describe`

### Get-Subset

Most relevant options for download `dataset_id`, `filter`, `username`, `password`

Don't use `force_download` as it has been deprecated in 2.0 and data sizes are very large!!

In [get.py](/copernicus_marine/get.py) we download some sea current data for the entire world on 2023/12/1 which is about 1.9GB of data.

## Netcdf-HDF5

Almost all the data URLs are to time-chunked or geo-chunked object data stores using zarr for chunking. 

The data is usually available as `*.nc` (Netcdf) files generated using hdf5 under the hood.

```
h5dump -H -A GLOBAL_ANALYSISFORECAST_PHY_001_024/cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_202406/2023/12/glo12_rg_1d-m_20231201-20231201_3D-uovo_hcst_R20231213.nc

...
   ATTRIBUTE "_NCProperties" {
      DATATYPE  H5T_STRING {
         STRSIZE 35;
         STRPAD H5T_STR_NULLTERM;
         CSET H5T_CSET_ASCII;
         CTYPE H5T_C_S1;
      }
--
      (0): "version=2,netcdf=4.7.1,hdf5=1.8.18,"
      }
   }
...
```

Can use netCDF4 to read the `*.nc` file. 

``` 
from netCDF4 import Dataset as NetCDFFile
nc = NetCDFFile('/path/to/file.nc')

```

### h5tools-h5dump

Can also use h5tools/h5dump to view information about the datasets.  

```
apt install h5tools
h5dump -H|-A <filename.nc> // dumps headers only with/out attributes, no data
h5dump -d <dataset_name> <filename.nc> // dumps data in dataset with dataset_name - usefuly only for small datasets
```

To view the 50 elements in the dataset `depths`

```
h5dump -d depth GLOBAL_ANALYSISFORECAST_PHY_001_024/cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_202406/2023/12/glo12_rg_1d-m_20231201-20231201_3D-uovo_hcst_R20231213.nc

DATASET "depth" {            
   DATATYPE  H5T_IEEE_F32LE
   DATASPACE  SIMPLE { ( 50 ) / ( 50 ) }
   DATA {                     
   (0): 0.494025, 1.54138, 2.64567, 3.81949, 5.07822, 6.44061, 7.92956,
   (7): 9.573, 11.405, 13.4671, 15.8101, 18.4956, 21.5988, 25.2114, 29.4447,
   (15): 34.4342, 40.3441, 47.3737, 55.7643, 65.8073, 77.8539, 92.3261,
   (22): 109.729, 130.666, 155.851, 186.126, 222.475, 266.04, 318.127,
   (29): 380.213, 453.938, 541.089, 643.567, 763.333, 902.339, 1062.44,
   (36): 1245.29, 1452.25, 1684.28, 1941.89, 2225.08, 2533.34, 2865.7,
   (43): 3220.82, 3597.03, 3992.48, 4405.22, 4833.29, 5274.78, 5727.92
   }
...
   ATTRIBUTE "units" {
      DATATYPE  H5T_STRING {
         STRSIZE 1;
         STRPAD H5T_STR_NULLTERM;
         CSET H5T_CSET_ASCII;
         CTYPE H5T_C_S1;
      }
      DATASPACE  SCALAR
      DATA {
      (0): "m"
      }
   }
}

``` 

The 40th element is at around 2km depth

## matplotlib

Create a `figure` & add `subplot` to it as in [display_netcdf.py](/copernicus_marine/display_netcdf.py)

```
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(1,2,1)
ax.set_title("northward velocity")
```
### basemap

Create a basemap centered around -15 to +15 degrees longitude & 30 to 50 degrees latitude.

```
map = Basemap(projection='merc', llcrnrlon=-15, llcrnrlat=30, urcrnrlon=15, urcrnrlat=50,resolution='i')
```

![Currents at surface](/copernicus_marine/currents_0.png)

Note the difference in resolution of the basemap between `i` (intermediate on the left) and `c` (crude on the right)

![Currents at 2km depth](/copernicus_marine/currents_40.png)

Note the lack of data near the coasts at 2km depth.

## References 

[Copernicus Marine Python Interface](https://toolbox-docs.marine.copernicus.eu/en/pre-releases-2.0.0a4/python-interface.html)
