# PrElGen (Productive uses Electricity demand Generator) - Economic Analysis
# Version: 24/04/2020
# This script can only be run after the electrification analysis has been carried out

clusters = QgsVectorLayer(home_repo_folder + 'clusters_final.gpkg',"","ogr")

# Merge PrElGen output with the key results of the electrification analysis
results_csv = home_repo_folder + 'onsset/results/ke-1-0_1_0_0_1_0.csv'
columns = pandas.read_csv(results_csv).columns.values

processing.run("native:joinattributestable", {
        'INPUT': clusters, 'FIELD': 'id',
        'INPUT_2': results_csv,
        'FIELD_2': 'id', 'FIELDS_TO_COPY': columns, 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_21_b.gpkg'})


clusters = QgsVectorLayer(processed_folder + 'clusters_21_b.gpkg',"","ogr")

# Import all Yield (kg/ha) cropland layers (Default datasets used: MapSPAM)
# NB: when using MapSPAM use harvested area, which accounts for multiple growing seasons per year)
rast_path = spam_folder + 'spam2010v1r0_global_yield.geotiff'
rasters_rainfed = glob.glob(os.path.join(rast_path, "spam2010*_r.tif"))

# Import all Yield (kg/ha) cropland layers (Default datasets used: MapSPAM)
rast_path = spam_folder + 'spam2010v1r0_global_yield.geotiff'
rasters_irrigated = glob.glob(os.path.join(rast_path, "spam2010*_i.tif"))

# 1) Estimate the yield gap
#Calculate zonal statistics for each crop for yield in rainfed areas
for data_path in rasters_rainfed:
    fileInfo = QFileInfo(data_path)
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    croptype = QgsRasterLayer(path, baseName)
    print('processing ', baseName)
    processing.run('gdal:rastercalculator', {'INPUT_A' : croptype, 'BAND_A' : 1, 'FORMULA' : '(A/(A>0))', 'OUTPUT' : processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'r.tif'})
    croptype = QgsRasterLayer(processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'r.tif')
    processing.run("qgis:zonalstatistics", {'INPUT_RASTER': croptype, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,'COLUMN_PREFIX': str('YR' + baseName[26:-2]), 'STATS': [2]})


climatezones = QgsRasterLayer(input_folder + 'GAEZ_climatezones.tif')
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': climatezones, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,'COLUMN_PREFIX':'climatezones', 'STATS': [9]})

# Extract the average pixel value of pixels for irrigated and rainfed agriculture in each GAEZ climatezone for each crop according to MapSPAM values, and substract them
# Calculate statistics (rainfed)
for data_path in rasters_rainfed:
    fileInfo = QFileInfo(data_path)
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    croptype = QgsRasterLayer(path, baseName)
    processing.run('gdal:rastercalculator', {'INPUT_A': croptype, 'BAND_A' : 1, 'FORMULA' : '(A/(A>0))', 'OUTPUT': processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'r.tif'})
    croptype = QgsRasterLayer(processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'r.tif')
    processing.run("native:rasterlayerzonalstats", {'INPUT':croptype,'BAND':1,'ZONES': climatezones,'ZONES_BAND':1,'REF_LAYER':0,'OUTPUT_TABLE':processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'r.csv'})

# Calculate statistics (irrigated)
for data_path in rasters_irrigated:
    fileInfo = QFileInfo(data_path)
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    croptype = QgsRasterLayer(path, baseName)
    processing.run('gdal:rastercalculator', {'INPUT_A' : croptype, 'BAND_A' : 1, 'FORMULA' : '(A/(A>0))', 'OUTPUT' : processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'i.tif'})
    croptype = QgsRasterLayer(processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'i.tif')
    processing.run("native:rasterlayerzonalstats", {'INPUT':croptype,'BAND':1,'ZONES': climatezones,'ZONES_BAND':1,'REF_LAYER':0,'OUTPUT_TABLE':processed_folder + 'cropstats/' + str(baseName[26:-1]) + 'i.csv'})

# Process the statistics
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_econ.csv', 'CP1250', clusters.crs(), 'CSV')
clusters = pandas.read_csv(processed_folder + 'clusters_econ.csv')

os.chdir(processed_folder + 'cropstats')
files = glob.glob('./*.csv')

def funmerge(X):
    crop = X[2:6]
    type = X[7:8]
    output = pandas.read_csv(X[2:], encoding = "ISO-8859-1")
    output = output[['zone','min', 'max', 'mean']]
    output["crop"] = crop
    output["type"]= type
    return(output)

df = list(map(funmerge, files))
df = pandas.concat(df)
df = df.round(2)

df = df.sort_values(['zone', 'crop', 'type'], ascending=[True, True, False])

shifted  = df[['min', 'max', 'mean']].shift(1)
shifted = shifted.fillna(0)
df = pandas.concat([df, shifted.rename(columns=lambda x: x+"_lag")], axis=1)

df['min'] = df['min_lag'] - df['min']
df['mean'] = df['mean_lag'] - df['mean']
df['max'] = df['max_lag'] - df['max']

df = df.loc[(df['type'] == 'i')]

df = df.rename(columns={'type':'diff'})

#ifelse yg = negative, then yg = 0 and wr for same crop and clzone = 0
df['min'][df['min'] < 0] = 0
df['max'][df['max'] < 0] = 0
df['mean'][df['mean'] < 0] = 0

# create naming consistent with gyga convention used in Python -> naming convention is
#YDIFF_basename, YR_basename, and YI_basename
df['name'] = "yg_" + df['crop'] + "_" + df['zone'].astype(int).astype(str)

####
# Derive YG by crop by cluster (depending on the climate zone)
crops = df['name'].str.slice(3,7)
crops = crops.unique()

for l in crops:
    print("processing " + l)
    clusters["yg_" + l] = 0
    Pattern1_list = df[df['name'].str.contains("yg_" + l)]
    clzone = Pattern1_list['zone'].astype(int).unique()
    for k in clzone:
        clusters["yg_" + l] = numpy.where(clusters['climatezonesmajority'] == k, clusters["A_" + l +"_sum"]*Pattern1_list.loc[Pattern1_list['zone'] == k, 'mean_lag'], clusters["yg_" + l])
        clusters["yg_" + l] = numpy.where(numpy.isnan(clusters["yg_" + l]), clusters["A_" + l +"_sum"]*Pattern1_list['mean_lag'].mean(), clusters["yg_" + l])

clusters['yg_total'] = clusters[[col for col in clusters if col.startswith('yg_')]].sum(axis=1)

clusters.to_csv(processed_folder + 'clusters_econ_2.csv')

field_to_copy = [col for col in clusters if col.startswith('yg')]

processing.run("native:joinattributestable", {
        'INPUT': processed_folder + 'clusters_21_b.gpkg', 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_econ_2.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': field_to_copy, 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_22.gpkg'})

# 2) Calculate potential economic revenue based on value of crops 
####
# Calculate revenue from new yield (p*new q for each crop)
# but apply constraints of no new revenue if the maximum depth for pumping constraint is not met
# import localprices_layer (usd/kg) (data is referring to 2018 from prices.xlsx in input folder). Also see http://www.nafis.go.ke/

# Process crop prices csv and convert it to a shapefile
prices = pandas.read_csv(input_folder + 'prices_with_coordinates.csv')

prices = geopandas.GeoDataFrame(prices.drop(['X', 'Y'], axis=1),
                            crs={'init': 'epsg:4326'},
                            geometry=[shapely.geometry.Point(xy) for xy in zip(prices.X, prices.Y)])

prices.columns = ['City'] + ['pri_' + str(col) for col in prices.columns[1:43]] +  ['geometry']

prices.to_file(processed_folder + 'prices_with_coordinates.gpkg', driver="GPKG")

# Read the shapefile
localprices = QgsVectorLayer(processed_folder + 'prices_with_coordinates.gpkg', "", "ogr")

clusters = QgsVectorLayer(processed_folder + 'clusters_22.gpkg',"","ogr")

# Merge polygons based on nearest neighbour (i.e. define the local price for each crop)
processing.run('native:joinbynearest', {'INPUT': clusters, 'INPUT_2': localprices,
                                        'OUTPUT': processed_folder + 'clusters_23.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_23.gpkg',"","ogr")

# Sum up to calculate total new local revenue (BENEFIT from YIELD DUE TO IRRIGATION)
# NB: No yield gain possible if distance/depth thresholds to water are not met
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_econ3.csv', 'CP1250', clusters.crs(), 'CSV')
clusters = pandas.read_csv(processed_folder + 'clusters_econ3.csv')

cols = [col for col in clusters.columns if 'pri_' in col]

ygs = [col for col in clusters.columns if 'yg' in col]

from fuzzywuzzy import fuzz
import re
for i in cols:
    mostsimilar = process.extract(i, ygs, limit=1, scorer=fuzz.token_sort_ratio)
    mostsimilar = re.findall(r"'(.*?)'", str(mostsimilar))[0]
    clusters["added_" + i] = clusters[i] * clusters[mostsimilar]

clusters['tt_ddvl'] = clusters[[col for col in clusters if col.startswith('added_')]].sum(axis=1)

clusters.to_csv(processed_folder + 'clusters_econ3.csv')

field_to_copy = ['tt_ddvl']

processing.run("native:joinattributestable", {
        'INPUT': processed_folder + 'clusters_23.gpkg', 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_econ3.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': field_to_copy, 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_24.gpkg'})

# Re-import the layer
clusters = QgsVectorLayer(processed_folder + 'clusters_24.gpkg', "", "ogr")

# 3) Calculate transportation cost for crops
# Formula: TC = 2 * (TTM x fuelcost x lpermin) * n

# Convert traveltime into travelcost based on transportation fuel (diesel) price
#traveltime = QgsRasterLayer(processed_folder + 'wholesale/traveltime_market.tif', "wholesale")
traveltime = QgsRasterLayer(home_repo_folder + 'onsset/input/travel.tif', "wholesale")

diesel = QgsRasterLayer(input_folder + 'diesel_price_baseline_countryspecific.tif', "diesel")

# Zonals for traveltime to market and diesel
processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': traveltime, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'wholesale', 'STATS': [2]}, feedback=f)

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': diesel, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'diesel_pri', 'STATS': [2]}, feedback=f)

QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_econ4.csv', 'CP1250', clusters.crs(), 'CSV')
clusters = pandas.read_csv(processed_folder + 'clusters_econ4.csv')

# impose limit travel time to market 
clusters['remote_from_market'] = numpy.where(clusters['wholesalemean']>360, 1, 0)
clusters['wholesalemean']= numpy.where(clusters['remote_from_market']==1, 0, clusters['wholesalemean'])

clusters['transp_costs'] = 2 * (clusters['wholesalemean']*fuel_consumption*clusters['diesel_primean']) * (clusters['yg_total']/1000/truck_bearing_t)

# lack of market access makes the gains unprofitable
clusters['tt_ddvl'] = numpy.where(clusters['remote_from_market']==1, 0, clusters['tt_ddvl'] )

# 4) Calculate cost for purchasing household appliances (for both new electrified and tier shift households)
clusters['appliances_cost'] = numpy.where(clusters['isurbanmajority'] ==1, (urb1_app_cost * clusters['HHs'] * clusters['acc_pop_share_t1_new'] + urb2_app_cost * clusters['HHs'] * clusters['acc_pop_share_t2_new'] + urb3_app_cost * clusters['HHs'] * clusters['acc_pop_share_t3_new'] + urb4_app_cost * clusters['HHs'] * clusters['acc_pop_share_t4_new']),(rur1_app_cost * clusters['HHs'] * clusters['acc_pop_share_t1_new'] + rur2_app_cost * clusters['HHs'] * clusters['acc_pop_share_t2_new'] + rur3_app_cost * clusters['HHs'] * clusters['acc_pop_share_t3_new'] + rur4_app_cost * clusters['HHs'] *  clusters['acc_pop_share_t4_new']))

# 5) Model cost of groundwater pump 
# 5.1. estimate the cost curve that links hydraulic head H_i and the pumping capacity required Q_i based on the meta-analysis of the costs of groundwater development projects in Sub-Saharan Africa carried out in  Xenarios and Pavelic (2013).

subprocess.call(['"C:/Programmi/R/R-3.5.1/bin/Rscript', '--vanilla', home_repo_folder + 'groundwater_pumps_costs.r"'])

# 5.2 estimate the total cost of pumps in each cluster based on q and h

mean_q_pump = 0.002500002 # 9 m3/h
SD = 0.002047534
Q1 = mean_q_pump - 0.675 * SD
Q3 = mean_q_pump + 0.675 * SD


clusters['q_sust'] = clusters[[col for col in clusters if col.startswith('q_sust')]].max(axis=1)

clusters['n_pumps_Q1'] = (0.33 * clusters['q_sust'])/Q1
clusters['n_pumps_M'] = (0.33 * clusters['q_sust'])/mean_q_pump
clusters['n_pumps_Q3'] = (0.33 * clusters['q_sust'])/Q3

clusters['TC_pumping'] = ((clusters['gr_wat_depth_mean'] * 228.1071)  + (Q1*823975) + (-21312.3*Q1*clusters['gr_wat_depth_mean']) -223.0523)*clusters['n_pumps_Q1'] + ((clusters['gr_wat_depth_mean'] * 228.1071)  + (Q3*823975) + (-21312.3*Q3*clusters['gr_wat_depth_mean']) -223.0523)*clusters['n_pumps_Q3'] + ((clusters['gr_wat_depth_mean'] * 228.1071)  + (mean_q_pump*823975) + (-21312.3*mean_q_pump*clusters['gr_wat_depth_mean']) -223.0523)*clusters['n_pumps_M']

# 6) Cost of purchasing healthcare and education appliances
#clusters['hc_appliances_cost'] = clusters['tier1'] * hc_1_app_cost + clusters['tier2'] * hc_2_app_cost + clusters['tier34']* 0.6 * hc_3_app_cost + clusters['tier34'] * 0.3 * hc_4_app_cost + clusters['tier34'] * 0.1 * hc_5_app_cost

#clusters.rename(columns={'sch_type1.tifsum':'sch_type1'}, inplace=True)
#clusters.rename(columns={'sch_type2.tifsum':'sch_type2'}, inplace=True)
#clusters.rename(columns={'sch_type3.tifsum':'sch_type3'}, inplace=True)
#clusters.rename(columns={'sch_type4.tifsum':'sch_type4'}, inplace=True)
#clusters.rename(columns={'sch_type5.tifsum':'sch_type5'}, inplace=True)
#
#clusters['sch_appliances_cost'] = clusters['sch_type1'] * sch_1_app_cost + clusters['sch_type2'] * sch_2_app_cost + clusters['sch_type3'] * sch_3_app_cost + clusters['sch_type4'] * sch_4_app_cost + clusters['sch_type5'] * sch_5_app_cost
#
# 7) Cost of crop processing
# Define average processing costs for each crop:
# FC_unit = machinery (with a certain processing capacity)
# VC = power consumption + operation and maintaniance 
# FC_percropi = (yield_i / capacity_machine_i)*FC_i
# VC_percropi = FC_percropi*0.1 + ...
# TC = sum(FC_percropi+VC_percropi)

# Import csv of machines cost and processing capacity


# Make calculations
#clusters['processing_cost'] = 

# 8) Net agricoltural profit
clusters['tt_ddvl'] = numpy.where(clusters['transp_costs']>clusters['tt_ddvl'], 0, clusters['tt_ddvl'] )
clusters['transp_costs'] = numpy.where(clusters['transp_costs']>clusters['tt_ddvl'], 0, clusters['transp_costs'] )

lifetimepump = 20
discount_rate = 0.15

clusters['profit_yearly'] = clusters['tt_ddvl'] - clusters['transp_costs'] - clusters['TC_pumping']/(1+discount_rate)**lifetimepump 
clusters['profit_yearly'] = numpy.where(clusters['profit_yearly']<0, 0, clusters['profit_yearly'])
clusters['investmentreq'] = clusters['InvestmentCost2025'] + clusters['InvestmentCost2030']

# 9) Paybacktime of electrification in each cluster
clusters['PBT'] = clusters['investmentreq'] / clusters['profit_yearly']

# print share of pop without access with PBT < 5 years
clusters['noaccsum'][clusters.PBT < 5].sum()  
clusters['noaccsum'][clusters.PBT < 5].sum()  / clusters['noaccsum'].sum()

clusters.to_csv(processed_folder + 'clusters_econ4.csv')

field_to_copy = ['transp_costs', 'TC_pumping', 'profit_yearly']

processing.run("native:joinattributestable", {
        'INPUT': processed_folder + 'clusters_24.gpkg', 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_econ4.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': field_to_copy, 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_econ_results.gpkg'})


##########
#Plots generation

subprocess.call(['"C:/Program Files/R/R-3.5.1/bin/Rscript', '--vanilla', home_repo_folder + 'plots.r"'])
