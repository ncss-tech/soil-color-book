# process color channels

# current filename, first argument
depth=$1

# colors to iterate over
colors="r
g
b"

# null-filling resolution
null_res=300

# number of levels used in composite
nlevels=64

# iterate over files
for color in $colors
  do
	# make file name
	base=color${depth}cm_90M_${color}1.tif
  
	# notification
	echo "working on $base..."

	# import
	r.in.gdal --q --o in=data/$base out=file.$color
	
	# fill nulls at 5km res
	g.region rast=file.$color -a res=$null_res
	# note that we have to make a temp copy of the map at the new res, r.fillnulls works at the native res
	r.mapcalc --o "temp = file.$color"
	r.fillnulls --q --o in=temp output=filled.$color method=bicubic

	# patch together at native resolution (90m)
	g.region rast=file.$color -a
	r.patch --q --o in=file.$color,filled.$color out=fixed.$color
	
	# reset colors to grey 0-1
	r.colors --q map=fixed.$color color=grey1.0
  done

# composite at native res
g.region rast=file.$color -a
r.composite --q --o red=fixed.r green=fixed.g blue=fixed.b output=${depth}.final levels=$nlevels

## exporting as PNG becuase TIFF files don't contain the full color table
## this is aking to exporting the GRASS display to file
r.out.png --o ${depth}.final out=export/${depth}-final.png
## make preview
convert -resize 800x export/${depth}-final.png export/${depth}-preview.jpg

## embed spatial reference information and convert to GeoTiff
gdal_translate -ot Byte -of GTiff -a_nodata 255 -a_srs "+proj=tmerc +lat_0=0 +lon_0=-90 +k=0.9996 +x_0=520000 +y_0=-4480000 +ellps=GRS80 +units=m +no_defs" -co "COMPRESS=LZW" -stats export/${depth}-final.png export/${depth}-final.tif

# clean-up:
# g.remove rast=temp
#for color in $colors
#  do
#	g.remove rast=file.$color,filled.$color,fixed.$color
#  done

