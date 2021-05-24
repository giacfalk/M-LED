totalpopulationconstant = sum(values(population), na.rm=T)

friction <- raster(paste0(input_folder, "friction_cut_1209.tif"))
friction <- projectRaster(friction, population)

friction <- overlay(friction, population, fun = function(x, y) {
  x[is.na(y)] <- NA
  return(x)
})

population <- aggregate(population, fact=10, fun="sum")
friction <- aggregate(friction, fact=10, fun="mean")

function_sens <- function(x){
  a <-(1/mean(x))
}

Tr <- transition(friction, function_sens, 8) 
saveRDS(Tr, "study.area.T_kenya.rds")
T.GC <- geoCorrection(Tr)                    
saveRDS(T.GC, "study.area.T.GC_kenya.rds")

repeat {
  all = which.max(population)
  print(all)
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
  
  # Convert the points into a matrix
  xy.data.frame <- data.frame()
  xy.data.frame[1:n.points,1] <- points[,1]
  xy.data.frame[1:n.points,2] <- points[,2]
  xy.matrix <- as.matrix(xy.data.frame)
  
  # Run the accumulated cost algorithm to make the final output map. This can be quite slow (potentially hours).
  acc <- accCost(T.GC, xy.matrix)
  acc = projectRaster(acc, population)
  
  values(population)[which(values(acc<=60))] <- NA
  values(population)[all] <- NA
  
  k_acc = cellStats(population, stat='sum', na.rm = TRUE)/totalpopulationconstant
  print(paste0("Fraction of populationulation more than 60 minutes away:", k_acc))
  # exit if the condition is met
  if (k_acc<=0.05) break
  
}

kenya <- gadm0
kenya <- st_cast(kenya, "POLYGON") %>% st_union()

prova <- new_facilities %>% 
  st_union() %>%
  st_voronoi(., envelope = kenya, dTolerance = 0, bOnlyEdges = FALSE) %>%
  st_collection_extract()

prova <- st_intersection(prova, kenya)

write_sf(prova, paste0(home_repo_folder, 'clusters_final.gpkg'))

clusters <- prova
