# load packages
library(aqp)
library(plyr)
library(reshape2)
library(scales)

# get a copy of the latest OSD colors:
# echo "\copy osd.osd_colors TO 'osd_colors.csv' CSV HEADER " | psql -U postgres ssurgo_combined
# gzip osd_colors.csv

# load OSD colors by horizons (gzipped CSV)
# don't convert characters -> factors
x <- read.csv('../data/osd_colors.csv.gz', stringsAsFactors=FALSE, na.strings='')

# re-order by series, then depth
x <- x[order(x$series, x$top), ]

# how many colors are we really dealing with?
# 366
x$color_str <- paste0(x$matrix_wet_color_hue, ' ', x$matrix_wet_color_value , '/', x$matrix_wet_color_chroma)
x$color_str_code <- as.integer(factor(x$color_str))

# make color table
osd.color.table <- unique(x[, c('color_str', 'color_str_code')])
idx <- grep('NA', osd.color.table$color_str, invert = TRUE)
osd.color.table <- osd.color.table[idx, ]
x.rgb <- parseMunsell(osd.color.table$color_str, return_triplets=TRUE)

##
## convert sRGB to integer, 0-255 range: be sure to include entire possible range of 0-1
##
x.rgb$r_int <- round(rescale(x.rgb$r, to=c(0,255), from = c(0,1)))
x.rgb$g_int <- round(rescale(x.rgb$g, to=c(0,255), from = c(0,1)))
x.rgb$b_int <- round(rescale(x.rgb$b, to=c(0,255), from = c(0,1)))

# re-combine with original LUT, row-order is preserved
osd.color.table <- cbind(osd.color.table, x.rgb)
osd.color.table <- osd.color.table[order(osd.color.table$color_str_code), ]


# init SoilProfileCollection obj
depths(x) <- series ~ top + bottom

# slice out depths
x.slices <- slice(x, c(5, 10, 15, 25, 50, 75, 100, 125) ~ color_str_code, just.the.data=TRUE, strict=FALSE)

# convert to wide format
x.wide <- dcast(x.slices, series ~ top, value.var = 'color_str_code')
names(x.wide) <- c('series', paste0('top_', c(5, 10, 15, 25, 50, 75, 100, 125)))

## these are moist colors

# save files
write.csv(x.wide, file=gzfile('../data/osd-moist-color-codes-slices.csv.gz'), row.names = FALSE, na = '')
write.csv(osd.color.table, file=gzfile('../data/osd-moist-color-table.csv.gz'), row.names = FALSE, na = '')



