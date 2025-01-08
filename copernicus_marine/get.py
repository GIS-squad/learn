import copernicusmarine
import os
from datetime import datetime
import xarray as xr

product_id = "GLOBAL_ANALYSIS_PHY_001_024"
dataset_id = "cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m"

# Requested time period
start_date = datetime(2023, 12, 1)
date_str = start_date.strftime('%Y%m%d')

copernicusmarine.get(
    dataset_id=dataset_id, 
    filter=f"*{date_str}*",
    username='username',
    password='password'
    )
