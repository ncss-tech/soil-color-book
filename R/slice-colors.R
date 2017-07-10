#
# 2016-12-15: fixed bug, conversion from sRGB -> HSV previously used RGB -> HSV
#


# load packages
library(aqp)
library(plyr)
library(colorspace)
library(scales)

# get a copy of the latest OSD colors:
# echo "\copy osd.osd_colors TO 'osd_colors.csv' CSV HEADER " | psql -U postgres ssurgo_combined
# gzip osd-colors-original.csv

# load OSD colors by horizons (gzipped CSV)
# don't convert characters -> factors
x <- read.csv('data/osd_colors.csv.gz', stringsAsFactors=FALSE, na.strings='')

# check: some series / horizons are missing colors
head(x)

# re-order by series, then depth
x <- x[order(x$series, x$top), ]

# note that there are some errors in there...
sort(table(x$matrix_dry_color_hue, useNA='always'), decreasing=TRUE)
sort(table(x$matrix_wet_color_hue, useNA='always'), decreasing=TRUE)


# perform color conversion
x.rgb <- with(x, munsell2rgb(matrix_wet_color_hue, matrix_wet_color_value, matrix_wet_color_chroma, return_triplets=TRUE))

# convert sRGB to HSV
x.hsv <- as(sRGB(x.rgb$r, x.rgb$g, x.rgb$b), 'HSV')@coords
              
# combine colors + series into new table for more convenient usage:
# make new cols and fill with NA
x.rgb$h <- x.hsv[, 1]
x.rgb$s <- x.hsv[, 2]
x.rgb$v <- x.hsv[, 3]

# check: OK
head(x.rgb)
              
# merge with series   
g <- data.frame(series=x$series, top=x$top, bottom=x$bottom, x.rgb, stringsAsFactors=FALSE)

# compute distace from origin ({V,S} axis) as index of brightest color
g$d <- with(g, sqrt(s^2 + v^2))

# check: OK
head(g, 20)

# clean-up, and garbage-collect
rm(x, x.rgb, x.hsv)
gc(reset=TRUE)


##
## convert sRGB to integer, 0-255 range: be sure to include entire possible range of 0-1
##
g$r_int <- round(rescale(g$r, to=c(0,255), from = c(0,1)))
g$g_int <- round(rescale(g$g, to=c(0,255), from = c(0,1)))
g$b_int <- round(rescale(g$b, to=c(0,255), from = c(0,1)))

# results are the same
rgb(g[2, c('r','g','b')])
rgb(g[2, c('r_int','g_int','b_int')], maxColorValue = 255)

##
## slice out specific depths
##

## this has several problems... as there are OSDs with multiple horizonations defined:
## https://soilseries.sc.egov.usda.gov/OSD_Docs/D/DISTIN.html
##
## ... or there may be errors in the horizons
## either way, slice() gets confused when there are > 1 matches / slice
## relax sanity checks with strict=FALSE


# init SoilProfileCollection obj
depths(g) <- series ~ top + bottom

# slice at the depths, keeping:  r_int, g_int, b_int, h, s, v
# ignore bad horizonation with strict=FALSE
g.slices <- slice(g, c(5, 10, 15, 25, 50, 75, 100, 125) ~ r_int + g_int + b_int, just.the.data=TRUE, strict=FALSE)

# save single depth slice to a file
vars <- c('series', 'r_int', 'g_int', 'b_int')
write.csv(g.slices[g.slices$top == 5, vars], file=gzfile('data/osd_colors-5cm.csv.gz'), row.names=FALSE, na='')
write.csv(g.slices[g.slices$top == 10, vars], file=gzfile('data/osd_colors-10cm.csv.gz'), row.names=FALSE, na='')
write.csv(g.slices[g.slices$top == 15, vars], file=gzfile('data/osd_colors-15cm.csv.gz'), row.names=FALSE, na='')
write.csv(g.slices[g.slices$top == 25, vars], file=gzfile('data/osd_colors-25cm.csv.gz'), row.names=FALSE, na='')
write.csv(g.slices[g.slices$top == 50, vars], file=gzfile('data/osd_colors-50cm.csv.gz'), row.names=FALSE, na='')
write.csv(g.slices[g.slices$top == 75, vars], file=gzfile('data/osd_colors-75cm.csv.gz'), row.names=FALSE, na='')
write.csv(g.slices[g.slices$top == 100, vars], file=gzfile('data/osd_colors-100cm.csv.gz'), row.names=FALSE, na='')
write.csv(g.slices[g.slices$top == 125, vars], file=gzfile('data/osd_colors-125cm.csv.gz'), row.names=FALSE, na='')


##
## select brightest color
##


# function for selecting the row with max Saturation
f <- function(i) {
  i.max <- which.max(i$d)
  return(i[i.max, c('series', 'r_int', 'g_int', 'b_int')])
}

# iterate over blocks of our data (s), defined by series
# select "brightest color" as defined by distance from {V,S} origin
g.b <- ddply(horizons(g), 'series', .fun=f, .progress='text')
              

# check:
head(g.b)

# save
write.csv(g.b[, vars], file=gzfile('data/osd-brightest-color.csv.gz'), row.names=FALSE, na='')



