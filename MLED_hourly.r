# MLED - Multisectoral Latent Electricity Demand assessment platform
# v1.1, R programming language
# Hourly resolution
# Version: 31/05/2021
# giacomo.falchetta@feem.it

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
source("scenario_baseline.R", echo = F)
#save.image(file="bk1.Rdata")

# Run population clustering (choose travel-time based on contiguity-based clustering)
timestamp()
#source("traveltime_based_clustering.R", echo = F)
source("contiguity_based_clustering.R", echo = F)
##save.image(file="bk1.Rdata")

# Estimate electrification
timestamp()
source("electrification_estimation.R", echo = F)
##save.image(file="bk1.Rdata")

# Cropland and irrigation demand
timestamp()
source("crop_module.R", echo = F)
#save.image(file="bk1.Rdata")

# Water pumping to energy
timestamp()
source("groundwater_module.R", echo = F)
#save.image(file="bk1.Rdata")

# Residential energy demand
timestamp()
source("residential.R", echo = F)
#save.image(file="bk1.Rdata")

# Health and education demand 
timestamp()
source("health_education_module.R", echo = F)
#save.image(file="bk1.Rdata")

# Other productive
timestamp()
source("other_productive.R", echo = F)
#save.image(file="bk1.Rdata")

# Produce spatio-temporal plots of demand 
timestamp()
source("hourly_conversion_plotting.R", echo = F)
#save.image(file="bk1.Rdata")

# Write output
write_sf(sf2, paste0(home_repo_folder, 'clusters_final.gpkg',driver="GPKG"))

# Write rasters for output

r <- raster(); res(r) <- 0.5; extent(r) <- ext; crs(r) <- "+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"

fields <- c("er_kwh_tt")

for (k in fields){
writeRaster(fasterize::fasterize(clusters, r, field=k, fun="first"), paste0(k, ".tif"))
}

#################
# Economic analysis

# Run it
timestamp()
source("MLED_economic_analysis.R", echo = F)
#save.image(file="bk1.Rdata")

# Plot it
timestamp()
source("economic_analysis_plots.R", echo = F)


