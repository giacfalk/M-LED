#Scenario_baseline 

####
# Country parameters
countryiso3 = 'MOZ' # ISO3
national_official_population = 30400000 # number of people # REF:
national_official_elrate = 0.31 # national electricity access rate
national_official_population_without_access = national_official_population- (national_official_population*national_official_elrate) # number of people without access

# Planning horizon parameters
today = 2020
planning_year = 2030
planning_horizon = planning_year - today

# Pump technical parameters
rho = 1000 # density of water (1000 kg / m3)
g = 9.81 # gravitational constant (m / s2)
c = 3.6 * (10^6) # differential pressure, (Pa)

#Threshold parameters
threshold_surfacewater_distance = 5000 # (m): distance threshold which discriminates if groundwater pumping is necessary or a surface pump is enough # REF:
threshold_groundwater_pumping = 15 # (m): maximum depth at which the model allows for water pumping: beyond it, no chance to install the pump # REF:

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

#number of hours of pumping, 3 during the morning and 3 during the evening
nhours_irr = 6
eta_pump = 0.75

discount_rate = 0.15 # 

# Transportation costs
fuel_consumption = 15 # (l/h) # REF: OnSSET
fuel_cost = 1 # (USD/l) # baseline, then adapted based on distance to city
truck_bearing_t = 15 # (tons) # REF: https://en.wikipedia.org/wiki/Dump_truck

#Pumo economic parameters
LCOE_for_pumping = 0.08 # USD/kWh # REF:
lifetimepump = 30

# import local crop prices csv.  Structure: X, Y, City, cropname1, cropname 2, ...
#prices = readxl::read_xlsx(paste0(input_folder , "prices.xls"))

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

#

########
# Define main input files #

# Country and provinces shapefiles
gadm0 = read_sf("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Applications/GISele_MLED_link/mozambique/Namajavira_4326.shp")

# Population (Default dataset used: HRSL, 30m)
population = raster("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Applications/GISele_MLED_link/mozambique/population_moz_2019-07-01.tif")

# Import cropland extent (Default dataset used: GFSAD30CE)
cropland_extent = raster("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Applications/GISele_MLED_link/mozambique/GFSAD30AFCE_2015_S20E30_001_2017261090100.tif")

# Import climatezones (Default datasets used: GAEZ soil classes)
climatezones = raster(paste0(input_folder , 'GAEZ_climatezones.tif'))

# Import surface water basins layer (Default datasets used: Global Surface Water Explorer)
categories_surface_water = raster(paste0(input_folder , 'transitions.tif'))

# Import diesel price layer (In each pixel: 2015 prices baseline , cost per transporting it from large cities)
diesel_price = raster(paste0(input_folder , 'diesel_price_baseline_countryspecific.tif'))

#
crops = readxl::read_xlsx(paste0(input_folder , 'crops_cfs_ndays_months.xlsx'))

# Define extent of country analysed
ext = extent(gadm0)

#source(noaccesspopulation.R)

clusters = read_sf("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Applications/GISele_MLED_link/mozambique/Namajavira_clusters.shp")

#clusters = read_sf("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Manuscript/First paper/Revision_1/mg_sites_2_5km.gpkg")

popnoaccess2018 = raster(paste0(processed_folder , 'noaccess/pop18_noaccess_kenya.tif'))
population = raster("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Applications/GISele_MLED_link/mozambique/population_moz_2019-07-01.tif")

clusters$pop <- exactextractr::exact_extract(population, clusters, fun="sum")
clusters$noacc <- exactextractr::exact_extract(popnoaccess2018, clusters, fun="sum")

# adjust
somma = sum(clusters$pop)
spread = ((national_official_population-somma)/somma)

print(spread)

clusters$pop <- clusters$pop * 1+spread

somma = sum(clusters$noacc)
spread = (((national_official_population*(1-national_official_elrate))-somma)/somma)

print(spread)

clusters$noacc <- clusters$noacc * 1+spread

clusters$elrate <- 1- (clusters$noacc/clusters$pop)

