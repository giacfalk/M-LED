email<-readline(prompt="Enter your Gmail address (after having enabled it to use Google Earth Engine): " )

if (!require("pacman")) install.packages("pacman"); library(pacman)

pacman::p_load(sf, raster, exactextractr, dplyr, readxl, cowplot, ggplot2, scales, tidyr, tidyverse, rgeos, gdalUtils, chron, nngeo, strex, rgee, data.table, gdata, FactoMineR, factoextra, maps  , mapdata, maptools, grid, randomForestSRC, countrycode, remotes, stars, gdistance, rgl, rasterVis, qlcMatrix)

if (!require("qgisprocess")) remotes::install_github("paleolimbot/qgisprocess"); library(qgisprocess)
qgis_configure()

if (!require("rgis")) remotes::install_github("JGCRI/rgis"); library(rgis)

ee_Initialize(email = email, drive = TRUE)