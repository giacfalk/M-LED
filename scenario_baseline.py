<<<<<<< HEAD
#Scenario_baseline 

####
# Country parameters
countryiso3 = 'KEN' # ISO3
national_official_population = 52000000 # number of people # REF:
national_official_elrate = 0.74 # national electricity access rate
national_official_population_without_access = national_official_population- (national_official_population*national_official_elrate) # number of people without access

# Planning horizon parameters
today = 2020
planning_year = 2030
planning_horizon = planning_year - today

# Pump technical parameters
rho = 1000 # density of water (1000 kg / m3)
g = 9.81 # gravitational constant (m / s2)
c = 3.6 * (10**6) # differential pressure, (Pa)

#Threshold parameters
threshold_surfacewater_distance = 5000 # (m): distance threshold which discriminates if groundwater pumping is necessary or a surface pump is enough # REF:
threshold_groundwater_pumping = 150 # (m): maximum depth at which the model allows for water pumping: beyond it, no chance to install the pump # REF:

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

## Demand per tier per household type (kWh/year)
#rur1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_1.csv')).iloc[:,1].sum(axis=0)/60000/100
#rur2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_2.csv')).iloc[:,1].sum(axis=0)/60000/100
#rur3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_3.csv')).iloc[:,1].sum(axis=0)/60000/100
#rur4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000/100
#rur5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_5.csv')).iloc[:,1].sum(axis=0)/60000/100
#
#urb1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_6.csv')).iloc[:,1].sum(axis=0)/60000/100
#urb2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_7.csv')).iloc[:,1].sum(axis=0)/60000/100
#urb3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_8.csv')).iloc[:,1].sum(axis=0)/60000/100
#urb4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_9.csv')).iloc[:,1].sum(axis=0)/60000/100
#urb5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_10.csv')).iloc[:,1].sum(axis=0)/60000/100
#
## define consumption of facility types (kWh/facility/year)
#health1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_1.csv')).iloc[:,1].sum(axis=0)/60000
#health2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_2.csv')).iloc[:,1].sum(axis=0)/60000
#health3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_3.csv')).iloc[:,1].sum(axis=0)/60000
#health4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
#health5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_5.csv')).iloc[:,1].sum(axis=0)/60000
#
## edu1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_6.csv')).iloc[:,1].sum(axis=0)/60000
## edu2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_7.csv')).iloc[:,1].sum(axis=0)/60000
## edu3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_8.csv')).iloc[:,1].sum(axis=0)/60000
## edu4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_9.csv')).iloc[:,1].sum(axis=0)/60000
## edu5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_10.csv')).iloc[:,1].sum(axis=0)/60000
#
#edu1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
#edu2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
#edu3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
#edu4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
#edu5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/OLD - NS Before Field Campaign/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
#

# General economic parameters
discount_rate = 0.15 # REF:

# Transportation costs
fuel_consumption = 15 # (l/h) # REF: OnSSET
fuel_cost = 1 # (USD/l) # baseline, then adapted based on distance to city
truck_bearing_t = 15 # (tons) # REF: https://en.wikipedia.org/wiki/Dump_truck

#Pumo economic parameters
LCOE_for_pumping = 0.08 # USD/kWh # REF:
lifetimepump = 30

# import local crop prices csv.  Structure: X, Y, City, cropname1, cropname 2, ...
prices = pandas.read_excel(input_folder + "prices.xls")

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

# Water demand scenario
water_demand_LPJmL_scenario = QgsRasterLayer(home_repo_folder + 'image/water_demand/mirrig.nc')
=======
#Scenario_baseline 

####
# Country parameters
countryiso3 = 'KEN' # ISO3
national_official_population = 52000000 # number of people # REF:
national_official_elrate = 0.74 # national electricity access rate
national_official_population_without_access = national_official_population- (national_official_population*national_official_elrate) # number of people without access

# Planning horizon parameters
today = 2020
planning_year = 2030
planning_horizon = planning_year - today

# Pump technical parameters
rho = 1000 # density of water (1000 kg / m3)
g = 9.81 # gravitational constant (m / s2)
c = 3.6 * (10**6) # differential pressure, (Pa)

#Threshold parameters
threshold_surfacewater_distance = 5000 # (m): distance threshold which discriminates if groundwater pumping is necessary or a surface pump is enough # REF:
threshold_groundwater_pumping = 150 # (m): maximum depth at which the model allows for water pumping: beyond it, no chance to install the pump # REF:

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

# Demand per tier per household type (kWh/year)
rur1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_1.csv')).iloc[:,1].sum(axis=0)/60000/100
rur2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_2.csv')).iloc[:,1].sum(axis=0)/60000/100
rur3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_3.csv')).iloc[:,1].sum(axis=0)/60000/100
rur4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000/100
rur5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_5.csv')).iloc[:,1].sum(axis=0)/60000/100

urb1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_6.csv')).iloc[:,1].sum(axis=0)/60000/100
urb2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_7.csv')).iloc[:,1].sum(axis=0)/60000/100
urb3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_8.csv')).iloc[:,1].sum(axis=0)/60000/100
urb4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_9.csv')).iloc[:,1].sum(axis=0)/60000/100
urb5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/results/output_file_10.csv')).iloc[:,1].sum(axis=0)/60000/100

# define consumption of facility types (kWh/facility/year)
health1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_1.csv')).iloc[:,1].sum(axis=0)/60000
health2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_2.csv')).iloc[:,1].sum(axis=0)/60000
health3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_3.csv')).iloc[:,1].sum(axis=0)/60000
#health4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
#health5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_5.csv')).iloc[:,1].sum(axis=0)/60000

health4 =12.27843163
health5 =12.27843163

# edu1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_6.csv')).iloc[:,1].sum(axis=0)/60000
# edu2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_7.csv')).iloc[:,1].sum(axis=0)/60000
# edu3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_8.csv')).iloc[:,1].sum(axis=0)/60000
# edu4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_9.csv')).iloc[:,1].sum(axis=0)/60000
# edu5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_10.csv')).iloc[:,1].sum(axis=0)/60000

edu1 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
edu2 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
edu3 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
edu4 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000
edu5 = (pandas.read_csv(home_repo_folder + 'ramp/RAMP_social/results/output_file_4.csv')).iloc[:,1].sum(axis=0)/60000


# General economic parameters
discount_rate = 0.15 # REF:

# Transportation costs
fuel_consumption = 15 # (l/h) # REF: OnSSET
fuel_cost = 1 # (USD/l) # baseline, then adapted based on distance to city
truck_bearing_t = 15 # (tons) # REF: https://en.wikipedia.org/wiki/Dump_truck

#Pumo economic parameters
LCOE_for_pumping = 0.08 # USD/kWh # REF:
lifetimepump = 30

# import local crop prices csv.  Structure: X, Y, City, cropname1, cropname 2, ...
prices = pandas.read_excel(input_folder + "prices.xls")

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

# Water demand scenario
water_demand_LPJmL_scenario = QgsRasterLayer(home_repo_folder + 'image/water_demand/mirrig.nc')
>>>>>>> bd368406b6772c89dcd5cc8ec865ee33c5860ea4
