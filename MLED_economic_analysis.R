clusters = read_sf(paste0(home_repo_folder, 'clusters_final.gpkg'))

# Import all Yield (kg/ha) cropland layers (Default datasets used: MapSPAM)
# NB: when using MapSPAM use harvested area, which accounts for multiple growing seasons per year)
rasters_rainfed = list.files(path = paste0(spam_folder, "spam2010v1r0_global_yield.geotiff") , pattern = 'r.tif')

# Import all Yield (kg/ha) cropland layers (Default datasets used: MapSPAM)
rasters_irrigated = list.files(path = paste0(spam_folder, "spam2010v1r0_global_yield.geotiff") , pattern = 'i.tif')

# 1) Estimate the yield gap
#Calculate zonal statistics for each crop for yield in rainfed areas
# NB: when using MapSPAM use harvested area, which accounts for multiple growing seasons per year)

for (X in rasters_rainfed){
  print(X)
  a = paste0("Y_" , gsub("_r.tif", "", gsub("spam2010v1r0_global_yield_", "", X)))
  clusters[a] <- exactextractr::exact_extract(raster(paste0(spam_folder, "spam2010v1r0_global_yield.geotiff/", X)), clusters, fun="mean")
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters <- clusters %>%  mutate(!!paste0("Y_", gsub("_r.tif", "", gsub("spam2010v1r0_global_yield_", "", X)), "_tot") := (!!as.name(a)) * pull(!!aa[paste0("A_", gsub("_r.tif", "", gsub("spam2010v1r0_global_yield_", "", X)))])) 
}

climatezones = raster(paste0(input_folder, 'GAEZ_climatezones.tif'))
clusters$climatezones <- exactextractr::exact_extract(climatezones, clusters, fun="majority")

# Extract the average pixel value of pixels for irrigated and rainfed agriculture in each GAEZ climatezone for each crop according to MapSPAM values, and substract them
# Calculate statistics (rainfed)

a = raster(paste0(spam_folder, "spam2010v1r0_global_yield.geotiff/", rasters_irrigated[1]))
climatezones_p <- projectRaster(climatezones, a, method = "ngb")

list_r <- list()

for (X in rasters_rainfed){
  print(X)
  a = raster(paste0(spam_folder, "spam2010v1r0_global_yield.geotiff/", X))
  list_r[[X]] <- as.data.frame(zonal(a, climatezones_p, fun='mean', digits=2, na.rm=TRUE))
  list_r[[X]]$crop <- paste0("Y_" , gsub(".tif", "", gsub("spam2010v1r0_global_yield_", "", X)))
  
}

list_r <- do.call(rbind, list_r)
list_r$type = "r"

# Calculate statistics (irrigated)

list_i <- list()

for (X in rasters_irrigated){
  print(X)
  a = raster(paste0(spam_folder, "spam2010v1r0_global_yield.geotiff/", X))
  list_i[[X]] <- as.data.frame(zonal(a, climatezones_p, fun='mean', digits=2, na.rm=TRUE))
  list_i[[X]]$crop <- paste0("Y_" , gsub(".tif", "", gsub("spam2010v1r0_global_yield_", "", X)))
}

list_i <- do.call(rbind, list_i)
list_i$type = "i"

list <- rbind(list_r, list_i)

list$crop <- substr(list$crop, 3, 6)

# 

list <- list %>% group_by(crop, zone) %>% summarise(mean=mean[2]-mean[1])
list$mean <- ifelse(list$mean<0, 0, list$mean)

# Derive YG by crop by cluster (depending on the climate zone), by multiplying per ha WG by a of cluster for each crop

for (crop in unique(list$crop)){

  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
clusters <- clusters %>%  mutate(!!paste0(paste0("yg_", crop)) := (pull(!!aa[paste0("A_", crop)]))*list$mean[list$crop==crop][aa$clima_zone]) 

}

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters$yg_total = as.vector(aa %>%  dplyr::select(starts_with('yg_')) %>% rowSums(na.rm = T) %>% as.numeric())

# 2) Calculate potential economic revenue based on value of crops 
####
# Calculate revenue from new yield (p*new q for each crop)
# but apply constraints of no new revenue if the maximum depth for pumping constraint is not met
# import localprices_layer (usd/kg) (data is referring to 2018 from prices.xlsx in input folder). Also see http://www.nafis.go.ke/

# Process crop prices csv and convert it to a shapefile
prices = read.csv(paste0(input_folder, 'prices_with_coordinates.csv'))
prices <- st_as_sf(prices, coords=c("ï..X", "Y"), crs=4326)
colnames(prices)[2:43] <- paste0("pri_", colnames(prices)[2:43])

# Merge polygons based on nearest neighbour (i.e. define the local price for each crop)
result <- qgis_run_algorithm(
  "native:joinbynearest",
  INPUT = clusters,
  INPUT_2 = prices,
  NEIGHBORS = 1
)

clusters <- sf::read_sf(qgis_output(result, "OUTPUT"))

# Sum up to calculate total new local revenue (BENEFIT from YIELD DUE TO IRRIGATION)
# NB: No yield gain possible if distance/depth thresholds to water are not met

cols = grep("pri_", colnames(clusters), value=T)
ygs = grep("yg", colnames(clusters), value=T)

for (i in 1:length(cols)){
mostsimilar <- agrep(cols[i],ygs,value=T, max.distance = 3)

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters <- clusters %>%  mutate(!!paste0("added_", mostsimilar) := (pull(!!aa[paste0("pri_", gsub("yg_", "", mostsimilar))])) * (pull(!!aa[paste0(mostsimilar)])))

}

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters$tt_ddvl = as.vector(aa %>%  dplyr::select(starts_with('added_')) %>% rowSums(na.rm = T) %>% as.numeric())

# 3) Calculate transportation cost for crops
# Formula: TC = 2 * (TTM x fuelcost x lpermin) * n

clusters$traveltime_market = exact_extract(traveltime_market, clusters, 'mean')

clusters$diesel_price = exact_extract(traveltime, clusters, 'mean')

# impose limit travel time to market 
clusters$remote_from_market = ifelse(clusters$traveltime_market>360, 1, 0)

clusters$transp_costs = 2 * (clusters$traveltime_market*fuel_consumption*clusters$diesel_price) * (clusters$yg_total/1000/truck_bearing_t)

# lack of market access makes the gains unprofitable
clusters$tt_ddvl = ifelse(clusters$remote_from_market==1, 0, clusters$tt_ddvl)

# 4) Calculate cost for purchasing household appliances (for both new electrified and tier shift households)

clusters$appliances_cost = ifelse(clusters$isurban ==1, (urb1_app_cost * clusters$HHs * clusters$acc_pop_share_t1_new + urb2_app_cost * clusters$HHs * clusters$acc_pop_share_t2_new + urb3_app_cost * clusters$HHs * clusters$acc_pop_share_t3_new + urb4_app_cost * clusters$HHs * clusters$acc_pop_share_t4_new),(rur1_app_cost * clusters$HHs * clusters$acc_pop_share_t1_new + rur2_app_cost * clusters$HHs * clusters$acc_pop_share_t2_new + rur3_app_cost * clusters$HHs * clusters$acc_pop_share_t3_new + rur4_app_cost * clusters$HHs *  clusters$acc_pop_share_t4_new))

# 5) Model cost of groundwater pump 
# 5.1. estimate the cost curve that links hydraulic head H_i and the pumping capacity required Q_i based on the meta-analysis of the costs of groundwater development projects in Sub-Saharan Africa carried out in  Xenarios and Pavelic (2013).


# 5.2 estimate the total cost of pumps in each cluster based on q and h

# Costs of groundwater pumps
timestamp()
source("groundwater_pumps_costs.R", echo = F)

mean_q_pump = 0.002500002 # 9 m3/h
SD = 0.002047534
Q1 = mean_q_pump - 0.675 * SD
Q3 = mean_q_pump + 0.675 * SD

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters$q_sust = as.vector(aa %>%  dplyr::select(starts_with('q_sust')) %>% qlcMatrix::rowMax() %>% as.numeric())

clusters$n_pumps_Q1 = (0.33 * clusters$q_sust)/Q1
clusters$n_pumps_M = (0.33 * clusters$q_sust)/mean_q_pump
clusters$n_pumps_Q3 = (0.33 * clusters$q_sust)/Q3

clusters$TC_pumping = ((clusters$gr_wat_depth * 228.1071)  + (Q1*823975) + (-21312.3*Q1*clusters$gr_wat_depth) -223.0523)*clusters$n_pumps_Q1 + ((clusters$gr_wat_depth * 228.1071)  + (Q3*823975) + (-21312.3*Q3*clusters$gr_wat_depth) -223.0523)*clusters$n_pumps_Q3 + ((clusters$gr_wat_depth * 228.1071)  + (mean_q_pump*823975) + (-21312.3*mean_q_pump*clusters$gr_wat_depth) -223.0523)*clusters$n_pumps_M

# 6) Cost of purchasing healthcare and education appliances
clusters$hc_appliances_cost = clusters$beds1 * hc_1_app_cost + clusters$beds2 * hc_2_app_cost + clusters$beds3* 0.6 * hc_3_app_cost + clusters$beds4 * 0.3 * hc_4_app_cost + clusters$beds5 * 0.1 * hc_5_app_cost

clusters$sch_appliances_cost = clusters$pupils1 * sch_1_app_cost + clusters$pupils2 * sch_2_app_cost + clusters$pupils3 * sch_3_app_cost + clusters$pupils4 * sch_4_app_cost + clusters$pupils5 * sch_5_app_cost

# 7) Cost of crop processing
# Define average processing costs for each crop:
# FC_unit = machinery (with a certain processing capacity)
# VC = power consumption + operation and maintaniance 
# FC_percropi = (yield_i / capacity_machine_i)*FC_i
# VC_percropi = FC_percropi*0.1 + ...
# TC = sum(FC_percropi+VC_percropi)

# Import csv of machines cost and processing capacity

# Make calculations


# 8) Net agricoltural profit
clusters$tt_ddvl = ifelse(clusters$transp_costs>clusters$tt_ddvl, 0, clusters$tt_ddvl)

lifetimepump = 20
discount_rate = 0.15

clusters$profit_yearly = clusters$tt_ddvl - clusters$transp_costs - clusters$TC_pumping/(1+discount_rate)^lifetimepump 

clusters$profit_yearly = ifelse(clusters$profit_yearly<0, 0, clusters$profit_yearly)

# 9) Paybacktime of electrification in each cluster
# clusters$PBT = clusters$investmentreq / clusters$profit_yearly

#print share of pop without access with PBT < 5 years
# clusters$noaccsum[clusters.PBT < 5].sum()  
# clusters$noaccsum[clusters.PBT < 5].sum()  / clusters$noaccsum.sum()