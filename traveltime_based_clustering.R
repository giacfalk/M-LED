library(readxl)
library(reshape2)
library(exactextractr)
library(dplyr)
library(raster)
library(sf)
library(foreign)
library(splitstackshape)
library(ggplot2)
library(ggpmisc)
library(gglorenz)
library(cowplot)
library(acid)
library(rnaturalearth)
library(rnaturalearthdata)
library(spatstat)
library(doBy)
library(parallel)
library(rgdal)
library(data.table)
require(gdistance)
library(spatialEco)
require(gdistance)
library(rgdal)
library(rgeos)
library(nngeo)

pop = raster('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/input_folder/Population.tif')
pop <- aggregate(pop, fact=30, fun=sum, na.rm=TRUE)
pop[pop<=0] = NA

totalpopconstant = cellStats(pop, 'sum', na.rm = TRUE)

setwd('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Inequal accessibility to services in sub-Saharan Africa')
T.filename <- 'study.area.T_kenya.rds'
T.GC.filename <- 'study.area.T.GC_kenya.rds'
friction <- raster("friction_cut_1209.tif")
friction <- projectRaster(friction, pop)

friction <- overlay(friction, pop, fun = function(x, y) {
  x[is.na(y)] <- NA
  return(x)
})

function_sens <- function(x){
  a <-(1/mean(x))
}

Tr <- transition(friction, function_sens, 8) 
saveRDS(Tr, "study.area.T_kenya.rds")
T.GC <- geoCorrection(Tr)                    
saveRDS(T.GC, "study.area.T.GC_kenya.rds")


repeat {
  all = which.max(pop)
  pos = as.data.frame(xyFromCell(pop, all))
  
  new_facilities <- if(exists("new_facilities")){
    rbind(new_facilities, st_as_sf(pos, coords = c("x", "y"), crs = 4326))
  } else {
    st_as_sf(pos, coords = c("x", "y"), crs = 4326)
  }
  
  points = as.data.frame(st_coordinates(new_facilities))
  
  # Fetch the number of points
  temp <- dim(points)
  n.points <- temp[1]
  
  T.GC <- readRDS(T.GC.filename)

  # Convert the points into a matrix
  xy.data.frame <- data.frame()
  xy.data.frame[1:n.points,1] <- points[,1]
  xy.data.frame[1:n.points,2] <- points[,2]
  xy.matrix <- as.matrix(xy.data.frame)
  
  # Run the accumulated cost algorithm to make the final output map. This can be quite slow (potentially hours).
  t34_new <- accCost(T.GC, xy.matrix)
  t34_new = crop(t34_new, extent(pop))
  
  pop <- overlay(pop, t34_new, fun = function(x, y) {
    x[y<=60] <- NA
    return(x)
  })
  
  k_34 = cellStats(pop, 'sum', na.rm = TRUE)/totalpopconstant
  print(paste0("Fraction of population more than 60 minutes away from healthcare: ", k_34))
  # exit if the condition is met
  if (k_34==0) break
  
}

kenya <- read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/input_folder/gadm36_KEN_0.shp')

kenya <- st_cast(kenya, "POLYGON") %>% st_union()

prova <- new_facilities %>% 
  st_union() %>%
  st_voronoi(., envelope = kenya, dTolerance = 0, bOnlyEdges = FALSE) %>%
  st_collection_extract()

write_sf(prova, 'prova.shp')

##############

new_facilities$id = 1:nrow(new_facilities)

cluster <- makePSOCKcluster(detectCores()-1)

clusterExport(cl=cluster, c("new_facilities", "T.GC","pop",
                            "st_coordinates","accCost","aggregate",
                            "extent","overlay","cellStats","crop", "rasterToPolygons", "st_as_sf", "st_sf", "mutate", "st_union"))

functpop<-parLapply(cluster,1:nrow(new_facilities),function(i){
  id_exp = new_facilities[i, ]$id
  xy.matrix <-st_coordinates(new_facilities[i, ])
  servedpop <- accCost(T.GC, xy.matrix)
  threshold = 60
  servedpop[servedpop>threshold] <- NA
  p <- rasterToPolygons(servedpop, n=16, na.rm=TRUE, digits=1, dissolve=TRUE)
  
  # assign id to polygon = i
  p = st_as_sf(p)
  p = st_union(p) 
  p = st_sf(p)
  p$id = id_exp
  p
})

stopCluster(cluster)


pop = raster('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/input_folder/Population.tif')

for (i in 1:length(functpop)){
  if (class(functpop[[i]]$p)[1]=="sfc_MULTIPOLYGON"){
    print(i)
    functpop[[i]] <- st_cast(functpop[[i]], "POLYGON")
  }
  functpop[[i]]  <- functpop[[i]] [c("p", "id")]
}

functpop2<-sf::st_as_sf(data.table::rbindlist(functpop))

nf_temp = new_facilities
nf_temp$geometry = NULL
nf_temp = dplyr::select(nf_temp, id) %>% as.data.frame()

pol = merge(nf_temp , functpop2, by="id") %>% st_as_sf(.)

cluster <- makePSOCKcluster(detectCores()-1)
clusterExport(cl=cluster, c("pol", "st_sf", "filter",
                            "exact_extract","st_intersection","st_intersects", "pop", "%>%", "st_geometry_type", "st_cast"))

#timestamp()
pp = mclapply(1:nrow(pol),function(i){
  b<-st_intersects(pol[i,], pol[-i,])
  a<-sf::st_touches(pol[i,], pol[-i,])
  ifelse(length(setdiff(b[1][[1]], a[1][[1]]))==0, exact_extract(pop, pol[i,], 'sum'), exact_extract(pop, pol[i,], 'sum')*ifelse(length(as.numeric(st_area(st_difference(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),])))))!=0, as.numeric(st_area(st_difference(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),]))))/as.numeric(st_area(pol[i,])), 0) + exact_extract(pop, pol[i,], 'sum')*ifelse(length(as.numeric(st_area(st_intersection(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),]))))!=0), as.numeric(st_area(st_intersection(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),]))))/as.numeric(st_area(pol[i,]))/length(setdiff(b[1][[1]], a[1][[1]])),0))
})
#timestamp()

stopCluster(cluster)

pp = do.call(rbind, pp)
pol$popsum = pp

pol$id = paste0("cl", 1:nrow(pol))

write_sf(pol, "D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/onsset/kenya_clusters/clusters_tt_based.gpkg")
