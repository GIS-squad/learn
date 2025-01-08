import copernicusmarine


catalogue = copernicusmarine.describe(contains=['SEALEVEL_GLO_PHY'], include_datasets=True, include_keywords=True)
#catalogue = copernicusmarine.describe(contains=['SEAICE_GLO_SEAICE'], include_datasets=True)
f=open("catalogue_sealevel_glo_phy","w")
f.write(str(catalogue))
f.close()

#print(catalogue)

