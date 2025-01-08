import sys
sys.path.remove('/usr/lib/python3/dist-packages')

from mpl_toolkits.basemap import Basemap 
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
import numpy as np

nc = NetCDFFile('/path/to/copernicus/marine/GLOBAL_ANALYSISFORECAST_PHY_001_024/cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_202406/2023/12/glo12_rg_1d-m_20231201-20231201_3D-uovo_hcst_R20231213.nc')

lat = nc.variables['latitude'][:]
lon = nc.variables['longitude'][:]
time = nc.variables['time'][:]

u = nc.variables['uo'][:][:][:] # 10m u-component of winds
v = nc.variables['vo'][:][:][:] # 10m v-component of winds

uu = u[0][40][:][:]
vv = v[0][40][:][:]

fig = plt.figure()
ax = fig.add_subplot(1,2,1)
ax.set_title("northward velocity")

map = Basemap(projection='merc',llcrnrlon=-15.,llcrnrlat=30.,urcrnrlon=15.,urcrnrlat=50.,resolution='i') # projection, lat/lon extents and resolution of polygons to draw
# resolutions: c - crude, l - low, i - intermediate, h - high, f - full

map.drawcoastlines()
map.drawstates()
map.drawcountries()
map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
map.drawcounties() # you can even add counties (and other shapefiles!)

parallels = np.arange(30,50,5.) # make latitude lines ever 5 degrees from 30N-50N
meridians = np.arange(-15,15,5.) # make longitude lines every 5 degrees from 15W to 15E
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

lons,lats= np.meshgrid(lon,lat)
#(lon-180,lat) # if in the dataset, longitude is 0 through 360, you need to subtract 180 to properly display on map
x,y = map(lons,lats)

nv = map.contourf(x,y,uu[:][:])#u[0,:,:])
cb = map.colorbar(nv, "bottom", size="5%", pad="2%")
cb.set_label('Northward Velocity (m/s)')

ax = fig.add_subplot(1,2,2)
ax.set_title("eastward velocity")
map = Basemap(projection='merc',llcrnrlon=-15.,llcrnrlat=30.,urcrnrlon=15.,urcrnrlat=50.,resolution='c') # projection, lat/lon extents and resolution of polygons to draw
# resolutions: c - crude, l - low, i - intermediate, h - high, f - full

map.drawcoastlines()
map.drawstates()
map.drawcountries()
map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
map.drawcounties() # you can even add counties (and other shapefiles!)

parallels = np.arange(30,50,5.) # make latitude lines ever 5 degrees from 30N-50N
meridians = np.arange(-15,15,5.) # make longitude lines every 5 degrees from 95W to 70W
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

lons,lats= np.meshgrid(lon,lat)
x,y = map(lons,lats)

ev = map.contourf(x,y,vv[:][:])#u[0,:,:])
cb = map.colorbar(ev, "bottom", size="5%", pad="2%")
cb.set_label('Eastward Velocity (m/s)')

plt.show()
fig.savefig('currents.png')
