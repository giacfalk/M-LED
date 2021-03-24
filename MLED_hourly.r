# finish translate economic module to R
# installdependencies -> fix 
# wiki -> update
# check order of magnitude of results

# MLED - Multisectoral Latent Electricity Demand assessment platform
# Hourly resolution
# Version: 23/02/2021

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

# Run clustering
timestamp()
source("traveltime_based_clustering.R", echo = T)
source("contiguity_based_clustering.R", echo = T)
save.image(file="bk1.Rdata")

# Estimate electrification
timestamp()
source("electrification_estimation.R", echo = T)
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

#################
# Economic analysis

# Run it
timestamp()
source("MLED_economic_analysis.R", echo = T)
save.image(file="bk1.Rdata")

# Costs of groundwater pumps
timestamp()
source("groundwater_pumps_costs.R", echo = T)
save.image(file="bk1.Rdata")


# Plot it
timestamp()
source("economic_analysis_plots.R", echo = T)


