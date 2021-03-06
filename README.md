# soil-color-book
A soil color map for every state.

Insert map of states, with colors set by soil color of state soil.

# Major TODO items:
 1. locate OSD with typos and assign fixes to one person in each region
 2. ID someone in each region to make corrections to OSDs
 3. determine gap-filling strategy: manual corrections, surrograte series, both?
 4. resolution, target output: WWW, print, both?
 5. ID people in each state to provide narrative (bbox + narrative)
 6. additional graphics: soil colors vs. depth or scatter plots
 7. make this an "official" project

# Questions:
 1. How much time can we all contribute 
 2. Set some deadlines or at least a timeline
 3. Assign some tasks: raw color maps, gap-filling, further embellishments like water or mlra, narrative authoring
 4. How widely do we want to expand this effort: should the narratives be done by someone in each state (I think so)
 5. Can some of the work be automated so that corrections in OSDs and harmonization of map units can be used in the future to make cleaner maps
 6. Do we need to involve anyone above us or get some kind of blessing from leadership
 7. Should there be a final editing of narratives by Lincoln, and follow up English editing by Aaron
 8. What are the final products; atlas style book, website, library of raster files for distribution, etc.
 9. How are the .clr files made, are they text / binary?
 10. Why do NOTCOM areas have colors via .clr mapping?
 11. Is there a more informative way to represent bedrock contact, besides "no color" (e.g. shallow and mod. deep soils)


# Misc. Ideas:
 1. STATSGO soil color maps used to "fill" NOTCOM and large misc. areas (most important in the western states and AK)
 2. fill tiny gaps (incomplete OSD-based color due to typos) with Photoshop
 3. use white or flourecent green for NODATA, this could inform a "select by color" for the above method

# Methods

## Color extraction from OSDs
https://github.com/dylanbeaudette/parse-osd


## Color conversion
http://dx.doi.org/10.1016/j.cageo.2012.10.020


## Color encoding and association with spatial Data

  1. [R,G,B channels as integers (0-255)](https://github.com/ncss-tech/soil-color-book/blob/master/R/slice-colors.R)
  2. [color-mapped via LUT of all possible "OSD colors" (303)](https://github.com/ncss-tech/soil-color-book/blob/master/R/color-table-method.R)



![](https://github.com/ncss-tech/soil-color-book/raw/master/static-images/NE_colors.gif)
![](https://github.com/ncss-tech/soil-color-book/raw/master/static-images/WI-10-preview.jpg)
![](https://github.com/ncss-tech/soil-color-book/raw/master/static-images/WI-25-preview.jpg)
![](https://github.com/ncss-tech/soil-color-book/raw/master/static-images/WI-75-preview.jpg)

