# PrElGen (Productive uses Electricity demand Generator) v0.1 - Electricity Demand Generation
# Hourly resolution
# Version: 20/05/2020

####
# Define the working directory
import os
os.chdir('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/')

# Import the manual_parameters, to be set before running this script
#from manual_parameters import *
    
# Load the required libraries
#from backend import *

# Select the scenario to be operated
#scenario = input('What is the name of the scenario (matching a .py file in your PrElGen folder) you want to implement?')
#import importlib
#importlib.import_module(scenario)

########
# Define main input files #

# Country and provinces shapefiles
gadm0 = QgsVectorLayer(input_folder + 'gadm36_' + countryiso3 + '_0.shp',"","ogr")
gadm1 = QgsVectorLayer(input_folder + 'gadm36_' + countryiso3 + '_1.shp',"","ogr")
gadm2 = QgsVectorLayer(input_folder + 'gadm36_' + countryiso3 + '_2.shp',"","ogr")
gadm3 = QgsVectorLayer(input_folder + 'gadm36_' + countryiso3 + '_3.shp',"","ogr")

# Population (Default dataset used: HRSL, 30m)
population = QgsRasterLayer(input_folder + 'Population.tif')

# Import cropland extent (Default dataset used: GFSAD30CE)
cropland_extent = QgsRasterLayer(input_folder + 'Croplands_GFSAD30AFCE.tif', "cropland_extent")

# Import climatezones (Default datasets used: GAEZ soil classes)
climatezones = QgsRasterLayer(input_folder + 'GAEZ_climatezones.tif')

# Import surface water basins layer (Default datasets used: Global Surface Water Explorer)
categories_surface_water = QgsRasterLayer(input_folder + 'transitions.tif')

# Import diesel price layer (In each pixel: 2015 prices baseline + cost per transporting it from large cities)
diesel_price = QgsRasterLayer(input_folder + 'diesel_price_baseline_countryspecific.tif', "diesel_price")

# Define extent of country analysed
ext = gadm0.extent()
xmin = ext.xMinimum() - 1
xmax = ext.xMaximum() + 1
ymin = ext.yMinimum() - 1
ymax = ext.yMaximum() + 1
coords = '{},{},{},{}'.format(xmin, xmax, ymin, ymax)

# These functions automatically interface with Google Earth Engine to create the population and no-access population rasters
#import noaccesspopulation

#Start timer to keep track
then = time.time()

###
# Select unit of aggregation for the database processing
#aggregation = input('What unit of aggregation to use? clustering_plugin, adm_boundaries, fishnet, or custom?')
#
#if aggregation == "clustering_plugin":
#    # NB If run over large areas it can take hours! 
#    import clustering_old
#    clusters = QgsVectorLayer(processed_folder + 'voronoi_clipped_repaired.shp', "", "ogr")
#elif aggregation == "adm_boundaries":
#    # Alternatively, use lowest level of administrative boundaries as the default areal unit
#    clusters = gadm3
#elif aggregation == "fishnet":
#    fishnet_resolution = input('What fishnet resolution to use (in degrees) e.g. 0.008333 for about 1km?')
#    processing.run("native:creategrid", {'TYPE':2,'EXTENT':coords + ' [EPSG:4326]','HSPACING':fishnet_resolution,'VSPACING':fishnet_resolution,'HOVERLAY':0,'VOVERLAY':0,'CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'OUTPUT':processed_folder + 'clusters.shp'})
#    clusters = QgsVectorLayer(processed_folder + 'clusters.shp', "", "ogr")
#    processing.run("native:selectbylocation", {'INPUT': clusters,'PREDICATE':[0,6],'INTERSECT':gadm0,'METHOD':0})
#    processing.run("native:saveselectedfeatures", {'INPUT':clusters,'OUTPUT': processed_folder + 'clusters_clipped.shp'})
#    clusters = QgsVectorLayer(processed_folder + 'clusters_clipped.shp', "", "ogr")
#elif aggregation == "custom":
#    custom = input("Exact path to shapefile")
#    clusters = QgsVectorLayer(custom, "", "ogr")
#else:
#    print("Wrong selection!")

#clusters = QgsVectorLayer(home_repo_folder + 'onsset/kenya_clusters/clusters.gpkg', "", "ogr")

#run algorithm of travel-time based clustering
#subprocess.call(['"C:/Programmi/R/R-3.5.1/bin/Rscript', '--vanilla', home_repo_folder + 'traveltime_based_clustering.r'])

clusters = QgsVectorLayer(home_repo_folder + 'onsset/kenya_clusters/clusters_tt_based.gpkg', "", "ogr")

# Add population without access to electricity and electrification level --> Genrated with 30m population in GEE 
#print(f"Estimating electrification levels. Elapsed time:", round((time.time() - then) / 60, 2), " minutes")

#gdd.download_file_from_google_drive(file_id=noacc_gd_id,
#                                    dest_path=processed_folder + 'noaccess/pop18_noaccess_kenya.tif')
#
#gdd.download_file_from_google_drive(file_id=pop_gd_id,
#                                    dest_path=processed_folder + 'noaccess/pop18_kenya.tif')

## Import it
popnoaccess2018 = QgsRasterLayer(processed_folder + 'noaccess/pop18_noaccess_kenya.tif')
population = QgsRasterLayer(processed_folder + 'noaccess/pop18_kenya.tif')

# print(f"Add population to clusters. Elapsed time:", round((time.time() - then) / 60, 2), " minutes")
processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': population, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'pop', 'STATS': [1]}, feedback=f)

# Add noaccess
processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': popnoaccess2018, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'noacc', 'STATS': [1]}, feedback=f)

# Harmonise with national population. To to this, calculate the current total pop found in clusters and obtain the relative difference with national population from official statistics
print(f"Harmonising with national populations and calculating electrification rate. Elapsed time:", round((time.time() - then) / 60, 2), " minutes")
features = clusters.getFeatures()

total = []
idx = clusters.fields().lookupField("popsum")

for feat in features:
    attr = feat.attributes()[idx]
    if attr == NULL:
        continue
    else:
        total.append((int(attr)))

somma = sum(total)
spread = ((national_official_population-somma)/somma)+1
print(spread, f"Share of population included (pre adjustment)")

##Harmonise by homogeneously spreaing the missing population across clusters
processing.run("qgis:fieldcalculator", {'INPUT': clusters, 'FIELD_NAME': 'popsum', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': False, 'FORMULA':'\"popsum\" *' + str(spread), 'OUTPUT': processed_folder + 'clusters_2.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_2.gpkg',"","ogr")

features = clusters.getFeatures()

total = []

for feat in features:
    attr = feat.attributes()[idx]
    if attr == NULL:
        continue
    else:
        total.append((int(attr)))

somma = sum(total)
spread = ((national_official_population-somma)/somma)+1
print(spread, f"Share of population included (after adjustment)", spread)

features = clusters.getFeatures()

total = []
idx = clusters.fields().lookupField("noaccsum")

for feat in features:
    attr = feat.attributes()[idx]
    if attr == NULL:
        continue
    else:
        total.append((int(attr)))

somma = sum(total)
spread = (((national_official_population*(1-national_official_elrate))-somma)/somma)+1
print(spread, f"Share of population without access included (pre adjustment)")

# Harmonise by homogeneously spreaing the missing population without access across clusters
processing.run("qgis:fieldcalculator", {'INPUT': clusters, 'FIELD_NAME': 'noaccsum', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': False, 'FORMULA':'\"noaccsum\" *' + str(spread), 'OUTPUT': processed_folder + 'clusters_3.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_3.gpkg',"","ogr")

features = clusters.getFeatures()

total = []

for feat in features:
    attr = feat.attributes()[idx]
    if attr == NULL:
        continue
    else:
        total.append((int(attr)))

somma = sum(total)
spread = (((national_official_population*(1-national_official_elrate))-somma)/somma)+1
print(spread, f"Share of population without access included (after adjustment)", spread)

# Calculate electrification rate in each cluster
processing.run("qgis:fieldcalculator", {'INPUT': clusters, 'FIELD_NAME': 'elrate', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' 1-(\"noaccsum\" / \"popsum\") ', 'OUTPUT': processed_folder + 'clusters_4.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_4.gpkg',"","ogr")

#%%
# 2) Cropland
print(f"Processing cropland. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")
# print(f"Cropping cropland. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")

# processing.run("gdal:cliprasterbyextent",
               # {'INPUT': cropland_extent, 'PROJWIN': coords,
                # 'DATA_TYPE': 0,
                # 'OUTPUT': processed_folder + 'cropland_cropped.tif', 'NODATA': 0})

# cropland_extent = QgsRasterLayer(processed_folder + 'cropland_cropped.tif', "cropland_extent")

# print(f"Reproject cropland to World Mercator (meters). Elapsed time:",  round((time.time()-then)/60, 2), " minutes")
# processing.run('gdal:warpreproject', {'INPUT' : cropland_extent, 'TARGET_CRS': 'EPSG:3395', 'OUTPUT' : processed_folder + 'cropland_extent_reprojected.tif'})

# Import it
cropland_extent_reprojected = QgsRasterLayer(processed_folder + 'cropland_extent_reprojected.tif')

print(f"Reproject clusters to World Mercator (meters). Elapsed time:",  round((time.time()-then)/60, 2), " minutes")
processing.run('native:reprojectlayer', {'INPUT' : processed_folder + 'clusters_4.gpkg', 'TARGET_CRS': 'EPSG:3395', 'OUTPUT' : processed_folder + 'clusters_5.gpkg'})

# Import them
clusters = QgsVectorLayer(processed_folder + 'clusters_5.gpkg',"","ogr")

print(f"Sum total cropland area within each cluster. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': cropland_extent_reprojected, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': 'cr_ha_', 'STATS': [0]})

# Convert to hectares (ha). NB here 894 = 29.9^2, which is because the pixel resolution is 29.90m.
processing.run("qgis:fieldcalculator", {'INPUT': clusters, 'FIELD_NAME': 'cr_ha_count', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': False, 'FORMULA': ' \"cr_ha_count\" * 894 * 0.0001', 'OUTPUT': processed_folder + 'clusters_6.gpkg'})

# Calculate the total cluster's area in hectares (ha)
processing.run("qgis:fieldcalculator", {'INPUT': processed_folder + 'clusters_6.gpkg', 'FIELD_NAME': 'Area', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' $area * 0.0001', 'OUTPUT': processed_folder + 'clusters_7.gpkg'})

#Create a 'cropland share' attribute in each cluster (% of cropland over total land area)
processing.run("qgis:fieldcalculator", {'INPUT': processed_folder + 'clusters_7.gpkg', 'FIELD_NAME': 'crshare', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' \"cr_ha_count\" / \"Area\"', 'OUTPUT': processed_folder + 'clusters_8.gpkg'})

# Reproject to WGS84
processing.run('native:reprojectlayer', {'INPUT' : processed_folder + 'clusters_8.gpkg', 'TARGET_CRS': 'EPSG:4326', 'OUTPUT' : processed_folder + 'clusters_9.gpkg'})

# Import it
clusters = QgsVectorLayer(processed_folder + 'clusters_9.gpkg',"","ogr")

print(f"Calculate sum of rainfed cropland area (ha) by crop in each cluster. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")

# # Downscale and calculate rainfed cropland area (ha) for each crop in each cluster

# Create a new sequential unique ID per cell raster with same resolution of SPAM (1km)
from rasterio import Affine

out_raster = processed_folder + 'ID_raster.tif'
res = 0.083333
cols = 2160
rows = 4320

ext = gadm0.extent()

xmin = ext.xMinimum() - 1
xmax = ext.xMaximum() + 1
ymin = ext.yMinimum() - 1
ymax = ext.yMaximum() + 1

profile = {
    'driver': 'GTiff',
    'dtype': 'uint32',
    'width': cols,
    'height': rows,
    'count': 1,
    'crs': 'epsg:4326',
    'transform': Affine(res, 0.0, xmin, 0.0, -res, ymax)}

ids = numpy.arange(1, rows*cols+1).reshape(rows, cols).astype(profile['dtype'])

with rasterio.open(out_raster, 'w', **profile) as out:
        out.write(ids, 1)

# Import it
ID_raster = QgsRasterLayer(processed_folder + 'ID_raster.tif')

# Zonal majority of ID field
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': ID_raster, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': 'id_pix_ras_', 'STATS': [9]})

processing.run("qgis:fieldcalculator", {'INPUT': clusters, 'FIELD_NAME': 'id', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' $id', 'OUTPUT': processed_folder + 'clusters_10.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_10.gpkg',"","ogr")

# Create new field crshare
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_2.csv', 'CP1250', clusters.crs(), 'CSV')

clusters = pandas.read_csv(processed_folder + 'clusters_2.csv')
clusters['total_crarea_underneath'] = clusters['cr_ha_count'].groupby(clusters['id_pix_ras_majority']).transform('sum')
clusters['crshare_sp'] =  clusters['cr_ha_count'] / clusters['total_crarea_underneath']
clusters['crshare_sp'] = clusters['crshare_sp'].fillna(0)
clusters.to_csv(processed_folder + 'clusters_2.csv')

processing.run("native:joinattributestable", {
        'INPUT': processed_folder + 'clusters_10.gpkg', 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_2.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['crshare_sp'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_11.gpkg'})

print(f"Downscaling cropland area for each crop to a resolution of 30m. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")

# Zonal and raster calculator for each crop and complete the process with the downscaling (assumption of equal redistribution of cropland for each crop in the cropland area beneath the 1-km resolution ID pixel)
clusters = QgsVectorLayer(processed_folder + 'clusters_11.gpkg')
os.chdir(spam_folder + 'spam2010v1r0_global_harv_area.geotiff')
files = glob.glob('./*r.tif')

for X in files:
    a = "A_" + X[37:41] + "_"
    print('iterating' + a)
    processing.run("qgis:zonalstatistics",
                   {'INPUT_RASTER': X, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                    'COLUMN_PREFIX': a, 'STATS': [1]})

# Downscaling
names = list(map(lambda X: "A_" + X[37:41] + "_sum", files))

for X in names:
    idx = clusters.fields().lookupField(X)
    clusters.startEditing()
    e = QgsExpression('crshare_sp * ' + X)
    c = QgsExpressionContext()
    s = QgsExpressionContextScope()
    s.setFields(clusters.fields())
    c.appendScope(s)
    e.prepare(c)
    for f in clusters.getFeatures():
        c.setFeature(f)
        value = e.evaluate(c)
        atts = {idx: value}
        clusters.dataProvider().changeAttributeValues({f.id(): atts})
    clusters.commitChanges()
    print('iterated' + X)


#%%
# 3) Irrigation water requirements
clusters = QgsVectorLayer(processed_folder + 'clusters_11.gpkg',"","ogr")

# Import and process agro-hydrological data (GAEZ) and quantify water requirements for irrigation in each cluster. Legend of climate zones:
print(f"Define dominant climate zone in each cluster. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': climatezones, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': 'clima_zone', 'STATS': [9]})

print(f"Estimating water and yield gap in each cluster. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")

# List of months in the year
list_months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

# Import PET and extract monthly mean within each cluster
bandnum = 1
pet = QgsRasterLayer(input_folder + "TerraClimate/TerraClimate_pet_2015.nc")

for X in list_months:
    print(X)
    processing.run("qgis:zonalstatistics",
                   {'INPUT_RASTER': pet, 'RASTER_BAND': bandnum, 'INPUT_VECTOR': clusters,
                    'COLUMN_PREFIX': "PET_" + X, 'STATS': [2]})
    bandnum = bandnum + 1
    print(bandnum)

# Import precipitations and extract monthly mean within each cluster
bandnum = 1
ppt = QgsRasterLayer(input_folder + "TerraClimate/TerraClimate_ppt_2015.tif")

for X in list_months:
    print(X)
    processing.run("qgis:zonalstatistics", {'INPUT_RASTER': ppt, 'RASTER_BAND': bandnum, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': "PPT_" + X, 'STATS': [2]})
    bandnum = bandnum + 1

# Import soil moisture and extract monthly mean within each cluster
bandnum = 1
soil = QgsRasterLayer(input_folder + "TerraClimate/TerraClimate_soil_2015.nc")

for X in list_months:
    print(X)
    processing.run("qgis:zonalstatistics", {'INPUT_RASTER': soil, 'RASTER_BAND': bandnum, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': "SOI_" + X, 'STATS': [2]})
    bandnum = bandnum + 1

QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_3.csv', 'CP1250', clusters.crs(), 'CSV')
clusters = pandas.read_csv(processed_folder + 'clusters_3.csv')

### Set up equations to derive total water requirements (WG) per crop per cluster
# Import days per each growing phase (for each crop)
# Import crop factors (for each crop for each growing period)
# Import crop schedule for each crop

crops = pandas.read_excel(input_folder + 'crops_cfs_ndays_months.xlsx')

# Define crop factor for each day of the year based on sum of beginning of growing seasons and length of each growing period
for i in range(0,len(crops), 1):
    print("Processing ", crops.iloc[i,0])
    daily = {'countdays': numpy.arange(1,730)}
    daily = pandas.DataFrame(data=daily)
    daily['date'] = pandas.date_range(datetime.datetime.strptime("01012019", "%d%m%Y"), periods=729)
    daily['month'] = pandas.DatetimeIndex(daily['date']).month
    daily['day'] = pandas.DatetimeIndex(daily['date']).day
    pm1=datetime.datetime.strptime(str(crops['pm_1'].iloc[i]) + "2019", "%d%m%Y")
    pm2=datetime.datetime.strptime(str(crops['pm_2'].iloc[i]) + "2019", "%d%m%Y")
    daily['k_c'] = numpy.where((daily['date']>= pm1) & (daily['date'] < (pm1 + datetime.timedelta(days=int(crops['nd_1'].iloc[i])))), crops['cf_1'].iloc[i], numpy.where((daily['date']>= pm1 + datetime.timedelta(days=int(crops['nd_1'].iloc[i]))) & (daily['date'] < (pm1 + datetime.timedelta(days=int(crops['nd_1'].iloc[i])) + datetime.timedelta(days=int(crops['nd_2'].iloc[i])))), (crops['cf_1'].iloc[i]+crops['cf_2'].iloc[i])/2, numpy.where((daily['date']>= pm1+ datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))) & (daily['date'] < (pm1 + datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_3'].iloc[i])))), (crops['cf_2'].iloc[i]+crops['cf_3'].iloc[i])/2, numpy.where((daily['date']>= pm1+ datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_3'].iloc[i]))) & (daily['date'] < (pm1 + datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_3'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_4'].iloc[i])))), crops['cf_3'].iloc[i],0))))# Calculate daily crop evapotraspiration (ETc) in each cluster         
    daily['k_c2'] = numpy.where((daily['date']>= pm2) & (daily['date'] < (pm2 + datetime.timedelta(days=int(crops['nd_1'].iloc[i])))), crops['cf_1'].iloc[i], numpy.where((daily['date']>= pm2 + datetime.timedelta(days=int(crops['nd_1'].iloc[i]))) & (daily['date'] < (pm2 + datetime.timedelta(days=int(crops['nd_1'].iloc[i])) + datetime.timedelta(days=int(crops['nd_2'].iloc[i])))), (crops['cf_1'].iloc[i]+crops['cf_2'].iloc[i])/2, numpy.where((daily['date']>= pm2+ datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))) & (daily['date'] < (pm2 + datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_3'].iloc[i])))), (crops['cf_2'].iloc[i]+crops['cf_3'].iloc[i])/2, numpy.where((daily['date']>= pm2+ datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_3'].iloc[i]))) & (daily['date'] < (pm2 + datetime.timedelta(days=int(crops['nd_1'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_2'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_3'].iloc[i]))+ datetime.timedelta(days=int(crops['nd_4'].iloc[i])))), crops['cf_3'].iloc[i],0))))# Calculate daily crop evapotraspiration (ETc) in each cluster (second plantation)  
    daily['k_c'] = daily[["k_c", "k_c2"]].max(axis=1)
    #group by day and month and take max value
    daily = daily.groupby(['month', 'day']).max().reset_index()
    daily['date'] = pandas.date_range(datetime.datetime.strptime("01012019", "%d%m%Y"), periods=366)
    for k in range(1,366, 1):
        clusters["ET_" + crops.iloc[i,0] + "_" + str(daily.iloc[k,0]) + "_" + str(daily.iloc[k,1])] = daily['k_c'].iloc[k] * clusters['PET_' + str(numpy.where(len(str(daily['month'].iloc[k])) == 1, "0" + str(daily['month'].iloc[k]), str(daily['month'].iloc[k]))) +"mean"]/30

# Summarise ETc by month by crop
for i in range(0,len(crops), 1):  
    for z in range(1,13, 1):
        print(z)
        clusters['monthly_ET_' + str(crops.iloc[i,0]) + "_" + str(z)] = clusters[[col for col in clusters if col.startswith('ET_' + crops.iloc[i,0] + "_" + str(z) + '_')]].sum(axis=1)
        #Convert ET to total m3 per cluster per month per crop
        clusters['monthly_ET_' + str(crops.iloc[i,0]) + "_" + str(z)] = clusters["A_" + str(crops.iloc[i,0]) + "_sum"] * clusters['monthly_ET_' + str(crops.iloc[i,0]) + "_" + str(z)]* 10
        # Absorption efficiency (share of water that roots are able to extract from soil)
        eta = 0.6
        #Convert PPT to total m3 per cluster per month per crop
        clusters['monthly_PPT_' + str(crops.iloc[i,0]) + "_" + str(z)] = clusters['PPT_' + str(numpy.where(len(str(z)) == 1, "0" + str(z), str(z))) + "mean"] * eta * 10 * clusters["A_" + str(crops.iloc[i,0]) + "_sum"]
        #Calculate irrigation requirement per cluster per month per crop in m3 considering different irrigation efficiency per each crop 
        clusters['monthly_IRREQ_' + str(crops.iloc[i,0]) + "_" + str(z)] = ((clusters['monthly_ET_' + str(crops.iloc[i,0]) + "_" + str(z)]) - (clusters['monthly_PPT_' + str(crops.iloc[i,0]) + "_" + str(z)])) / crops['eta_irr'].iloc[i]
        clusters['monthly_IRREQ_' + str(crops.iloc[i,0]) + "_" + str(z)] = numpy.where(clusters['monthly_IRREQ_' + str(crops.iloc[i,0]) + "_" + str(z)]<0, 0, clusters['monthly_IRREQ_' + str(crops.iloc[i,0]) + "_" + str(z)])

# Obtain total yearly WG per cluster (in m3)
clusters['IRREQ_year'] = clusters[[col for col in clusters if col.startswith("monthly_IRREQ_")]].sum(axis=1)

for z in range(1,13, 1):
    a = clusters[[col for col in clusters if col.startswith('monthly_IRREQ_')]]
    a2 = a[[col for col in a if col.endswith('_' + str(z))]]
    clusters['monthly_IRREQ' + "_" + str(z)] = a2.sum(axis=1)

# Write results
clusters.to_csv(processed_folder + 'clusters_4.csv')

# Import and merge
fields_to_copy =  ['IRREQ_year', 'monthly_IRREQ_1', 'monthly_IRREQ_2','monthly_IRREQ_3','monthly_IRREQ_4','monthly_IRREQ_5','monthly_IRREQ_6','monthly_IRREQ_7','monthly_IRREQ_8','monthly_IRREQ_9','monthly_IRREQ_10','monthly_IRREQ_11','monthly_IRREQ_12']

processing.run("native:joinattributestable", {
        'INPUT': processed_folder + 'clusters_11.gpkg', 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_4.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': fields_to_copy, 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_12.gpkg'})

#%%
# 4) Groundwater and surface water data
print(f"Processing and importing groundwater and surface water data. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")

# Quantify electricity requirements for pumping water in each cluster as a function of:
clusters =  QgsVectorLayer(processed_folder + 'clusters_12.gpkg',"","ogr")

# # a) proximity to surfaee water source
# # Clip it
# processing.run("gdal:cliprasterbyextent",
               # {'INPUT': categories_surface_water, 'PROJWIN': coords, 'NODATA': None,
                # 'OPTIONS': '', 'DATA_TYPE': 5,
                # 'OUTPUT': processed_folder + 'transitions_cropped.tif'})

# # Re-import it
# categories_surface_water = QgsRasterLayer(processed_folder + 'transitions_cropped.tif')

# # Reproject to world mercator to work in meters
# processing.run('gdal:warpreproject', {'INPUT' : categories_surface_water, 'DATA_TYPE' : 0, 'TARGET_CRS': 'EPSG:3395', 'OUTPUT' : processed_folder + 'transitions_wm.tif', 'OPTIONS': 'COMPRESS=DEFLATE|PREDICTOR=2|ZLEVEL=9', 'NODATA': None, 'TARGET_RESOLUTION': 500, 'MULTITHREADING': True})

# # Import it
# categories_surface_water = QgsRasterLayer(processed_folder + 'transitions_wm.tif')

# # Use distance from raster values tool to produce a layer of proximity(distance) to permanent (values 1 and 2) surface water
# processing.run('gdal:proximity', {'INPUT': categories_surface_water , 'BAND': 1, 'VALUES':'1,2', 'OUTPUT' : processed_folder + 'distance_surfwater.tif', 'OPTIONS': 'COMPRESS=DEFLATE|PREDICTOR=2|ZLEVEL=9', 'UNITS': 0})

# # Import it
# distance_surfwater = QgsRasterLayer(processed_folder + 'distance_surfwater.tif')

# # Reproject to WGS84
# processing.run('gdal:warpreproject', {'INPUT' : distance_surfwater, 'TARGET_CRS': 'EPSG:4326', 'OUTPUT' : processed_folder + 'distance_surfwater_repr.tif', 'OPTIONS': 'COMPRESS=DEFLATE|PREDICTOR=2|ZLEVEL=9', 'MULTITHREADING': True})

# Import it
distance_surfwater = QgsRasterLayer(processed_folder + 'distance_surfwater_repr.tif')
clusters =  QgsVectorLayer(processed_folder + 'clusters_12.gpkg',"","ogr")

# Zonal statistics of distance to permanent surface water
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': distance_surfwater, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': 'surfw_dist_', 'STATS': [2]})

# b)Groundwater depth
# Reclassify to numeric
# clusters = pandas.read_csv(input_folder + 'DepthToGroundwater/xyzASCII_dtwmap_v1.txt', sep='\t')
# clusters['depthwater'] = numpy.where(clusters['DTWAFRICA_'] == 'VS', 3.5, numpy.where(clusters['DTWAFRICA_'] == "S", 16, numpy.where(clusters['DTWAFRICA_'] == "SM", 37.5, numpy.where(clusters['DTWAFRICA_'] == "M", 75, numpy.where(clusters['DTWAFRICA_'] == "D", 175, numpy.where(clusters['DTWAFRICA_'] == "D", 250, 0))))))
# clusters.to_csv(input_folder + 'DepthToGroundwater/xyzASCII_dtwmap_v2.txt')

# uri='file:///' + input_folder + 'DepthToGroundwater/xyzASCII_dtwmap_v2.txt' + '?delimiter=,&yField=Y&xField=X'
# layer = QgsVectorLayer(uri, 'WeeklyContacts-2019-07-15', 'delimitedtext')
# QgsVectorFileWriter.writeAsVectorFormat(layer, input_folder + 'DepthToGroundwater/depthgroundwater.shp', "UTF-8", layer.crs(), "ESRI Shapefile", layerOptions=['SHPT=POINT'])

# # Import it
# groundwater_depth = QgsVectorLayer(input_folder + 'DepthToGroundwater/depthgroundwater.shp',"","ogr")

# # Clip it
# processing.run("gdal:clipvectorbyextent", {'INPUT':groundwater_depth,'EXTENT':'33.90958786,41.92621613,-4.72041702,5.06116581 [EPSG:4326]','OPTIONS':'','OUTPUT':processed_folder + 'groundwater_depth_cut.shp'})

# # Import it
# groundwater_depth = QgsVectorLayer(processed_folder + 'groundwater_depth_cut.shp',"","ogr")

# # Rasterize vector using depthwater as burn-in field
# processing.run("gdal:gridnearestneighbor", {
    # 'INPUT': groundwater_depth,
    # 'Z_FIELD': 'depthwater', 'RADIUS_1': 0, 'RADIUS_2': 0, 'ANGLE': 0, 'NODATA': None, 'OPTIONS': '', 'DATA_TYPE': 5,
    # 'OUTPUT': processed_folder + 'groundwater_depth_ras.tif'})

# Import it
groundwater_depth = QgsRasterLayer(processed_folder + 'groundwater_depth_ras.tif')
clusters =  QgsVectorLayer(processed_folder + 'clusters_12.gpkg',"","ogr")

# Zonal statistics
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': groundwater_depth, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': 'gr_wat_depth_', 'STATS': [2]})

# c) Groundwater storage
# Reclassify to numeric
# clusters = pandas.read_csv(input_folder + 'GroundwaterStorage/xyzASCII_gwstor_v1.txt', sep='\t')
# clusters['storagewater'] = numpy.where(clusters['GWSTOR_V2'] == 'VL', 0, numpy.where(clusters['GWSTOR_V2'] == "L", 500, numpy.where(clusters['GWSTOR_V2'] == "LM", 5500, numpy.where(clusters['GWSTOR_V2'] == "M", 17500, numpy.where(clusters['GWSTOR_V2'] == "H", 37500, 50000)))))
# clusters.to_csv(input_folder + 'GroundwaterStorage/xyzASCII_gwstor_v2.txt')

# uri='file:///' + input_folder + 'GroundwaterStorage/xyzASCII_gwstor_v2.txt' + '?delimiter=,&yField=Y&xField=X'
# layer = QgsVectorLayer(uri, 'WeeklyContacts-2019-07-15', 'delimitedtext')
# QgsVectorFileWriter.writeAsVectorFormat(layer, input_folder + 'GroundwaterStorage/storagegroundwater.shp', "UTF-8", layer.crs(), "ESRI Shapefile", layerOptions=['SHPT=POINT'])

# # Import it
# groundwater_storage = QgsVectorLayer(input_folder + 'GroundwaterStorage/storagegroundwater.shp',"","ogr")

# # Clip it
# processing.run("gdal:clipvectorbyextent", {'INPUT':groundwater_storage,'EXTENT':'33.90958786,41.92621613,-4.72041702,5.06116581 [EPSG:4326]','OPTIONS':'','OUTPUT':processed_folder + 'groundwater_storage_cut.shp'})

# # Import it
# groundwater_storage = QgsVectorLayer(processed_folder + 'groundwater_storage_cut.shp',"","ogr")

# # Rasterize vector using storagewater as burn-in field
# processing.run("gdal:gridnearestneighbor", {
    # 'INPUT': groundwater_storage,
    # 'Z_FIELD': 'storagewat', 'RADIUS_1': 0, 'RADIUS_2': 0, 'ANGLE': 0, 'NODATA': None, 'OPTIONS': '', 'DATA_TYPE': 5,
    # 'OUTPUT': processed_folder + 'groundwater_storage_ras.tif'})

# Import it
groundwater_storage = QgsRasterLayer(processed_folder + 'groundwater_storage_ras.tif')
clusters =  QgsVectorLayer(processed_folder + 'clusters_12.gpkg',"","ogr")

# Zonal statistics
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': groundwater_storage, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': 'gr_wat_storage_', 'STATS': [2]})

# d)Groundwate productivity
# Reclassify to numeric
# clusters = pandas.read_csv(input_folder + 'GroundwaterProductivity/xyzASCII_gwprod_v1.txt', sep='\t')
# clusters['productivitywater'] = numpy.where(clusters['GWPROD_V2'] == 'VH', 25, numpy.where(clusters['GWPROD_V2'] == "H", 12.5, numpy.where(clusters['GWPROD_V2'] == "M", 3, numpy.where(clusters['GWPROD_V2'] == "LM", 0.75, numpy.where(clusters['GWPROD_V2'] == "L", 0.3, 0.05)))))
# clusters.to_csv(input_folder + 'GroundwaterProductivity/xyzASCII_gwprod_v2.txt')

# uri='file:///' + input_folder + 'GroundwaterProductivity/xyzASCII_gwprod_v2.txt' + '?delimiter=,&yField=Y&xField=X'
# layer = QgsVectorLayer(uri, 'WeeklyContacts-2019-07-15', 'delimitedtext')
# QgsVectorFileWriter.writeAsVectorFormat(layer, input_folder + 'GroundwaterProductivity/productivitygroundwater.shp', "UTF-8", layer.crs(), "ESRI Shapefile", layerOptions=['SHPT=POINT'])

# # Import it
# groundwater_productivity = QgsVectorLayer(input_folder + 'GroundwaterProductivity/productivitygroundwater.shp',"","ogr")

# # Clip it
# processing.run("gdal:clipvectorbyextent", {'INPUT':groundwater_productivity,'EXTENT':'33.90958786,41.92621613,-4.72041702,5.06116581 [EPSG:4326]','OPTIONS':'','OUTPUT':processed_folder + 'groundwater_productivity_cut.shp'})

# # Import it
# groundwater_productivity = QgsVectorLayer(processed_folder + 'groundwater_productivity_cut.shp',"","ogr")

# # Rasterize vector using productivitywater as burn-in field
# processing.run("gdal:gridnearestneighbor", {
    # 'INPUT': groundwater_productivity,
    # 'Z_FIELD': 'productivi', 'RADIUS_1': 0, 'RADIUS_2': 0, 'ANGLE': 0, 'NODATA': None, 'OPTIONS': '', 'DATA_TYPE': 5,
    # 'OUTPUT': processed_folder + 'groundwater_productivity_ras.tif'})

# Import it
groundwater_productivity = QgsRasterLayer(processed_folder + 'groundwater_productivity_ras.tif')
clusters =  QgsVectorLayer(processed_folder + 'clusters_12.gpkg',"","ogr")

# Zonal statistics
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': groundwater_productivity, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters, 'COLUMN_PREFIX': 'gr_wat_productivity_', 'STATS': [2]})


#%%
# 5) Groundwater and - where needed - surfacewater pump
print(f"Estimating grounwater pump power requirements. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")

# Calculate the pumping electric power requirements (as a function of 2a, 2b, 2c, 2d, and total crop water requirements in each month)
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_5.csv', 'CP1250', clusters.crs(), 'CSV')

clusters = pandas.read_csv(processed_folder + 'clusters_5.csv')

# To fix potential bugs in the data, delete negative values
clusters['gr_wat_depth_mean'] = numpy.where(clusters['gr_wat_depth_mean']<0, 0, clusters['gr_wat_depth_mean'])

# Groundwater pump flow rate required in m3/s as the maximum of 12 months

for i in range(1, 13, 1):
    clusters["q" + str(i)] = clusters['monthly_IRREQ' + "_" + str(i)] /30/nhours_irr/3600

#constraint for the flow rate, where the amount of groundwater depletion during the 6 hours with irrigation is lower than the amount of groundwater generation during the 18 hours with no irrigation
clusters["qc1"]=((clusters["gr_wat_productivity_mean"]*(24-nhours_irr)/nhours_irr)+clusters["gr_wat_productivity_mean"])/1000*clusters['Area']*0.05
import math
#clusters["qc1"]= math.inf

#constraint for the flow rate, where the flow rate to consume completely the storage in 6 hours is higher than the flow rate required
clusters["qc2"]=clusters["gr_wat_storage_mean"] * clusters['Area']*0.05 *10 /(nhours_irr * 3600) + (clusters["gr_wat_productivity_mean"]/1000)

#if the flow rate is lower than the productivity no problem
#if the th flow rate complies the 2 constraints it is ok as well
#if neither hold, the flow rate is too much and the irrigation implies a depletion of the groundwater reservoir, so no optimal condition for the crop growth, highlighting this problem with a flag and bringing down the pump capacity to sustainable levels
for i in range(1, 13, 1):
    clusters["warning" + str(i)] = numpy.where((clusters["q"+ str(i)]<clusters["qc1"]) & (clusters["q"+ str(i)]<clusters["qc2"]), 0, 1)
    # Sustainable groundwater pumping rate
    clusters["q_sust" + str(i)] = numpy.where((clusters["q"+ str(i)]<clusters["qc1"]) & (clusters["q"+ str(i)]<clusters["qc2"]), clusters["q"+ str(i)], clusters[['qc1','qc2']].min(axis=1))
    # Unmet demand due to unsustainable pumping
    clusters["q_diff"+ str(i)] = clusters["q"+ str(i)] - clusters["q_sust"+ str(i)]
    # RGH to estimate power for pump (in W), missing the head losses
    clusters['powerforpump'+ str(i)] = (rho* g * clusters['gr_wat_depth_mean']* clusters["q_sust"+ str(i)])/eta_pump
    clusters['powerforpump'+ str(i)] = numpy.where(clusters["gr_wat_depth_mean"]>15, 0, clusters['powerforpump'+ str(i)])
    clusters["nogroundwater"] = numpy.where(clusters["gr_wat_depth_mean"]>15, 1, 0)
    #  If necessary, and if it is possible, get the difference between q and q_sust from surface water bodies
    # NB: groundwater pumping is always prioritised! 
    clusters["surfw_q"+ str(i)] = numpy.where(clusters["nogroundwater"] == 0, clusters["q_diff"+ str(i)], clusters["q"+ str(i)])
    # But put a distance limit 
    clusters["surfw_q"+ str(i)] = numpy.where(clusters["surfw_dist_mean"]<=threshold_surfacewater_distance, clusters["surfw_q"+ str(i)], 0)
    # And put a variable to signal clusters where we cannot meet irrigation needs nither by groundwater nor by surfacewater pumping
    clusters["imposs_wat"+ str(i)] = numpy.where((clusters["q_diff"+ str(i)]!=0) & (clusters["surfw_dist_mean"]>threshold_surfacewater_distance), 1, 0)
    # Estimate pump power (in W) for surface water pump
    water_speed = 2 #m/s, https://www.engineeringtoolbox.com/flow-velocity-water-pipes-d_385.html
    water_viscosity = 0.00089 #https://www.engineersedge.com/physics/water__density_viscosity_specific_weight_13146.htm
    pipe_diameter = 0.8 # m
    clusters["surfw_w"+ str(i)] = clusters["surfw_q"+ str(i)]*((32 * water_speed * clusters["surfw_dist_mean"] *water_viscosity)/pipe_diameter**2)/eta_pump
    #Calculate monthly electric requirement
    clusters['wh_monthly'+ str(i)] = clusters['powerforpump'+ str(i)]*nhours_irr*30 + clusters['surfw_w'+ str(i)]*nhours_irr*30
    clusters['er_kwh' + str(i)] = clusters['wh_monthly'+ str(i)]/1000

# simulate daily profile
load_curve_irr = [0, 0, 0, 0, 0, 0.166, 0.166, 0.166, 0.166, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.166, 0.166]

for k in range(1, 13, 1):
    for i in range(24):
        clusters['er_kwh_' + str(k) + "_" + str(i)] = (clusters['er_kwh'+ str(k)]/30)*load_curve_irr[i]

for k in range(1, 13, 1):
    clusters['er_kwh_tt' + str(k)] = clusters['er_kwh' + str(k)]/30

for k in range(1, 13, 1):
    for i in range(24):
        clusters['er_kwh_' + str(k) + "_" +  str(i)] = clusters['er_kwh_' + str(k) + "_" + str(i)]/clusters['er_kwh_tt' + str(k)]
        clusters['er_kwh_' + str(k) + "_" + str(i)] = clusters['er_kwh_' + str(k) + "_" + str(i)].fillna(0)

clusters.to_csv(processed_folder + 'clusters_7.csv')

list1 = [col for col in clusters.columns if 'er_kwh_' in col]

list2 = [col for col in clusters.columns if 'q_sust' in col]

list2.append(list1)

#Write to file
processing.run("native:joinattributestable", {
        'INPUT': processed_folder + 'clusters_12.gpkg', 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_7.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': list1, 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_13.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_13.gpkg',"","ogr")

#%%
#7) Generate appliance-based stochastic demand for residential customers using RAMP

for i in range(1, 13, 1): 
    vars()['rur1' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Rural/Outputs/Tier-1/output_file_' + str(i) + '.csv')
    vars()['rur1'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['rur1'+ "_" + str(i)]['hour'] = vars()['rur1'+ "_" + str(i)]['minutes']//60%24
    vars()['rur1'+ "_" + str(i)] = vars()['rur1'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['rur1'+ "_" + str(i)]['values'] = vars()['rur1'+ "_" + str(i)]['values']/1000/100
    vars()['rur2' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Rural/Outputs/Tier-2/output_file_' + str(i) + '.csv')
    vars()['rur2'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['rur2'+ "_" + str(i)]['hour'] =  vars()['rur2'+ "_" + str(i)]['minutes']//60%24
    vars()['rur2'+ "_" + str(i)] =  vars()['rur2'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['rur2'+ "_" + str(i)]['values'] =  vars()['rur2'+ "_" + str(i)]['values']/1000/100
    vars()['rur3' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Rural/Outputs/Tier-3/output_file_' + str(i) + '.csv')
    vars()['rur3'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['rur3'+ "_" + str(i)]['hour'] =  vars()['rur3'+ "_" + str(i)]['minutes']//60%24
    vars()['rur3'+ "_" + str(i)] =  vars()['rur3'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['rur3'+ "_" + str(i)]['values'] =  vars()['rur3'+ "_" + str(i)]['values']/1000/100
    vars()['rur4' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Rural/Outputs/Tier-4/output_file_' + str(i) + '.csv')
    vars()['rur4'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['rur4'+ "_" + str(i)]['hour'] =  vars()['rur4'+ "_" + str(i)]['minutes']//60%24
    vars()['rur4'+ "_" + str(i)] =  vars()['rur4'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['rur4'+ "_" + str(i)]['values'] =  vars()['rur4'+ "_" + str(i)]['values']/1000/100
    vars()['rur5' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Rural/Outputs/Tier-5/output_file_' + str(i) + '.csv')
    vars()['rur5'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['rur5'+ "_" + str(i)]['hour'] =  vars()['rur5'+ "_" + str(i)]['minutes']//60%24
    vars()['rur5'+ "_" + str(i)] =  vars()['rur5'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['rur5'+ "_" + str(i)]['values'] =  vars()['rur5'+ "_" + str(i)]['values']/1000/100

for i in range(1, 13, 1): 
    vars()['urb1' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Urban/Outputs/Tier-1/output_file_' + str(i) + '.csv')
    vars()['urb1'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['urb1'+ "_" + str(i)]['hour'] = vars()['urb1'+ "_" + str(i)]['minutes']//60%24
    vars()['urb1'+ "_" + str(i)] = vars()['urb1'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['urb1'+ "_" + str(i)]['values'] = vars()['urb1'+ "_" + str(i)]['values']/1000/100
    vars()['urb2' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Urban/Outputs/Tier-2/output_file_' + str(i) + '.csv')
    vars()['urb2'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['urb2'+ "_" + str(i)]['hour'] =  vars()['urb2'+ "_" + str(i)]['minutes']//60%24
    vars()['urb2'+ "_" + str(i)] =  vars()['urb2'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['urb2'+ "_" + str(i)]['values'] =  vars()['urb2'+ "_" + str(i)]['values']/1000/100
    vars()['urb3' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Urban/Outputs/Tier-3/output_file_' + str(i) + '.csv')
    vars()['urb3'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['urb3'+ "_" + str(i)]['hour'] =  vars()['urb3'+ "_" + str(i)]['minutes']//60%24
    vars()['urb3'+ "_" + str(i)] =  vars()['urb3'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['urb3'+ "_" + str(i)]['values'] =  vars()['urb3'+ "_" + str(i)]['values']/1000/100
    vars()['urb4' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Urban/Outputs/Tier-4/output_file_' + str(i) + '.csv')
    vars()['urb4'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['urb4'+ "_" + str(i)]['hour'] =  vars()['urb4'+ "_" + str(i)]['minutes']//60%24
    vars()['urb4'+ "_" + str(i)] =  vars()['urb4'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['urb4'+ "_" + str(i)]['values'] =  vars()['urb4'+ "_" + str(i)]['values']/1000/100
    vars()['urb5' + "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_households/Urban/Outputs/Tier-5/output_file_' + str(i) + '.csv')
    vars()['urb5'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['urb5'+ "_" + str(i)]['hour'] =  vars()['urb5'+ "_" + str(i)]['minutes']//60%24
    vars()['urb5'+ "_" + str(i)] =  vars()['urb5'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['urb5'+ "_" + str(i)]['values'] =  vars()['urb5'+ "_" + str(i)]['values']/1000/100


# define if clsuter is prevalently urban or rural
processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': input_folder + 'GHSL_settlement_type.tif', 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'isurban', 'STATS': [9]})

# Energy efficiency improvements. For now, we will assume that efficiency improvements are stronger by 5% for each tier higher
#rur1= rur1- eff_impr_rur1*rur1
#rur2= rur2- eff_impr_rur2*rur2
#rur3= rur3- eff_impr_rur3*rur3
#rur4= rur4- eff_impr_rur4*rur4
#rur5= rur5- eff_impr_rur5*rur5
#
#urb1= urb1- eff_impr_urb1*urb1
#urb2= urb2- eff_impr_urb2*urb2
#urb3= urb3- eff_impr_urb3*urb3
#urb4= urb4- eff_impr_urb4*urb4
#urb5= urb5- eff_impr_urb5*urb5

####
# Calculate the number of people in each tier in each cluster
#clusters = QgsVectorLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database_SSA/statcompiler_subnational_data_2020-03-17/shps/sdr_subnational_data_dhs_2015.shp',"","ogr") 
#
#raster_tiers = QgsRasterLayer('D:/merged_tiers.tif')
#
#processing.run("qgis:zonalstatistics",
#               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
#                'COLUMN_PREFIX': 'acc_pop_t1', 'STATS': [1]})
#
#processing.run("qgis:zonalstatistics",
#               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 2, 'INPUT_VECTOR': clusters,
#                'COLUMN_PREFIX': 'acc_pop_t2', 'STATS': [1]})
#
#processing.run("qgis:zonalstatistics",
#               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 3, 'INPUT_VECTOR': clusters,
#                'COLUMN_PREFIX': 'acc_pop_t3', 'STATS': [1]})
#
#processing.run("qgis:zonalstatistics",
#               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 4, 'INPUT_VECTOR': clusters,
#                'COLUMN_PREFIX': 'acc_pop_t4', 'STATS': [1]})
#
#population = QgsRasterLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/LandScan Global 2012-2017/landscan2017.tif')
#
## print(f"Add population to clusters. Elapsed time:", round((time.time() - then) / 60, 2), " minutes")
#processing.run("qgis:zonalstatistics",
#               {'INPUT_RASTER': population, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
#                'COLUMN_PREFIX': 'pop', 'STATS': [1]}, feedback=f)
#
#processing.run('native:reprojectlayer', {'INPUT' : clusters, 'TARGET_CRS': 'EPSG:3395', 'OUTPUT' : processed_folder + 'sdr_subnational_data_dhs_2015_rep.gpkg'})
#
#processing.run("qgis:fieldcalculator", {'INPUT': processed_folder + 'sdr_subnational_data_dhs_2015_rep.gpkg', 'FIELD_NAME': 'Area', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' $area * 0.0001', 'OUTPUT': processed_folder + 'sdr_subnational_data_dhs_2015_rep2.gpkg'})
#
##Create a 'pop density' attribute in each cluster (% of cropland over total land area)
#processing.run("qgis:fieldcalculator", {'INPUT': processed_folder + 'sdr_subnational_data_dhs_2015_rep2.gpkg', 'FIELD_NAME': 'popdens', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' \"popsum\" / \"Area\"', 'OUTPUT': processed_folder + 'sdr_subnational_data_dhs_2015_rep3.gpkg'})
#
## Urban / rural
#processing.run("qgis:zonalstatistics",
#               {'INPUT_RASTER': input_folder + 'GHSL_settlement_type.tif', 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
#                'COLUMN_PREFIX': 'isurban', 'STATS': [9]})
#
clusters = QgsVectorLayer(processed_folder + 'sdr_subnational_data_dhs_2015_rep3.gpkg',"","ogr")

# Predict future pop in each tier based on local income quintile distribution and U/R in currently electrified areas
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_train.csv', 'CP1250', clusters.crs(), 'CSV')

# Calculate the number of people in each tier in each cluster
clusters = QgsVectorLayer(processed_folder + 'clusters_13.gpkg',"","ogr")

raster_tiers = QgsRasterLayer('D:/merged_tiers.tif')

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t1', 'STATS': [1]})

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 2, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t2', 'STATS': [1]})

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 3, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t3', 'STATS': [1]})

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 4, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t4', 'STATS': [1]})

# Spatial join between income quintiles DHS and clusters
dhs = QgsVectorLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database_SSA/statcompiler_subnational_data_2020-03-17/shps/sdr_subnational_data_dhs_2015.shp',"","ogr") 

processing.run("qgis:joinattributesbylocation", {'INPUT':clusters ,'JOIN':dhs,'PREDICATE':[0,1],'JOIN_FIELDS':['HCWIXQPLOW', 'HCWIXQP2ND', 'HCWIXQPMID', 'HCWIXQP4TH', 'HCWIXQPHGH', 'ISO'],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':processed_folder + 'clusters_14.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_14.gpkg',"","ogr")

QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_predict.csv', 'CP1250', clusters.crs(), 'CSV')

### run in R
subprocess.call(['"C:/Programmi/R/R-3.5.1/bin/Rscript', '--vanilla', home_repo_folder + 'jrc/residential_r.r"'])
####

# joinanttributetables back to shapefile
processing.run("native:joinattributestable", {
        'INPUT': clusters, 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_predict.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['acc_pop_share_t1_new', 'acc_pop_share_t2_new', 'acc_pop_share_t3_new', 'acc_pop_share_t4_new'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_15.gpkg'})

clusters = QgsVectorLayer(processed_folder + 'clusters_15.gpkg',"","ogr")
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_predict2.csv', 'CP1250', clusters.crs(), 'CSV')
clusters = pandas.read_csv(processed_folder +'clusters_predict2.csv')

clusters['acc_pop_t1_new'] =  clusters['acc_pop_share_t1_new'] * clusters['noaccsum']
clusters['acc_pop_t2_new'] =  clusters['acc_pop_share_t2_new'] * clusters['noaccsum']
clusters['acc_pop_t3_new'] =  clusters['acc_pop_share_t3_new'] * clusters['noaccsum']
clusters['acc_pop_t4_new'] =  clusters['acc_pop_share_t4_new'] * clusters['noaccsum']

# Calculate number of households in each cluster
clusters['HHs'] = numpy.where(clusters['isurbanmajority']>=12, clusters['popsum']/3.5, clusters['popsum']/4.5)

for m in range(1, 13, 1):
    for i in range(0, 24, 1):
        clusters['PerHHD_' + str(m) + "_" + str(i)] = numpy.where(clusters['isurbanmajority'] >=12, vars()['urb1'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t1_new'] + vars()['urb2'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t2_new'] + vars()['urb3'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t3_new'] + vars()['urb4'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t4_new'] * 0.75 + vars()['urb5'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t4_new'] * 0.25, numpy.where(clusters['isurbanmajority'] < 12, vars()['rur1'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t1_new'] + vars()['rur2'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t2_new'] + vars()['rur3'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t3_new'] + vars()['rur4'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t4_new'] * 0.75 + vars()['rur5'+ "_" + str(m)]['values'].iloc[i] * clusters['acc_pop_share_t4_new'] * 0.25 , 0))

idx = clusters.columns.str.startswith('PerHHD_')
clusters['PerHHD_tt'] = clusters.iloc[:,idx].sum(axis=1) 

for m in range(1, 13, 1):
    idx = clusters.columns.str.startswith('PerHHD_' + str(m))
    clusters['PerHHD_tt' +"_monthly_" + str(m)] = clusters.iloc[:,idx].iloc[:,0:24].sum(axis=1) 

for m in range(1, 13, 1):
    for i in range(0, 24, 1):
        clusters['PerHHD_' + str(m) + "_" + str(i)] = clusters['PerHHD_' + str(m) + "_" + str(i)] / clusters['PerHHD_tt' +"_monthly_" + str(m)]

filter_col = ['id', 'HHs'] + [col for col in clusters if col.startswith('PerHHD_')] 
clusters = clusters[filter_col]

clusters.to_csv(processed_folder + 'clusters_6.csv')

#Write to file
processing.run("native:joinattributestable", {
        'INPUT': processed_folder + 'clusters_15.gpkg', 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_6.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': filter_col, 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_16.gpkg'})    

#%%
#6) Other productive activities: energy demand

## Input and georeference employment rate
#dhs_employment= QgsVectorLayer(input_folder + 'sdr_subnational_data_dhs_2014.gpkg',"","ogr")
#
#processing.run("qgis:joinattributesbylocation", {'INPUT':processed_folder + 'clusters_18.gpkg' ,'JOIN':dhs_employment,'PREDICATE':[0,1],'JOIN_FIELDS':['EMEMPLWEMC','EMEMPLMEMC'],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':processed_folder + 'clusters_19.gpkg'})
#
#clusters = QgsVectorLayer(processed_folder + 'clusters_19.gpkg',"","ogr")
#QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_11.csv', 'CP1250', clusters.crs(), 'CSV')
#
#clusters = pandas.read_csv(processed_folder + 'clusters_11.csv')
#
## Calculate a potential demand from productive activities based on Moner Girona et al. 2019
#clusters['employment_rate'] = (clusters['EMEMPLMEMC']*0.5 + clusters['EMEMPLWEMC']*0.5)/100
#
#clusters['ProductiveD'] = (clusters['HHs'] * clusters['PerHHD_ref'] * clusters['employment_rate'])*0.25 + 0.25* clusters['er_kwh']
# 
#clusters.to_csv(processed_folder + 'clusters_12.csv')
#
#processing.run("native:joinattributestable", {
#       'INPUT': processed_folder + 'clusters_19.gpkg', 'FIELD': 'id',
#       'INPUT_2': processed_folder + 'clusters_12.csv',
#       'FIELD_2': 'id', 'FIELDS_TO_COPY': ['ProductiveD', 'employment_rate'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
#       'OUTPUT': processed_folder + 'clusters_20.gpkg'})
#


#Crop processing machinery: energy demand
# Import csv of energy consumption by crop 
energy_crops = pandas.read_csv(input_folder +'crop_processing.csv')

# Extract yield 
# Import all Yield (kg/ha) cropland layers (Default datasets used: MapSPAM)
# NB: when using MapSPAM use harvested area, which accounts for multiple growing seasons per year)
rast_path = spam_folder + 'spam2010v1r0_global_yield.geotiff'
rasters_rainfed = glob.glob(os.path.join(rast_path, "spam2010*_r.tif"))
clusters = QgsVectorLayer(processed_folder + 'clusters_16.gpkg',"","ogr")

for X in rasters_rainfed:
    a = "Y_" + X[-10:-6] + "_"
    print('iterating' + a)
    processing.run("qgis:zonalstatistics",
                   {'INPUT_RASTER': X, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                    'COLUMN_PREFIX': a, 'STATS': [2]})

# Multiply kg/ha by harvested
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_7.csv', 'CP1250', clusters.crs(), 'CSV')
clusters = pandas.read_csv(processed_folder +'clusters_7.csv')

for X in rasters_rainfed:
    clusters["yield_" + X[-10:-6] + "_tot"] = (clusters["Y_" + X[-10:-6] + "_mean"] * clusters["A_" + X[-10:-6] + "_sum"])

# Multiply yearly yield of each crop by unit processing energy requirement to estimate yearly demand in each cluster as the sum of each crop processing energy demand
for X in energy_crops['Crop']:
    clusters["kwh" + X + "_tot"] = clusters["yield_" + X + "_tot"] * energy_crops.loc[energy_crops['Crop'] == X, 'kwh_kg'].values[0]

clusters['kwh_cp_tt'] = clusters[[col for col in clusters if col.startswith('kwh')]].sum(axis=1)

crops = pandas.read_excel(input_folder + 'crops_cfs_ndays_months.xlsx')

# processing to take place in post-harvesting months: for each crop 1) take harvesting date 2) take plantation months. for those months between 1 and 2 equally allocate crop processing

crops = crops[crops.set_index(['crop']).index.isin(energy_crops.set_index(['Crop']).index)]

for i in range(0,len(crops), 1):
    for m in range(1,13, 1): 
        print("Processing ", crops.iloc[i,0])
        daily = {'countdays': numpy.arange(1,730)}
        daily = pandas.DataFrame(data=daily)
        daily['date'] = pandas.date_range(datetime.datetime.strptime("01012019", "%d%m%Y"), periods=729)
        daily['month'] = pandas.DatetimeIndex(daily['date']).month
        daily['day'] = pandas.DatetimeIndex(daily['date']).day
        pm1=datetime.datetime.strptime(str(crops['pm_1'].iloc[i]) + "2019", "%d%m%Y")
        pm2=datetime.datetime.strptime(str(crops['pm_2'].iloc[i]) + "2019", "%d%m%Y")
        a = daily[daily['date'] > (pm1 + datetime.timedelta(days=int(crops['nd_1'].iloc[i]) + int(crops['nd_2'].iloc[i])+int(crops['nd_3'].iloc[i])+int(crops['nd_4'].iloc[i])))]
        a = a[a['date']<datetime.datetime(2020, 3, 15, 0, 0)]
        a = a[a["month"] == m]
        a = a.shape[0]
        clusters["kwh_cp" + str(crops['crop'].iloc[i]) + "_" + str(m)] = clusters["kwh" + str(crops['crop'].iloc[i]) + "_tot"] / a
        clusters["kwh_cp" + str(crops['crop'].iloc[i]) + "_" + str(m)].replace(numpy.inf, 0, inplace=True)
        clusters["kwh_cp" + str(crops['crop'].iloc[i]) + "_" + str(m)].replace(numpy.nan, 0, inplace=True)

# sum all crops by months
for z in range(1,13, 1):
    a = clusters[[col for col in clusters if col.startswith('kwh_cp')]]
    a2 = a[[col for col in a if col.endswith('_' + str(z))]]
    clusters['monthly_kwh_cropproc' + "_" + str(z)] = a2.sum(axis=1)

# simulate daily profile
load_curve_cp = [0, 0, 0, 0, 0, 0, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0, 0, 0, 0, 0, 0]

for k in range(1, 13, 1):
    clusters['kwh_cropproc_tt_' + str(k)] = clusters['monthly_kwh_cropproc' + "_" + str(k)]/30

for k in range(1, 13, 1):
    for i in range(24):
        clusters['kwh_cropproc' + str(k) + "_" +  str(i)] = (clusters['kwh_cropproc_tt_' + str(k)])*load_curve_cp[i]

for k in range(1, 13, 1):
    for i in range(24):
        clusters['kwh_cropproc' + str(k) + "_" +  str(i)] = clusters['kwh_cropproc' + str(k) + "_" +  str(i)]/clusters['kwh_cropproc_tt_' + str(k)]
        clusters['kwh_cropproc' + str(k) + "_" + str(i)] = clusters['kwh_cropproc' + str(k) + "_" +  str(i)].fillna(0)

list1 = [col for col in clusters.columns if 'kwh_cropproc' in col]
list1.insert(0, "kwh_cp_tt")
list1.insert(0, "id")

clusters = clusters[list1]

clusters = clusters.fillna(0)

# Write to csv file
clusters.to_csv(processed_folder + 'clusters_8.csv')

#%%
# 7) Add education and healthcare facilities
print(f"Estimating electricity requirements form schools and healthcare facilities. Elapsed time:",  round((time.time()-then)/60, 2), " minutes")

#OSM_question = input(Do you want to use a local shapefile or retireve facilities using OpenStreetMap?)
#https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0

# Classifying schools and healthcare facilities
health = pandas.read_excel(health_edu_folder + "GeoHealth Data.xlsx")

# Extract coordinates from csv file of healthcare facilities
health['Y'] = health.Geolocation.apply(lambda st: st[st.find("(")+1:st.find(",")]  if pandas.notnull(st) else st)
health['X'] = health.Geolocation.apply(lambda st: st[st.find(",")+1:st.find(")")]  if pandas.notnull(st) else st)

# Select columns to keep
health = health[["FCode", "X", "Y", "Type", "Beds", "Cots", "Open24Hours", "OpenWeekends", "OperationalStatus"]]

# Keep only operational facilities
health = health.loc[(health['OperationalStatus'] == 'Operational') | ('OperationalStatus' == "Pending Opening")]

# Classify healthcare facilities into 5 tiers
health['heal_type1'] = (health['Type'] == 'Dispensary')
health['heal_type2'] = (health['Type']=='Medical Clinic') | (health['Type'] == 'Dental Clinic') | (health['Type'] == 'Eye Centre') |  (health['Type'] == 'Laboratory (Stand-alone)') | (health['Type'] == 'Medical Centre') | (health['Type'] == 'Radiology Unit') |  (health['Type'] == 'Regional Blood Tranclustersusion Centre') | (health['Type']=='Health Centre') | (health['Type']=='Maternity Home') | (health['Type']=='Nursing Home') | (health['Type']=='VCT Centre') | (health['Type']=='Health Programme') | (health['Type']=='Health Project') |  (health['Type']=='Rural Health Training Centre') | (health['Type']=='Training Institution in Health (Stand-alone)')
health['heal_type3'] = (health['Type']=='Other Hospital') | (health['Type']=='Sub-District Hospital')
health['heal_type4'] = (health['Type']=='District Hospital') |  (health['Type']=='Provincial General Hospital') 
health['heal_type5'] = (health['Type']=='National Referral Hospital')

 
# Calculate number of beds and cots of each tier in each cluster
health['beds_1'] = numpy.where(health['heal_type1']== 1, health['Beds'] + health['Cots'], 0)
health['beds_2'] = numpy.where(health['heal_type2']== 1, health['Beds'] + health['Cots'], 0)
health['beds_3'] = numpy.where(health['heal_type3']== 1, health['Beds'] + health['Cots'], 0)
health['beds_4'] = numpy.where(health['heal_type4']== 1, health['Beds'] + health['Cots'], 0)
health['beds_5'] = numpy.where(health['heal_type5']== 1, health['Beds'] + health['Cots'], 0)

# In any case the dispensary counts as one bed
health['beds_1'] = numpy.where((health['beds_1']==0) & (health['heal_type1']== 1), 1, health['beds_1'])

#Fill empty fields with average number of beds of the category
health['beds_1'] = health['beds_1'].fillna(1)
health['beds_2'] = health['beds_2'].fillna(45)
health['beds_2'] = numpy.where((health['beds_2']==0), 45, health['beds_2'])
health['beds_3'] = health['beds_3'].fillna(150)
health['beds_3'] = numpy.where((health['beds_3']==0), 150, health['beds_3'])
health['beds_4'] = health['beds_4'].fillna(450)
health['beds_4'] = numpy.where((health['beds_4']==0), 450, health['beds_4'])
health['beds_5'] = health['beds_5'].fillna(2000)
health['beds_5'] = numpy.where((health['beds_5']==0), 2000, health['beds_5'])

# #Keep only hospitals with valid coordinates
health = health[pandas.to_numeric(health['X'], errors='coerce').notnull()]

# To numeric
health['Y'] = pandas.to_numeric(health['Y'])
health['X'] = pandas.to_numeric(health['X'])

# #Convert to a spatial dataframe using coordinates
health_geo = geopandas.GeoDataFrame(health.drop(['X', 'Y'], axis=1),
                                crs={'init': 'epsg:4326'},
                                geometry=[shapely.geometry.Point(xy) for xy in zip(health.X, health.Y)])

# # Write to shapefile
health_geo.to_file(processed_folder + 'health_facilities_in_kenya.shp')

#Import schools
schools = geopandas.read_file(health_edu_folder + 'Kenya_Open_Data_Initiative_KODI_Primary_Schools.shp')

# Classify schools using total enrollment as a proxy for their tier
schools['sch_type1'] = (schools['TotalEnrol'] > 0) & (schools['TotalEnrol'] <= 50)      #method to be confirmed
schools['sch_type2'] = (schools['TotalEnrol'] > 50) & (schools['TotalEnrol'] <= 150)    #method to be confirmed
schools['sch_type3'] = (schools['TotalEnrol'] > 150) & (schools['TotalEnrol'] <= 300)   #method to be confirmed
schools['sch_type4'] = (schools['TotalEnrol'] > 300) & (schools['TotalEnrol'] <= 600)   #method to be confirmed
schools['sch_type5'] = (schools['TotalEnrol'] > 600)                                    #method to be confirmed

schools['pupils_1'] = numpy.where(schools['sch_type1']== 1, schools['TotalEnrol'], 0)
schools['pupils_2'] = numpy.where(schools['sch_type2']== 1, schools['TotalEnrol'], 0)
schools['pupils_3'] = numpy.where(schools['sch_type3']== 1, schools['TotalEnrol'], 0)
schools['pupils_4'] = numpy.where(schools['sch_type4']== 1, schools['TotalEnrol'], 0)
schools['pupils_5'] = numpy.where(schools['sch_type5']== 1, schools['TotalEnrol'], 0)

schools['pupils_1'] = numpy.where(schools['pupils_1']== 0, 50, schools['pupils_1'])
schools['pupils_2'] = numpy.where(schools['pupils_2']== 0, 100, schools['pupils_2'])
schools['pupils_3'] = numpy.where(schools['pupils_3']== 0, 225, schools['pupils_3'])
schools['pupils_4'] = numpy.where(schools['pupils_4']== 0, 450, schools['pupils_4'])
schools['pupils_5'] = numpy.where(schools['pupils_5']== 0, 700, schools['pupils_5'])

# Rewrite to shapefile
schools.to_file(health_edu_folder + 'Kenya_Open_Data_Initiative_KODI_Primary_Schools.shp')

# Import schools and healthcare classified (Default datasets used: ...)
primaryschools = QgsVectorLayer(health_edu_folder + 'Kenya_Open_Data_Initiative_KODI_Primary_Schools.shp',"","ogr")
healthcarefacilities = QgsVectorLayer(processed_folder + 'health_facilities_in_kenya.shp',"","ogr")

# Count the number of schools of each type in each cluster
fields = ['pupils_1', 'pupils_2', 'pupils_3', 'pupils_4', 'pupils_5']
for field in fields:
    print("Processing ", field)
    processing.run("gdal:rasterize", {
    'INPUT': primaryschools,
    'FIELD': field, 'UNITS': 1, 'WIDTH': 0.008333, 'HEIGHT': 0.008333,
    'EXTENT': coords, 'OPTIONS': '', 'DATA_TYPE': 5,
    'INIT': None, 'INVERT': False, 'OUTPUT': processed_folder + field + ".tif", 'NO_DATA': 0})

# # Count the number of healthcare facilities of each type in each cluster
fields = ['beds_1', 'beds_2', 'beds_3', 'beds_4', 'beds_5']
for field in fields:
    print("Processing ", field)
    processing.run("gdal:rasterize", {
    'INPUT': healthcarefacilities,
    'FIELD': field, 'UNITS': 1, 'WIDTH': 0.008333, 'HEIGHT': 0.008333,
    'EXTENT': coords, 'OPTIONS': '', 'DATA_TYPE': 5,
    'INIT': None, 'INVERT': False, 'OUTPUT': processed_folder + field + ".tif", 'NO_DATA': 0})

#fields = ['sch_type1', 'sch_type2', 'sch_type3', 'sch_type4', 'sch_type5']
#for field in fields:
    #print("Processing ", field)
    #processing.run("gdal:rasterize", {
        #'INPUT': primaryschools,
        #'FIELD': field, 'UNITS': 1, 'WIDTH': 0.0008333, 'HEIGHT': 0.0008333,
        #'EXTENT': coords, 'OPTIONS': '', 'DATA_TYPE': 5,
        #'INIT': None, 'INVERT': False, 'OUTPUT': processed_folder + field + ".tif", 'NO_DATA': 0})

# fields = ['heal_type1', 'heal_type2', 'heal_type3', 'heal_type4', 'heal_type5']
# for field in fields:
    # print("Processing ", field)
    # processing.run("gdal:rasterize", {
        # 'INPUT': healthcarefacilities,
        # 'FIELD': field, 'UNITS': 1, 'WIDTH': 0.0008333, 'HEIGHT': 0.0008333,
        # 'EXTENT': coords, 'OPTIONS': '', 'DATA_TYPE': 5,
        # 'INIT': None, 'INVERT': False, 'OUTPUT': processed_folder + field + ".tif", 'NO_DATA': 0})

clusters = QgsVectorLayer(processed_folder + 'clusters_16.gpkg',"","ogr")
files = ['pupils_1.tif', 'pupils_2.tif', 'pupils_3.tif', 'pupils_4.tif', 'pupils_5.tif', 'beds_1.tif', 'beds_2.tif', 'beds_3.tif', 'beds_4.tif', 'beds_5.tif']

for i in files:
    print(i)
    processing.run("qgis:zonalstatistics",
                   {'INPUT_RASTER': processed_folder + i, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                    'COLUMN_PREFIX': i, 'STATS': [1]})

# Assume densification of schools
#exec(open("./healthedu2030predict.py").read(), globals())

#%%
# 8) Estimate the yearly electric demand from healthcare and education facilities
# define consumption of facility types (kWh/facility/year)
for i in range(1, 13, 1): 
    vars()['health1'+ "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/1.Health/Dispensary/Outputs/output_file_' + str(i) + '.csv')
    vars()['health1'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['health1'+ "_" + str(i)]['hour'] = vars()['health1'+ "_" + str(i)]['minutes']//60%24
    vars()['health1'+ "_" + str(i)] = vars()['health1'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['health1'+ "_" + str(i)]['values'] = vars()['health1'+ "_" + str(i)]['values']/1000
    vars()['health2'+ "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/1.Health/HealthCentre/Outputs/output_file_' + str(i) + '.csv')
    vars()['health2'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['health2'+ "_" + str(i)]['hour'] = vars()['health2'+ "_" + str(i)]['minutes']//60%24
    vars()['health2'+ "_" + str(i)] = vars()['health2'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['health2'+ "_" + str(i)]['values'] = vars()['health2'+ "_" + str(i)]['values']/1000
    vars()['health3'+ "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' + str(i) + '.csv')
    vars()['health3'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['health3'+ "_" + str(i)]['hour'] = vars()['health3'+ "_" + str(i)]['minutes']//60%24
    vars()['health3'+ "_" + str(i)] = vars()['health3'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['health3'+ "_" + str(i)]['values'] = vars()['health3'+ "_" + str(i)]['values']/1000
    vars()['health4'+ "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' + str(i) + '.csv')
    vars()['health4'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['health4'+ "_" + str(i)]['hour'] = vars()['health4'+ "_" + str(i)]['minutes']//60%24
    vars()['health4'+ "_" + str(i)] = vars()['health4'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['health4'+ "_" + str(i)]['values'] = vars()['health4'+ "_" + str(i)]['values']/1000*1.3
    vars()['health5'+ "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' + str(i) + '.csv')
    vars()['health5'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['health5'+ "_" + str(i)]['hour'] = vars()['health5'+ "_" + str(i)]['minutes']//60%24
    vars()['health5'+ "_" + str(i)] = vars()['health5'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['health5'+ "_" + str(i)]['values'] = vars()['health5'+ "_" + str(i)]['values']/1000*1.6

for i in range(1, 13, 1): 
    vars()['edu'+ "_" + str(i)] = pandas.read_csv(home_repo_folder + 'ramp/RAMP_services/2.School/Output/output_file_' + str(i) + '.csv')
    vars()['edu'+ "_" + str(i)].columns = ['minutes', 'values']
    vars()['edu'+ "_" + str(i)]['hour'] = vars()['edu'+ "_" + str(i)]['minutes']//60%24
    vars()['edu'+ "_" + str(i)] = vars()['edu'+ "_" + str(i)].groupby('hour', as_index=False)['values'].mean()
    vars()['edu'+ "_" + str(i)]['values'] = vars()['edu'+ "_" + str(i)]['values']/1000/10 #/10 schools simulated 

# Allocate demand to each cluster based on  number of facilities and their tier
clusters = QgsVectorLayer(processed_folder + 'clusters_16.gpkg',"","ogr")
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_13.csv', 'CP1250', clusters.crs(), 'CSV')

clusters = pandas.read_csv(processed_folder + 'clusters_13.csv')

for m in range(1, 13, 1):
    for i in range(0, 24, 1):
        clusters['er_hc_' + str(m) + "_" + str(i)] = vars()['health1'+ "_" + str(m)]['values'].iloc[i] * clusters['beds_1.tifsum'] + vars()['health2'+ "_" + str(m)]['values'].iloc[i]/45 * clusters['beds_2.tifsum'] + vars()['health3'+ "_" + str(m)]['values'].iloc[i]/150 * clusters['beds_3.tifsum'] + vars()['health4'+ "_" + str(m)]['values'].iloc[i]/450 * clusters['beds_4.tifsum'] + vars()['health5'+ "_" + str(m)]['values'].iloc[i]/2000 * clusters['beds_5.tifsum']       
        clusters['er_sch_' + str(m) + "_" + str(i)] = clusters['pupils_1.tifsum'] * vars()['edu'+ "_" + str(m)]['values'].iloc[i]/700 + clusters['pupils_2.tifsum'] * vars()['edu'+ "_" + str(m)]['values'].iloc[i]/700 + clusters['pupils_3.tifsum'] * vars()['edu'+ "_" + str(m)]['values'].iloc[i]/700 + clusters['pupils_4.tifsum'] * vars()['edu'+ "_" + str(m)]['values'].iloc[i]/700 + clusters['pupils_5.tifsum'] * vars()['edu'+ "_" + str(m)]['values'].iloc[i]/700
        # Schools and healthcare facilities are assumed to be already electrified in the total electricity access level in the cluster is > 0.75
        clusters['er_hc_' + str(m) + "_" + str(i)] = numpy.where(clusters['elrate'] > 0.75, 0,  clusters['er_hc_' + str(m) + "_" + str(i)])
        clusters['er_sch_' + str(m) + "_" + str(i)] = numpy.where(clusters['elrate'] > 0.75, 0,  clusters['er_sch_' + str(m) + "_" + str(i)])

# Generate variable for total daily demand and variables as shares of the daily demand
idx = clusters.columns.str.startswith('er_hc_')
clusters['er_hc_tt'] = clusters.iloc[:,idx].sum(axis=1) 

for m in range(1, 13, 1):
    idx = clusters.columns.str.startswith('er_hc_' + str(m))
    clusters['er_hc_tt' +"_monthly_" + str(m)] = clusters.iloc[:,idx].iloc[:,0:24].sum(axis=1) 

for m in range(1, 13, 1):
    for i in range(0, 24, 1):
        clusters['er_hc_' + str(m) + "_" + str(i)] = clusters['er_hc_' + str(m) + "_" + str(i)] / clusters['er_hc_tt' +"_monthly_" + str(m)]

idx = clusters.columns.str.startswith('er_sch_')
clusters['er_sch_tt'] = clusters.iloc[:,idx].sum(axis=1) 

for m in range(1, 13, 1):
    idx = clusters.columns.str.startswith('er_sch_' + str(m))
    clusters['er_sch_tt' +"_monthly_" + str(m)] = clusters.iloc[:,idx].iloc[:,0:24].sum(axis=1) 

for m in range(1, 13, 1):
    for i in range(0, 24, 1):
        clusters['er_sch_' + str(m) + "_" + str(i)] = clusters['er_sch_' + str(m) + "_" + str(i)] / clusters['er_sch_tt' +"_monthly_" + str(m)]

filter_col = [col for col in clusters if col.startswith('er_sch') or col.startswith('er_hc')]
filter_col.insert(0, "id")

clusters = clusters[filter_col]

clusters = clusters.fillna(0)

# Write to csv file
clusters.to_csv(processed_folder + 'clusters_16.csv')

clusters = QgsVectorLayer(processed_folder + 'clusters_final.gpkg',"","ogr")
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_final.csv', 'CP1250', clusters.crs(), 'CSV')

#Write to raster for inputting into EU-JRC
clusters = pandas.read_csv(processed_folder + 'clusters_final.csv')
filter_col1 = [col for col in clusters if col.startswith('er_')]
filter_col2 = [col for col in clusters if col.startswith('CROPPROC')]
filter_col3 = [col for col in clusters if col.startswith('PerHHD')]

filter_col1.append(filter_col2)
filter_col1.append(filter_col3)

clusters = QgsVectorLayer(home_repo_folder + 'clusters_final.gpkg',"","ogr")

for k in filter_col1:
    processing.run("gdal:rasterize", {'INPUT':clusters,'FIELD':k,'BURN':None,'UNITS':1,'WIDTH':0.5,'HEIGHT':0.5,'EXTENT':'33.89999999645014,41.89166663115139,-4.700000001149985,5.499999958050098 [EPSG:4326]','NODATA':-1,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'OUTPUT': processed_folder + str(k) + ".tif"})

# import glob
# list = glob.glob(processed_folder + 'clusters*.gpkg')
# for f in list:
    # os.remove(f)
