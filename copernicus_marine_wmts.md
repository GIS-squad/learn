# [Contents](#Contents)
- [Copernicus Marine Wmts](#Copernicus-Marine-Wmts)
- [Google Maps](#google-maps)
- [Todo](#todo)
- [References](#references)

## Copernicus Marine Wmts

Starting off with [this](https://help.marine.copernicus.eu/en/articles/6478168-how-to-use-wmts-to-visualize-data) resource, we construct the API calls to the WMTS service.

The most relevant parameters are as follows:

`tilematrixset` determines the Spatial Coordinate Reference (SCR) System. 
`tilematrix` can be 0-10 and determines the matrix (is akin to zoom level in Google Maps)
`tilerow` the row of the tile in the matrix
`tilecol` the column of the tile in the matrix

The number of tiles in the `tilematrix` depends on the choice of `tilematrixset`. We choose EPSG:3587 instead of EPSG:4326 as in the examples because we want to use it with Google Maps next. The number of tiles in the 'tilematrix' can be parsed from the `capabilities` of the dataset in the catalog.

To only query for the `capabilities` of a particular dataset `cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_202406` :

```
curl --output glo_phy-cur_anfc_0.083deg_PT6H-i_capabilities "https://wmts.marine.copernicus.eu/teroWmts/GLOBAL_ANALYSISFORECAST_PHY_001_024/cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_202406?SERVICE=WMTS&version=1.0.0&REQUEST=GetCapabilities"
```

The link to the `capabilities` of the entire catalog are in the reference.

Individual tiles can then be downloaded for given `product id`, `tilematrixset`, `tilematrix`, `tilerow` & `tilecol`

```
curl --output glo_phy-cur_anfc_0.083deg_PT6H-i_2_1_1.png "https://wmts.marine.copernicus.eu/teroWmts/?service=WMTS&request=GetTile&version=1.0.0&format=image%2Fpng&layer=GLOBAL_ANALYSISFORECAST_PHY_001_024%2Fcmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_202406%2Fsea_water_velocity&tilematrixset=EPSG:3857&tilematrix=2&tilerow=1&tilecol=1&time=2024-09-09T00:00:00.000000000Z&STYLE=vectorStyle:solidAndVector,cmap:thermal"

curl --output glo_phy-cur_anfc_0.083deg_PT6H-i_2_1_2.png "https://wmts.marine.copernicus.eu/teroWmts/?service=WMTS&request=GetTile&version=1.0.0&format=image%2Fpng&layer=GLOBAL_ANALYSISFORECAST_PHY_001_024%2Fcmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_202406%2Fsea_water_velocity&tilematrixset=EPSG:3857&tilematrix=2&tilerow=1&tilecol=2&time=2024-09-09T00:00:00.000000000Z&STYLE=vectorStyle:solidAndVector,cmap:thermal"

etc. etc.
```
A montage can then be created by stitching together the tiles:

```
montage glo_phy-cur_anfc_0.083deg_PT6H-i_2_1_[1-3].png -tile 3x1 -geometry +0+0 nh.png
montage glo_phy-cur_anfc_0.083deg_PT6H-i_2_2_[1-3].png -tile 3x1 -geometry +0+0 sh.png
montage nh.png sh.png -tile 1x2 -geometry +0+0 ww_cur.png
```
![Worldwide currents on 2024/09/09](/wmts/ww_cur.png)

## Google Maps

Instead of downloading the tiles and stitching them together, let Google Maps do this for us at various zoom levels on the fly. 

Note that [Google Maps' tile co-ordinates](https://developers.google.com/maps/documentation/javascript/coordinates) are compatible with Copernicus Marine's WMTS only with EPSG:3587.

We use an [ImageMapType](https://developers.google.com/maps/documentation/javascript/reference/image-overlay#ImageMapTypeOptions) to create a map with custom tiles. The source in [pubapp.js](/wmts/pubapp.js) does just this and the results can be viewed [here](https://ev.m0v.in/treecam/gis).

### Todo

Results can be viewed (here)[https://ev.m0v.in/treecam/gis]. Next immediate step is allow user to select the data for a particular date/time and also provide a drop-down for a few more example queries to the WMTS.

The [MyOcean Light](https://data.marine.copernicus.eu/viewer) viewer is another way to visualize the data though not all the data served by the WMTS is viewable in MyOcean.

### References

[The capabilities of the entire catalog](https://wmts.marine.copernicus.eu/teroWmts?service=WMTS&version=1.0.0&request=GetCapabilities) 



