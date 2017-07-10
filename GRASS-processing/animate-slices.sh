# images in order
images=`ls export/*-preview.jpg | sort -h -r`

# annotate images first
for x in $images
do
f=`basename $x`
depth="Soil color at `echo $f | cut -d'-' -f 1` cm depth -- 2017 USDA-NRCS"
width=`identify -format %w $x`

convert -fill black -gravity west -size ${width}x20 \
caption:"$depth" \
$x +swap -gravity southwest -composite animation/$f
done

# animate
convert -delay 240 -loop 0 animation/5-preview.jpg animation/10-preview.jpg animation/15-preview.jpg animation/25-preview.jpg animation/50-preview.jpg animation/75-preview.jpg animation/100-preview.jpg slices.gif
