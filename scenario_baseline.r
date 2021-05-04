#####################
# Parameters
#####################

# Country parameters
countryname = 'Kenya' 
countryiso3 = 'KEN' # ISO3
national_official_population = 52000000 # number of people # REF:
national_official_elrate = 0.74 # national electricity access rate
national_official_population_without_access = national_official_population- (national_official_population*national_official_elrate) # number of people without access

# Planning horizon parameters
today = 2020
planning_year = 2030
planning_horizon = planning_year - today
discount_rate = 0.15 

# Energy efficiency improvement factors
eff_impr_rur1= 0.05
eff_impr_rur2= 0.075
eff_impr_rur3= 0.1
eff_impr_rur4= 0.125
eff_impr_rur5= 0.15

eff_impr_urb1= 0.05
eff_impr_urb2= 0.075
eff_impr_urb3= 0.1
eff_impr_urb4= 0.125
eff_impr_urb5= 0.15

# Groundwater pump technical parameters
rho = 1000 # density of water (1000 kg / m3)
g = 9.81 # gravitational constant (m / s2)
c = 3.6 * (10^6) # differential pressure, (Pa)

# Surface water parameters
water_speed = 2 #m/s, https://www.engineeringtoolbox.com/flow-velocity-water-pipes-d_385.html
water_viscosity = 0.00089 #https://www.engineersedge.com/physics/water__density_viscosity_specific_weight_13146.htm
pipe_diameter = 0.8 # m

#Threshold parameters
threshold_surfacewater_distance = 5000 # (m): distance threshold which discriminates if groundwater pumping is necessary or a surface pump is enough # REF:
threshold_groundwater_pumping = 15 # (m): maximum depth at which the model allows for water pumping: beyond it, no chance to install the pump # REF:

#number of hours of pumping, 3 during the morning and 3 during the evening
nhours_irr = 6
eta_pump = 0.75

# Transportation costs
fuel_consumption = 15 # (l/h) # REF: OnSSET
fuel_cost = 1 # (USD/l) # baseline, then adapted based on distance to city
truck_bearing_t = 15 # (tons) # REF: https://en.wikipedia.org/wiki/Dump_truck

#Pumo economic parameters
LCOE_for_pumping = 0.08 # USD/kWh # REF:
lifetimepump = 30

# import local crop prices csv.  Structure: X, Y, City, cropname1, cropname 2, ...
prices = readxl::read_xls(paste0(input_folder , "prices.xls"))

# Appliances cost, household (check ./ramp/ramp/RAMP_households/Appliances cost.xlsx for inputs)
rur1_app_cost=154
rur2_app_cost=171
rur3_app_cost=278
rur4_app_cost=958
rur5_app_cost=1905

urb1_app_cost=113
urb2_app_cost=307
urb3_app_cost=902
urb4_app_cost=1464
urb5_app_cost=2994

# Appliances cost, schools (check ./ramp/ramp/RAMP_social/Appliances_schools.xlsx for inputs)
sch_1_app_cost = 60
sch_2_app_cost = 360
sch_3_app_cost = 1590
sch_4_app_cost = 2550
sch_5_app_cost = 3220

# Appliances cost, healtchare  (check ./ramp/ramp/RAMP_social/Appliances_healthcare.xlsx for inputs)
hc_1_app_cost = 110
hc_2_app_cost = 4710
hc_3_app_cost = 95060
hc_4_app_cost = 305660
hc_5_app_cost = 611450

#####################
# Input data
#####################

#
clusters = read_sf(paste0(home_repo_folder , 'clusters_final.gpkg'))

#
provinces <- read_sf(paste0(db_folder, '/input_folder/KEN_8_provinces.shp'))

# Country and provinces shapefiles
gadm0 = read_sf(paste0(input_folder , 'gadm36_' , countryiso3 , '_0.shp'))
gadm1 = read_sf(paste0(input_folder , 'gadm36_' , countryiso3 , '_1.shp'))
gadm2 = read_sf(paste0(input_folder , 'gadm36_' , countryiso3 , '_2.shp'))
gadm3 = read_sf(paste0(input_folder , 'gadm36_' , countryiso3 , '_3.shp'))

# Define extent of country analysed
ext = extent(gadm0)

# Import cropland extent (Default dataset used: GFSAD30CE)
cropland_extent = raster(paste0(input_folder , 'Croplands_GFSAD30AFCE.tif'))

# Import climatezones (Default datasets used: GAEZ soil classes)
climatezones = raster(paste0(input_folder , 'GAEZ_climatezones.tif'))

# Import surface water basins layer (Default datasets used: Global Surface Water Explorer)
categories_surface_water = raster(paste0(input_folder , 'transitions.tif'))

# Import diesel price layer (In each pixel: 2015 prices baseline , cost per transporting it from large cities)
diesel_price = raster(paste0(input_folder , 'diesel_price_baseline_countryspecific.tif'))

#
crops = readxl::read_xlsx(paste0(input_folder , 'crops_cfs_ndays_months.xlsx'))

# plot on a fishnet of 1x1 km
template <- raster(paste0(db_folder, '/input_folder/template_1km.tif'))

# Import csv of energy consumption by crop 
energy_crops = read.csv(paste0(input_folder,'crop_processing.csv'))

crops = read_xlsx(paste0(input_folder ,'crops_cfs_ndays_months.xlsx'))

#
pet = stack(paste0(input_folder , "TerraClimate/TerraClimate_pet_2015.nc"))
ppt = stack(paste0(input_folder , "TerraClimate/TerraClimate_ppt_2015.tif"))
soil = stack(paste0(input_folder , "TerraClimate/TerraClimate_soil_2015.nc"))

#
roads<-read_sf(paste0(input_folder, '/onsset/input/Roads/RoadsKEN.shp'))

empl_wealth<-read_sf(paste0(input_folder, '/jrc/wealth_employment/shps/sdr_subnational_data_dhs_2014.shp'))

traveltime <- raster(paste0(input_folder, 'travel.tif'))

traveltime_market = raster(paste0(processed_folder, 'wholesale/traveltime_market.tif'))

#
DepthToGroundwater = read.delim(paste0(input_folder , 'DepthToGroundwater/xyzASCII_dtwmap_v1.txt'), sep='\t')
GroundwaterStorage = read.delim(paste0(input_folder , 'GroundwaterStorage/xyzASCII_gwstor_v1.txt'), sep='\t')
GroundwaterProductivity = read.delim(paste0(input_folder , 'GroundwaterProductivity/xyzASCII_gwprod_v1.txt'), sep='\t')

#
urbrur <- raster(paste0(input_folder , 'GHSL_settlement_type.tif'))

#
raster_tiers = raster(paste0(input_folder , 'tiersofaccess_SSA_2018.nc'))

#
population <- raster(paste0(input_folder, "GHS_POP_E2015_GLOBE_R2019A_4326_30ss_V1_0.tif"))

population <- rgis::mask_raster_to_polygon(population, gadm0)

#
dhs = read_sf(paste0(db_folder , '_SSA/statcompiler_subnational_data_2020-03-17/shps/sdr_subnational_data_dhs_2015.shp'))

# Classifying schools and healthcare facilities
health = read_xlsx(paste0(health_edu_folder , "GeoHealth Data.xlsx"))

# Extract coordinates from csv file of healthcare facilities
health$Y = as.numeric(gsub("[^0-9.-]", "", (sub("\\,.*", "", health$Geolocation))))
health$X = as.numeric(gsub("[^0-9.-]", "", (sub(".*,", "", health$Geolocation))))

# Keep only operational facilities
health = subset(health, (health$OperationalStatus == 'Operational') | (health$OperationalStatus == "Pending Opening"))

# Classify healthcare facilities into 5 tiers
health$heal_type1 = ifelse(health$Type == 'Dispensary', 1, 0)
health$heal_type2 = ifelse((health$Type=='Medical Clinic') | (health$Type == 'Dental Clinic') | (health$Type == 'Eye Centre') |  (health$Type == 'Laboratory (Stand-alone)') | (health$Type == 'Medical Centre') | (health$Type == 'Radiology Unit') |  (health$Type == 'Regional Blood Tranclustersusion Centre') | (health$Type=='Health Centre') | (health$Type=='Maternity Home') | (health$Type=='Nursing Home') | (health$Type=='VCT Centre') | (health$Type=='Health Programme') | (health$Type=='Health Project') |  (health$Type=='Rural Health Training Centre') | (health$Type=='Training Institution in Health (Stand-alone)'), 1, 0)
health$heal_type3 = ifelse((health$Type=='Other Hospital') | (health$Type=='Sub-District Hospital'), 1, 0)
health$heal_type4 = ifelse((health$Type=='District Hospital') |  (health$Type=='Provincial General Hospital') , 1, 0)
health$heal_type5 = ifelse((health$Type=='National Referral Hospital'), 1, 0)

# Calculate number of beds and cots of each tier in each cluster
health$beds_1 = ifelse(health$heal_type1== 1, health$Beds + health$Cots, 0)
health$beds_2 = ifelse(health$heal_type2== 1, health$Beds + health$Cots, 0)
health$beds_3 = ifelse(health$heal_type3== 1, health$Beds + health$Cots, 0)
health$beds_4 = ifelse(health$heal_type4== 1, health$Beds + health$Cots, 0)
health$beds_5 = ifelse(health$heal_type5== 1, health$Beds + health$Cots, 0)

# In any case the dispensary counts as one bed
health$beds_1 = ifelse((health$beds_1==0) & (health$heal_type1== 1), 1, health$beds_1)

#Fill empty fields with average number of beds of the category
health$beds_1 = ifelse(is.na(health$beds_1), 1, health$beds_1)
health$beds_2 = ifelse(is.na(health$beds_2), 45, health$beds_2)
health$beds_3 = ifelse(is.na(health$beds_3), 150, health$beds_3)
health$beds_4 = ifelse(is.na(health$beds_4), 450, health$beds_4)
health$beds_5 = ifelse(is.na(health$beds_5), 2000, health$beds_5)

# #Keep only hospitals with valid coordinates
health = filter(health, !is.na(health$X))

# #Convert to a spatial dataframe using coordinates
healthcarefacilities = st_as_sf(health, coords = c("X", "Y"), crs=4326)

#Import primaryschools
primaryschools = read_sf(paste0(health_edu_folder , 'Kenya_Open_Data_Initiative_KODI_Primary_Schools.shp'))

# Classify primaryschools using total enrollment as a proxy for their tier
primaryschools$sch_type1 = ifelse((primaryschools$TotalEnrol > 0) & (primaryschools$TotalEnrol <= 50), 1, 0)      #method to be confirmed
primaryschools$sch_type2 = ifelse((primaryschools$TotalEnrol > 50) & (primaryschools$TotalEnrol <= 150) , 1, 0)     #method to be confirmed
primaryschools$sch_type3 = ifelse((primaryschools$TotalEnrol > 150) & (primaryschools$TotalEnrol <= 300), 1, 0)     #method to be confirmed
primaryschools$sch_type4 = ifelse((primaryschools$TotalEnrol > 300) & (primaryschools$TotalEnrol <= 600) , 1, 0)    #method to be confirmed
primaryschools$sch_type5 = ifelse((primaryschools$TotalEnrol > 600)         , 1, 0)                             #method to be confirmed

primaryschools$pupils_1 = ifelse(primaryschools$sch_type1== 1, primaryschools$TotalEnrol, 0)
primaryschools$pupils_2 = ifelse(primaryschools$sch_type2== 1, primaryschools$TotalEnrol, 0)
primaryschools$pupils_3 = ifelse(primaryschools$sch_type3== 1, primaryschools$TotalEnrol, 0)
primaryschools$pupils_4 = ifelse(primaryschools$sch_type4== 1, primaryschools$TotalEnrol, 0)
primaryschools$pupils_5 = ifelse(primaryschools$sch_type5== 1, primaryschools$TotalEnrol, 0)

primaryschools$pupils_1 = ifelse(primaryschools$pupils_1== 0, 50, primaryschools$pupils_1)
primaryschools$pupils_2 = ifelse(primaryschools$pupils_2== 0, 100, primaryschools$pupils_2)
primaryschools$pupils_3 = ifelse(primaryschools$pupils_3== 0, 225, primaryschools$pupils_3)
primaryschools$pupils_4 = ifelse(primaryschools$pupils_4== 0, 450, primaryschools$pupils_4)
primaryschools$pupils_5 = ifelse(primaryschools$pupils_5== 0, 700, primaryschools$pupils_5)

#####################
# Assumed load curves
#####################

# crop processing
load_curve_cp = c(0, 0, 0, 0, 0, 0, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0, 0, 0, 0, 0, 0)

# irrigation
load_curve_irrig = c(0, 0, 0, 0, 0, 0.166, 0.166, 0.166, 0.166, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.166, 0.166)
load_curve_irr = load_curve_irrig

# import load curve of productive activities
load_curve_prod_act <- read.csv(paste0(input_folder, 'productive profile.csv'))
