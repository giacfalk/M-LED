totalpopulationconstant = sum(values(population), na.rm=T)

T.filename <- 'study.area.T_kenya.rds'
T.GC.filename <- 'study.area.T.GC_kenya.rds'
friction <- raster(paste0(input_folder, "friction_cut_1209.tif"))
friction <- projectRaster(friction, population)

friction <- overlay(friction, population, fun = function(x, y) {
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
  all = which.max(population)
  pos = as.data.frame(xyFromCell(population, all))
  
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
  acc <- accCost(T.GC, xy.matrix)
  acc = crop(acc, extent(population))
  
  population <- overlay(population, acc, fun = function(x, y) {
    x[y<=60] <- NA
    return(x)
  })
  
  k_acc = cellStats(population, fun='sum', na.rm = TRUE)/totalpopulationconstant
  print(paste0("Fraction of populationulation more than 60 minutes away from healthcare: ", k_acc))
  # exit if the condition is met
  if (k_acc==0) break
  
}

kenya <- gadm0

kenya <- st_cast(kenya, "POLYGON") %>% st_union()

prova <- new_facilities %>% 
  st_union() %>%
  st_voronoi(., envelope = kenya, dTolerance = 0, bOnlyEdges = FALSE) %>%
  st_collection_extract()

write_sf(prova, 'prova.shp')

##############

new_facilities$id = 1:nrow(new_facilities)

cluster <- makePSOCKcluster(detectCores()-1)

clusterExport(cl=cluster, c("new_facilities", "T.GC","population",
                            "st_coordinates","accCost","aggregate",
                            "extent","overlay","cellStats","crop", "rasterToPolygons", "st_as_sf", "st_sf", "mutate", "st_union"))

functpopulation<-parLapply(cluster,1:nrow(new_facilities),function(i){
  id_exp = new_facilities[i, ]$id
  xy.matrix <-st_coordinates(new_facilities[i, ])
  servedpopulation <- accCost(T.GC, xy.matrix)
  threshold = 60
  servedpopulation[servedpopulation>threshold] <- NA
  p <- rasterToPolygons(servedpopulation, n=16, na.rm=TRUE, digits=1, dissolve=TRUE)
  
  # assign id to polygon = i
  p = st_as_sf(p)
  p = st_union(p) 
  p = st_sf(p)
  p$id = id_exp
  p
})

stopCluster(cluster)

for (i in 1:length(functpopulation)){
  if (class(functpopulation[[i]]$p)[1]=="sfc_MULTIPOLYGON"){
    print(i)
    functpopulation[[i]] <- st_cast(functpopulation[[i]], "POLYGON")
  }
  functpopulation[[i]]  <- functpopulation[[i]] [c("p", "id")]
}

functpopulation2<-sf::st_as_sf(data.table::rbindlist(functpopulation))

nf_temp = new_facilities
nf_temp$geometry = NULL
nf_temp = dplyr::select(nf_temp, id) %>% as.data.frame()

pol = merge(nf_temp , functpopulation2, by="id") %>% st_as_sf(.)

cluster <- makePSOCKcluster(detectCores()-1)
clusterExport(cl=cluster, c("pol", "st_sf", "filter",
                            "exact_extract","st_intersection","st_intersects", "population", "%>%", "st_geometry_type", "st_cast"))

#timestamp()
pp = mclapply(1:nrow(pol),function(i){
  b<-st_intersects(pol[i,], pol[-i,])
  a<-sf::st_touches(pol[i,], pol[-i,])
  ifelse(length(setdiff(b[1][[1]], a[1][[1]]))==0, exact_extract(population, pol[i,], 'sum'), exact_extract(population, pol[i,], 'sum')*ifelse(length(as.numeric(st_area(st_difference(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),])))))!=0, as.numeric(st_area(st_difference(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),]))))/as.numeric(st_area(pol[i,])), 0) + exact_extract(population, pol[i,], 'sum')*ifelse(length(as.numeric(st_area(st_intersection(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),]))))!=0), as.numeric(st_area(st_intersection(pol[i,], st_union(pol[setdiff(b[1][[1]], a[1][[1]]),]))))/as.numeric(st_area(pol[i,]))/length(setdiff(b[1][[1]], a[1][[1]])),0))
})
#timestamp()

stopCluster(cluster)

pp = do.call(rbind, pp)
pol$populationsum = pp

pol$id = paste0("cl", 1:nrow(pol))

write_sf(pol, paste0(home_repo_folder, 'clusters_final.gpkg'))
