# Groundwater and surface water pumping module

# Use Google Earth Engine to extract the distance to the nearest source of surface water
gaul = ee$FeatureCollection("FAO/GAUL/2015/level0")$filter(ee$Filter$eq('ADM0_NAME', countryname))
i = ee$Image("JRC/GSW1_2/GlobalSurfaceWater")$select('transition')$clip(gaul)
i = i$mask(i$lte(2)$And(i$gt(0)))
maxDist = ee$Kernel$circle(25000, 'meters', TRUE, 1)
kernel = ee$Kernel$euclidean(25000,"meters");
i = i$distance(kernel,FALSE)$clip(gaul)

img_02 <- ee_as_raster(
  image = i,
  region = gaul$geometry(),
  via = "drive",
  scale = 1000
)

# Calculate the mean distance from each cluster to the nearest source of surface water
clusters$surfw_dist <- exact_extract(raster(img_02), clusters, fun="mean")


# Groundwater depth
# Reclassify to numeric
DepthToGroundwater$depthwater = ifelse(DepthToGroundwater$DTWAFRICA_ == 'VS', 3.5, ifelse(DepthToGroundwater$DTWAFRICA_ == "S", 16, ifelse(DepthToGroundwater$DTWAFRICA_ == "SM", 37.5, ifelse(DepthToGroundwater$DTWAFRICA_ == "M", 75, ifelse(DepthToGroundwater$DTWAFRICA_ == "D", 175, ifelse(DepthToGroundwater$DTWAFRICA_ == "D", 250, 0))))))

DepthToGroundwater$depthwater <- as.numeric(DepthToGroundwater$depthwater)

groundwater_depth <- rasterFromXYZ(DepthToGroundwater[c("X", "Y", "depthwater")], crs = 4326)

# Extract mean value within each cluster
clusters$gr_wat_depth <- exactextractr::exact_extract(groundwater_depth, clusters, fun="mean")

# Groundwater storage
GroundwaterStorage$storagewater = ifelse(GroundwaterStorage$GWSTOR_V2 == 'VL', 0, ifelse(GroundwaterStorage$GWSTOR_V2 == "L", 500, ifelse(GroundwaterStorage$GWSTOR_V2 == "LM", 5500, ifelse(GroundwaterStorage$GWSTOR_V2 == "M", 17500, ifelse(GroundwaterStorage$GWSTOR_V2 == "H", 37500, 50000)))))

GroundwaterStorage$storagewater <- as.numeric(GroundwaterStorage$storagewater)

groundwater_storage <- rasterFromXYZ(GroundwaterStorage[c("X", "Y", "storagewater")], crs = 4326)

# Extract mean value within each cluster
clusters$gr_wat_storage <- exactextractr::exact_extract(groundwater_storage, clusters, fun="mean")


# Groundwate productivity
GroundwaterProductivity$Productivitywater = ifelse(GroundwaterProductivity$GWPROD_V2 == 'VH', 25, ifelse(GroundwaterProductivity$GWPROD_V2 == "H", 12.5, ifelse(GroundwaterProductivity$GWPROD_V2 == "M", 3, ifelse(GroundwaterProductivity$GWPROD_V2 == "LM", 0.75, ifelse(GroundwaterProductivity$GWPROD_V2 == "L", 0.3, 0.05)))))

GroundwaterProductivity$Productivitywater <- as.numeric(GroundwaterProductivity$Productivitywater)

groundwater_Productivity <- rasterFromXYZ(GroundwaterProductivity[c("X", "Y", "Productivitywater")], crs = 4326)

# Extract mean value within each cluster
clusters$gr_wat_productivity <- exactextractr::exact_extract(groundwater_Productivity, clusters, fun="mean")

# To fix potential bugs in the data, delete negative values
clusters$gr_wat_depth = ifelse(clusters$gr_wat_depth<0, 0, clusters$gr_wat_depth)
clusters$surfw_dist = ifelse(is.na(clusters$surfw_dist), 1000000, clusters$gr_wat_depth)

# Calculate groundwater pump flow rate required in m3/s as the maximum requirement of 12 months
for (i in c(1:12)){
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0("q" , as.character(i))] = aa[paste0('monthly_IRREQ' , "_" , as.character(i))] /30/nhours_irr/3600
}

#constraint for the flow rate, where the amount of groundwater depletion during the 6 hours with irrigation is lower than the amount of groundwater generation during the 18 hours with no irrigation
clusters["qc1"]=((clusters$gr_wat_productivity*(24-nhours_irr)/nhours_irr) + clusters$gr_wat_productivity)/1000*clusters$area*0.05

#constraint for the flow rate, where the flow rate to consume completely the storage in 6 hours is higher than the flow rate required
clusters["qc2"]=clusters$gr_wat_storage * clusters$area*0.05 *10 /(nhours_irr * 3600) + (clusters$gr_wat_productivity/1000)

#if the flow rate is lower than the productivity no problem
#if the th flow rate complies the 2 constraints it is ok as well
#if neither hold, the flow rate is too much and the irrigation implies a depletion of the groundwater reservoir, so no optimal condition for the crop growth, highlighting this problem with a flag and bringing down the pump capacity to sustainable levels
for (i in 1:12){
  print(i)
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0("warning" , as.character(i))] = ifelse((aa[paste0("q", as.character(i))]<aa["qc1"]) & (aa[paste0("q", as.character(i))]<aa["qc2"]), 0, 1)
  
  # Sustainable groundwater pumping rate
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0("q_sust" , as.character(i))] = ifelse((aa[paste0("q", as.character(i))]<aa["qc1"]) & (aa[paste0("q", as.character(i))]<aa["qc2"]), pull(aa[paste0("q", as.character(i))]), pmin(clusters$qc1, clusters$qc2))
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  # Unmet demand due to unsustainable pumping
  clusters[paste0("q_diff", as.character(i))] = aa[paste0("q", as.character(i))] - aa[paste0("q_sust", as.character(i))]
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  # RGH to estimate power for pump (in W), missing the head losses
  clusters[paste0('powerforpump', as.character(i))] = (rho* g * clusters$gr_wat_depth* aa[paste0("q_sust", as.character(i))])/eta_pump
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0('powerforpump', as.character(i))] = ifelse(aa["gr_wat_depth"]>threshold_groundwater_pumping, 0, pull(aa[paste0('powerforpump', as.character(i))]))
  
  clusters["nogroundwater"] = ifelse(aa["gr_wat_depth"]>threshold_groundwater_pumping, 1, 0)
  
  #  If necessary, and if it is possible, get the difference between q and q_sust from surface water bodies
  # NB: groundwater pumping is always prioritised!
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0("surfw_q", as.character(i))] = ifelse(aa["nogroundwater"] == 0, pull(aa[paste0("q_diff", as.character(i))]), pull(aa[paste0("q", as.character(i))]))
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  # But put a distance limit 
  clusters[paste0("surfw_q", as.character(i))] = ifelse(aa["surfw_dist"]<=threshold_surfacewater_distance, pull(aa[paste0("surfw_q", as.character(i))]), 0)
  
  # And put a variable to signal clusters where we cannot meet irrigation needs nither by groundwater nor by surfacewater pumping
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0("imposs_wat", as.character(i))] = ifelse((aa[paste0("q_diff", as.character(i))]!=0) & (aa["surfw_dist"]>threshold_surfacewater_distance), 1, 0)
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0("surfw_w", as.character(i))] = aa[paste0("surfw_q", as.character(i))]*((32 * water_speed * aa["surfw_dist"] *water_viscosity)/pipe_diameter**2)/eta_pump
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  #Calculate monthly electric requirement
  clusters[paste0('wh_monthly', as.character(i))] = aa[paste0('powerforpump', as.character(i))]*nhours_irr*30 + aa[paste0('surfw_w', as.character(i))]*nhours_irr*30
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0('er_kwh' , as.character(i))] = aa[paste0('wh_monthly', as.character(i))]/1000
}

# simulate daily profile

for (k in 1:12){
  
  print(k)
  
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters[paste0('er_kwh_' , as.character(k) , "_" , as.character(i))] <- (aa[paste0('er_kwh', as.character(k))]/30)*load_curve_irr[i]
  }}


for (k in 1:12){
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  
  clusters[paste0('er_kwh_tt' , as.character(k))] = aa[paste0('er_kwh' , as.character(k))]/30
}


for (k in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters[paste0('er_kwh_' , as.character(k) , "_" ,  as.character(i))] = aa[paste0('er_kwh_' , as.character(k) , "_" , as.character(i))]/aa[paste0('er_kwh_tt' , as.character(k))]
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters[paste0('er_kwh_' , as.character(k) , "_" , as.character(i))] = aa[paste0('er_kwh_' , as.character(k) , "_" , as.character(i))]
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters[paste0('er_kwh_' , as.character(k) , "_" , as.character(i))] <- ifelse(is.na(aa[paste0('er_kwh_' , as.character(k) , "_" , as.character(i))]), 0, pull(aa[paste0('er_kwh_' , as.character(k) , "_" , as.character(i))]))
  }}
