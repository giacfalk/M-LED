# geom / geometry = NULL in tutti gli script
# keep at the end of some script to hasten running -> use remove instead of keep
# recover comments from py and comment all code

# MLED (Productive uses Electricity demand Generator) v0.1 - Electricity Demand Generation
# Hourly resolution
# R translation
# Version: 09/02/2021

####
# Define the working directory
setwd("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo")

# 
timestamp()
source("backend.R", echo = F)

# Import the manual_parameters, to be set before running this script
timestamp()
source("manual_parameters.R", echo = F)
    
# Select the scenario to be operated
timestamp()
source("scenario_baseline.R", echo = T)
save.image(file="bk1.Rdata")

# Cropland and irrigation demand
timestamp()
source("crop_module.R", echo = T)
save.image(file="bk1.Rdata")

# Water pumping to energy
timestamp()
source("groundwater_module.R", echo = T)
save.image(file="bk1.Rdata")

# Residential energy demand
timestamp()
source("residential.R", echo = T)
save.image(file="bk1.Rdata")

# Health and education demand 
timestamp()
source("health_education_module.R", echo = T)
save.image(file="bk1.Rdata")

# Other productive
timestamp()
source("other_productive.R", echo = T)
save.image(file="bk1.Rdata")

# 
timestamp()
source("hourly_conversion_plotting.R", echo = T)
save.image(file="bk1.Rdata")

# Write output
write_sf(sf2, paste0(home_repo_folder, 'clusters_final.gpkg',driver="GPKG"))

# Write rasters for output

r <- raster(); res(r) <- 0.5; extent(r) <- ext; crs(r) <- "+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"

fields <- c("")

for (k in fields){
writeRaster(fasterize::fasterize(clusters, r, field=k, fun="first"), paste0(k, ".tif"))
}
