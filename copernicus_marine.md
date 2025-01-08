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

### h5tools-h5dump

```
apt install h5tools
h5dump -H|-A <filename.nc> // dumps headers only with/out attributes, no data
h5dump -d <dataset_name> <filename.nc> // dumps data in dataset with dataset_name - usefuly only for small datasets
```


## matplotlib

```
```
### basemap

![Currents at surface](/copernicus_marine/currents_0.png)

![Currents at 2km depth](/copernicus_marine/currents_40.png)

## References 

[Copernicus Marine Python Interface](https://toolbox-docs.marine.copernicus.eu/en/pre-releases-2.0.0a4/python-interface.html)
