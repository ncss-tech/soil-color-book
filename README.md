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

