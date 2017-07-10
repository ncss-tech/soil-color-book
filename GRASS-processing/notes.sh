
# TODO: add MASK from WI outline
# TODO: output geotiff

# make a new location for WI, UTM NAD83HARN
g.region rast=5-red -ap

# convert coordinate system of WI shp
# get via gdalsrsinfo :
# +proj=tmerc +lat_0=0 +lon_0=-90 +k=0.9996 +x_0=520000 +y_0=-4480000 +ellps=GRS80 +units=m +no_defs 
ogr2ogr -t_srs '+proj=tmerc +lat_0=0 +lon_0=-90 +k=0.9996 +x_0=520000 +y_0=-4480000 +ellps=GRS80 +units=m +no_defs' wi_border.shp State.shp

# set MASK from outline of WI
v.in.ogr --o dsn=data layer=wi_border out=wi_border
v.to.rast wi_border use=val val=1 out=wi_border_rast
g.copy wi_border_rast,MASK


# about 15 minutes each

sh process-channels.sh 5
sh process-channels.sh 10
sh process-channels.sh 15
sh process-channels.sh 25
sh process-channels.sh 50
sh process-channels.sh 75
sh process-channels.sh 100

