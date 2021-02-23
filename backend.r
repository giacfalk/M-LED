if (!require("pacman")) install.packages("pacman"); library(pacman)

pacman::p_load(sf, raster, exactextractr, dplyr, readxl, cowplot, ggplot2, scales, tidyr, tidyverse, rgeos, gdalUtils, chron, nngeo, strex, rgee, data.table, qgisprocess, gdata, FactoMineR, factoextra, maps  , mapdata, maptools, grid, randomForestSRC, countrycode)

ee_Initialize(email = 'giacomo.falchetta@gmail.com', drive = TRUE)
