# PrElGen v0.2
# Giacomo Falchetta, Paolo Cornali, Davide Mazzoni, Nicolò Stevanato
# Version: 24/10/2019

# Prepare csv for OnSSET using 'xxxx_HRSL_All_Cells.csv' convention

#########################
# Preamble
########################

# The manual_parameters must be set manually before running this script
#from manual_parameters import *

# Load required libraries
#from backend import *

gadm0 = QgsVectorLayer(input_folder + 'gadm36_' + countryiso3 + '_0.shp',"","ogr")

# Define clusters generated in PrElGen

##############fix filenames ######################

clusters_final = QgsVectorLayer(home_repo_folder + 'clusters_final.gpkg',"","ogr")

processing.run("native:reprojectlayer", {'INPUT':clusters_final,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),'OUTPUT':processed_folder + 'clusters_final_projected.gpkg'})

clusters_final = QgsVectorLayer(processed_folder + 'clusters_final_projected.gpkg',"","ogr")

# Define input files for the supply side (energy)
elevation = QgsRasterLayer(home_repo_folder + r'/onsset/input/elevation.tif')
ghi = QgsRasterLayer(home_repo_folder + r'/onsset/input/ghi.tif')
travel = QgsRasterLayer(home_repo_folder + r'/onsset/input/travel.tif')
windvel = QgsRasterLayer(home_repo_folder + r'/onsset/input/windvel.tif')
land_cover = QgsRasterLayer(home_repo_folder + r'/onsset/input/land_cover.tif')
night_ligths = QgsRasterLayer(home_repo_folder + r'/onsset/input/nightlights.tif')
urban_rural = QgsRasterLayer(home_repo_folder + r'/onsset/input/ghs_layer_smod_2015.tif')

substations = QgsVectorLayer(home_repo_folder + r'/onsset/input/substations.shp', "", "ogr")
#transformers = QgsVectorLayer(home_repo_folder + r'/onsset/input/transformers.shp', "", "ogr")
existing_HV = QgsVectorLayer(home_repo_folder + r'/onsset/input/existing_HV.shp', "", "ogr")
existing_MV = QgsVectorLayer(home_repo_folder + r'/onsset/input/existing_MV.shp', "", "ogr")
planned_HV = QgsVectorLayer(home_repo_folder + r'/onsset/input/planned_HV.shp', "", "ogr")
#planned_MV = QgsVectorLayer(home_repo_folder + r'/onsset/input/planned_MV.shp', "", "ogr")
roads = QgsVectorLayer(home_repo_folder + r'/onsset/input/roads.shp', "", "ogr")
hydro_points = QgsVectorLayer(home_repo_folder + r'/onsset/input/hydro_points.shp', "", "ogr")

# None layers
transformers = None
planned_MV = None

workspace = home_repo_folder + r'/onsset/input/'
settlements_fc = countryiso3
projCord = 'EPSG:3395'
hydropowerField = 'PowerMW'
hydropowerFieldUnit = 'MW'  # ["W", "kW", "MW"]

# Run data preparation script (credits to Babak Khavari, KTH https://github.com/KTH-dESA/Cluster-based_extraction_OnSSET)

sys.path.insert(0, './onsset/prepare')

# Prepare data for OnSSET
import os.path

# Create folder structure
if not os.path.exists(workspace + r"/Assist"):
    os.makedirs(workspace + r"/Assist")

if not os.path.exists(workspace + r"/Assist2"):
    os.makedirs(workspace + r"/Assist2")

if not os.path.exists(workspace + r"/DEM"):
    os.makedirs(workspace + r"/DEM")

if not os.path.exists(workspace + r"/Hydropower"):
    os.makedirs(workspace + r"/Hydropower")

if not os.path.exists(workspace + r"/Land_Cover"):
    os.makedirs(workspace + r"/Land_Cover")

if not os.path.exists(workspace + r"/Customimized demand"):
    os.makedirs(workspace + r"/Customimized demand")

if not os.path.exists(workspace + r"/Population_2015"):
    os.makedirs(workspace + r"/Population_2015")

if not os.path.exists(workspace + r"/Roads"):
    if roads != None:
        os.makedirs(workspace + r"/Roads")

if not os.path.exists(workspace + r"/Slope"):
    os.makedirs(workspace + r"/Slope")

if not os.path.exists(workspace + r"/Solar"):
    os.makedirs(workspace + r"/Solar")

if not os.path.exists(workspace + r"/Transformers"):
    if transformers != None:
        os.makedirs(workspace + r"/Transformers")

if not os.path.exists(workspace + r"/Substations"):
    if substations != None:
        os.makedirs(workspace + r"/Substations")

if not os.path.exists(workspace + r"/HV_Network"):
    if planned_HV or existing_HV != None:
        os.makedirs(workspace + r"/HV_Network")

if not os.path.exists(workspace + r"/MV_Network"):
    if planned_MV or existing_MV != None:
        os.makedirs(workspace + r"/MV_Network")

if not os.path.exists(workspace + r"/Travel_time"):
    os.makedirs(workspace + r"/Travel_time")

if not os.path.exists(workspace + r"/Wind"):
    os.makedirs(workspace + r"/Wind")

if not os.path.exists(workspace + r"/Night_lights"):
    os.makedirs(workspace + r"/Night_lights")

# Define assisting folder
assistingFolder = workspace + r"/Assist"
assistingFolder2 = workspace + r"/Assist2"

# Administrative boundaries
admin = gadm0

# Population clusters
Pop = clusters_final

# Define the extent of the clusters shapefile

ext = admin.extent()

xmin = ext.xMinimum() - 1
xmax = ext.xMaximum() + 1
ymin = ext.yMinimum() - 1
ymax = ext.yMaximum() + 1

coords = '{},{},{},{}'.format(xmin, xmax, ymin, ymax)

slope = 'slope'

#########################
# Centroids and points stuff
########################
processing.run('native:reprojectlayer', {'INPUT' : Pop, 'TARGET_CRS': 'EPSG:3395', 'OUTPUT' : home_repo_folder + 'clusters_final_reprojected.gpkg'})

Pop = QgsVectorLayer(home_repo_folder + 'clusters_final_reprojected.gpkg',"","ogr")

for field in Pop.fields():
    if field.name() == 'popsum':
        with edit(Pop):
            idx = Pop.fields().indexFromName(field.name())
            Pop.renameAttribute(idx, 'pop2015' + countryiso3)

print('Creating point layer for clusters larger than one sq. km. (100 ha)', 'Time:', datetime.datetime.now().time())
processing.run("qgis:selectbyexpression", {
    'INPUT': Pop, 'EXPRESSION': '\"Area\">=100', 'METHOD': 0})

processing.run("native:saveselectedfeatures", {
    'INPUT': Pop,
    'OUTPUT': workspace + r'/Population_2015/pop2015_large.shp'})

processing.run("qgis:pointsalonglines", {
    'INPUT': workspace + r'/Population_2015/pop2015_large.shp',
    'DISTANCE': 1000, 'START_OFFSET': 0, 'END_OFFSET': 0,
    'OUTPUT': assistingFolder + r"/virtualpoints.shp"})

settlement_points = QgsVectorLayer(assistingFolder + r'/virtualpoints.shp', '', 'ogr')

print('Creating point layer for clusters smaller than one sq. km. (100 ha)', 'Time:', datetime.datetime.now().time())
processing.run("qgis:selectbyexpression", {
    'INPUT': Pop, 'EXPRESSION': '\"Area\"<100', 'METHOD': 0})

processing.run("native:saveselectedfeatures", {
    'INPUT': Pop,
    'OUTPUT': workspace + r'/Population_2015/pop2015_small.shp'})

processing.run("native:centroids", {
    'INPUT': workspace + r'/Population_2015/pop2015_small.shp',
    'ALL_PARTS': False, 'OUTPUT': assistingFolder + r'/centerpoints.shp'})

centerpoints = QgsVectorLayer(assistingFolder + r'/centerpoints.shp', "" "ogr")

#########################
# Rasters processing
########################
print('Processing the DEM and slope maps.', 'Time:', datetime.datetime.now().time())
processing.run("gdal:cliprasterbyextent",
               {'INPUT': elevation, 'PROJWIN': coords, 'NODATA': None,
                'OPTIONS': '', 'DATA_TYPE': 5,
                'OUTPUT': workspace + r'/DEM/elevation_' + countryiso3 + '.tif'})
processing.run("gdal:slope",
               {'INPUT': workspace + r'/DEM/elevation_' + countryiso3 + '.tif', 'BAND': 1,
                'SCALE': 111120, 'AS_PERCENT': False, 'COMPUTE_EDGES': False, 'ZEVENBERGEN': False,
                'OPTIONS': '',
                'OUTPUT': workspace + r"/Slope/slope_" + countryiso3 + ".tif"})
processing.run("gdal:fillnodata",
               {'INPUT': workspace + r"/Slope/slope_" + countryiso3 + ".tif", 'BAND': 1,
                'DISTANCE': 50, 'ITERATIONS': 0, 'NO_MASK': False, 'MASK_LAYER': None,
                'OUTPUT': assistingFolder2 + r'/' + slope + ".tif"})
processing.run("gdal:fillnodata",
               {'INPUT': workspace + r'/DEM/elevation_' + countryiso3 + '.tif', 'BAND': 1,
                'DISTANCE': 50, 'ITERATIONS': 0, 'NO_MASK': False, 'MASK_LAYER': None,
                'OUTPUT': assistingFolder2 + r'/elevation.tif'})
processing.run("gdal:warpreproject",
               {'INPUT': assistingFolder2 + r'/' + slope + ".tif", 'SOURCE_CRS': None,
                'TARGET_CRS': projCord, 'RESAMPLING': 0,
                'DATA_TYPE': 6, 'MULTITHREADING': False,
                'OUTPUT': workspace + r'/Slope/slope_' + countryiso3 + '_Proj.tif'})
processing.run("gdal:warpreproject",
               {'INPUT': assistingFolder2 + r'/elevation.tif',
                'SOURCE_CRS': None, 'TARGET_CRS': projCord, 'NODATA': 0, 'TARGET_RESOLUTION': 0,
                'OPTIONS': '', 'RESAMPLING': 0, 'DATA_TYPE': 5, 'TARGET_EXTENT': None,
                'TARGET_EXTENT_CRS': None, 'MULTITHREADING': False,
                'OUTPUT': workspace + r'/DEM/elevation' + countryiso3 + '_Proj.tif'})

print('Processing the GHI map.', 'Time:', datetime.datetime.now().time())
processing.run("gdal:cliprasterbyextent",
               {'INPUT': ghi, 'PROJWIN': coords, 'NODATA': None,
                'OPTIONS': '', 'DATA_TYPE': 5,
                'OUTPUT': workspace + r'/Solar/ghi_' + countryiso3 + '.tif'})
processing.run("gdal:fillnodata",
               {'INPUT': workspace + r'/Solar/ghi_' + countryiso3 + '.tif', 'BAND': 1,
                'DISTANCE': 50, 'ITERATIONS': 0, 'NO_MASK': False, 'MASK_LAYER': None,
                'OUTPUT': assistingFolder2 + r'/ghi.tif'})
processing.run("gdal:warpreproject",
               {'INPUT': assistingFolder2 + r'/ghi.tif', 'SOURCE_CRS': None,
                'TARGET_CRS': projCord, 'NODATA': 0, 'TARGET_RESOLUTION': 0, 'OPTIONS': '', 'RESAMPLING': 0,
                'DATA_TYPE': 5, 'TARGET_EXTENT': None, 'TARGET_EXTENT_CRS': None, 'MULTITHREADING': False,
                'OUTPUT': workspace + r'/Solar/ghi_' + countryiso3 + '_Proj.tif'})
print('Processing the traveltime map.', 'Time:', datetime.datetime.now().time())
processing.run("gdal:cliprasterbyextent",
               {'INPUT': travel, 'PROJWIN': coords, 'NODATA': None,
                'OPTIONS': '', 'DATA_TYPE': 5,
                'OUTPUT': workspace + r'/Travel_time/travel_' + countryiso3 + '.tif'})
processing.run("gdal:fillnodata",
               {'INPUT': workspace + r'/Travel_time/travel_' + countryiso3 + '.tif',
                'BAND': 1, 'DISTANCE': 50, 'ITERATIONS': 0, 'NO_MASK': False, 'MASK_LAYER': None,
                'OUTPUT': assistingFolder2 + r'/travel.tif'})
processing.run("gdal:warpreproject",
               {'INPUT': assistingFolder2 + r'/travel.tif',
                'SOURCE_CRS': None, 'TARGET_CRS': projCord, 'NODATA': 0, 'TARGET_RESOLUTION': 0,
                'OPTIONS': '', 'RESAMPLING': 0, 'DATA_TYPE': 5, 'TARGET_EXTENT': None,
                'TARGET_EXTENT_CRS': None, 'MULTITHREADING': False,
                'OUTPUT': workspace + r'/Travel_time/travel_' + countryiso3 + '_Proj.tif'})
print('Processing the wind speed map.', 'Time:', datetime.datetime.now().time())
processing.run("gdal:cliprasterbyextent",
               {'INPUT': windvel, 'PROJWIN': coords, 'NODATA': None,
                'OPTIONS': '', 'DATA_TYPE': 5,
                'OUTPUT': workspace + r'/Wind/windvel_' + countryiso3 + '.tif'})
processing.run("gdal:fillnodata",
               {'INPUT': workspace + r'/Wind/windvel_' + countryiso3 + '.tif', 'BAND': 1,
                'DISTANCE': 50, 'ITERATIONS': 0, 'NO_MASK': False, 'MASK_LAYER': None,
                'OUTPUT': assistingFolder2 + r'/windvel.tif'})
processing.run("gdal:warpreproject",
               {'INPUT': assistingFolder2 + r'/windvel.tif', 'SOURCE_CRS': None,
                'TARGET_CRS': projCord, 'NODATA': 0, 'TARGET_RESOLUTION': 0, 'OPTIONS': '', 'RESAMPLING': 0,
                'DATA_TYPE': 5, 'TARGET_EXTENT': None, 'TARGET_EXTENT_CRS': None, 'MULTITHREADING': False,
                'OUTPUT': workspace + r'/Wind/windvel_' + countryiso3 + '_Proj.tif'})
print('Processing the landcover map.', 'Time:', datetime.datetime.now().time())
processing.run("gdal:cliprasterbyextent",
               {'INPUT': land_cover, 'PROJWIN': coords, 'NODATA': None, 'OPTIONS': '', 'DATA_TYPE': 5,
                'OUTPUT': workspace + r'/Land_Cover/land_cover_' + countryiso3 + '.tif'})
parameters = {'INPUT_A': workspace + r'/Land_Cover/land_cover_' + countryiso3 + '.tif',
              'BAND_A': 1,
              'FORMULA': '(A/(A>-1))',
              'OUTPUT': workspace + r'/Land_Cover/land_cover_' + countryiso3 + '2.tif'}
processing.run('gdal:rastercalculator', parameters)
processing.run("gdal:warpreproject",
               {'INPUT': workspace + r'/Land_Cover/land_cover_' + countryiso3 + '2.tif',
                'SOURCE_CRS': None, 'TARGET_CRS': projCord,
                'RESAMPLING': 0, 'DATA_TYPE': 5, 'MULTITHREADING': False,
                'OUTPUT': workspace + r'/Land_Cover/land_cover_' + countryiso3 + '_Proj.tif'})
print('Processing the night ligths map.', 'Time:', datetime.datetime.now().time())
processing.run("gdal:cliprasterbyextent",
               {'INPUT': night_ligths, 'PROJWIN': coords, 'NODATA': None,
                'OPTIONS': '', 'DATA_TYPE': 5,
                'OUTPUT': workspace + r'/Night_lights/night_lights_' + countryiso3 + '.tif'})
processing.run("gdal:fillnodata",
               {'INPUT': workspace + r'/Night_lights/night_lights_' + countryiso3 + '.tif', 'BAND': 1,
                'DISTANCE': 50, 'ITERATIONS': 0, 'NO_MASK': False, 'MASK_LAYER': None,
                'OUTPUT': assistingFolder2 + r'/nightlights.tif'})
processing.run("gdal:warpreproject",
               {'INPUT': assistingFolder2 + r'/nightlights.tif', 'SOURCE_CRS': None,
                'TARGET_CRS': projCord, 'NODATA': 0, 'TARGET_RESOLUTION': 0, 'OPTIONS': '', 'RESAMPLING': 0,
                'DATA_TYPE': 5, 'TARGET_EXTENT': None, 'TARGET_EXTENT_CRS': None, 'MULTITHREADING': False,
                'OUTPUT': workspace + r'/Night_lights/night_lights_' + countryiso3 + '_Proj.tif'})
#shutil.rmtree(workspace + r"/Assist2")
#os.makedirs(workspace + r"/Assist2")
#assistingFolder2 = workspace + r"/Assist2"

traveltime = QgsRasterLayer(workspace + r'/Travel_time/travel_' + countryiso3 + '_Proj.tif', 'traveltime')
windvel = QgsRasterLayer(workspace + r'/Wind/windvel_' + countryiso3 + '_Proj.tif', 'windvel')
solar = QgsRasterLayer(workspace + r'/Solar/ghi_' + countryiso3 + '_Proj.tif', 'solar')
elevation = QgsRasterLayer(workspace + r'/DEM/elevation' + countryiso3 + '_Proj.tif', 'elevation')
slope = QgsRasterLayer(workspace + r'/Slope/' + 'slope_' + countryiso3 + '_Proj.tif', 'slope')
landcover = QgsRasterLayer(workspace + r'/Land_Cover/land_cover_' + countryiso3 + '_Proj.tif', 'landcover')
night_ligths = QgsRasterLayer(workspace + r'/Night_lights/night_lights_' + countryiso3 + '_Proj.tif', 'nightlights')
print('Add wind speeds to the clusters.', 'Time:', datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': windvel, 'RASTER_BAND': 1, 'INPUT_VECTOR': Pop,
                                        'COLUMN_PREFIX': 'windveloci', 'STATS': [2]})
print('Add GHI to the clusters.', 'Time:', datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': solar, 'RASTER_BAND': 1, 'INPUT_VECTOR': Pop,
                                        'COLUMN_PREFIX': 'ghisolarad', 'STATS': [2]})
print('Add travel time to the clusters.', 'Time:', datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': traveltime, 'RASTER_BAND': 1, 'INPUT_VECTOR': Pop,
                                        'COLUMN_PREFIX': 'traveltime', 'STATS': [2]})
print('Add elevation to the clusters.', 'Time:', datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': elevation, 'RASTER_BAND': 1, 'INPUT_VECTOR': Pop,
                                        'COLUMN_PREFIX': 'elevationm', 'STATS': [2]})
print('Add slope to the clusters.', 'Time:', datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': slope, 'RASTER_BAND': 1, 'INPUT_VECTOR': Pop,
                                        'COLUMN_PREFIX': 'terraslope', 'STATS': [9]})
print('Add land cover to the clusters.', 'Time:', datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': landcover, 'RASTER_BAND': 1, 'INPUT_VECTOR': Pop,
                                        'COLUMN_PREFIX': 'landcoverm', 'STATS': [9]})
print('Add night lights to the clusters.', 'Time:', datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {'INPUT_RASTER': night_ligths, 'RASTER_BAND': 1, 'INPUT_VECTOR': Pop,
                                        'COLUMN_PREFIX': 'nightlight', 'STATS': [6]})
input = Pop

########################
# Vectors
########################

#########
# Substations
#########
if substations != None:
    print('Processing the substations.', 'Time:', datetime.datetime.now().time())
    processing.run("native:clip", {'INPUT': substations, 'OVERLAY': admin, 'OUTPUT': workspace + r'/Substations/Substations' + countryiso3 + '.shp'})
    processing.run("qgis:fieldcalculator", {'INPUT': workspace + r'/Substations/Substations' + countryiso3 + '.shp', 'FIELD_NAME': 'AUTO', 'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA': ' $id', 'OUTPUT': workspace + r'/Substations/Substations_with_ID.shp'})
    processing.run("native:reprojectlayer", {'INPUT': workspace + r'/Substations/Substations_with_ID.shp', 'TARGET_CRS': projCord, 'OUTPUT': workspace + r'/Substations/Substations' + countryiso3 + '_Proj.shp'})
    # Give all intersecting polygon distance 0
    processing.run("native:selectbylocation", {'INPUT': Pop, 'PREDICATE': [0],
                                               'INTERSECT': workspace + r'/Substations/Substations' + countryiso3 + '_Proj.shp', 'METHOD': 0})
    processing.run("native:saveselectedfeatures", {'INPUT': Pop, 'OUTPUT': assistingFolder2 + r'/sub_int.shp'})
    processing.run("qgis:fieldcalculator", {'INPUT': assistingFolder2 + r'/sub_int.shp', 'FIELD_NAME': 'Substation', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': True, 'FORMULA': '0', 'OUTPUT': assistingFolder2 + r'/Substations_intersect.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': Pop, 'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/Substations_intersect.shp', 'FIELD_2': 'id', 'FIELDS_TO_COPY': ['Substation'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '', 'OUTPUT': assistingFolder2 + r'/Substationdist_intersecting.shp'})
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': settlement_points,
                                                       'HUBS': workspace + r'/Substations/Substations' + countryiso3 + '_Proj.shp', 'FIELD': 'AUTO', 'UNIT': 3, 'OUTPUT': assistingFolder2 + r"\Substationdist.shp"})
    processing.run("qgis:statisticsbycategories", {
        'INPUT': assistingFolder2 + r"\Substationdist.shp", 'VALUES_FIELD_NAME': 'HubDist', 'CATEGORIES_FIELD_NAME': ['id'], 'OUTPUT': assistingFolder2 + r'/Substationdist_largerThanOne_sta.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/Substationdist_intersecting.shp', 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Substationdist_largerThanOne_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '', 'OUTPUT': assistingFolder2 + r'/Substationdist_largerThanOne.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Substationdist_largerThanOne.shp',
        'FIELD_NAME': 'Substation', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"Substation\" IS NULL, represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/Substationdist_largerThanOne_andIntersect.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': centerpoints,
                                                       'HUBS': workspace + r'/Substations/Substations' + countryiso3 + '_Proj.shp', 'FIELD': 'AUTO', 'UNIT': 3, 'OUTPUT': assistingFolder2 + r'/Substationdist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/Substationdist_largerThanOne_andIntersect.shp', 'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/Substationdist_smallerThanOne.shp', 'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '', 'OUTPUT': assistingFolder2 + r'/Substationdistplaceholder.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Substationdistplaceholder.shp',
        'FIELD_NAME': 'Substation', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"Substation\" is NULL, \"HubDist\",\"Substation\")',
        'OUTPUT': assistingFolder2 + r'/Substationdist_2.shp'})
    sub_dist = QgsVectorLayer(assistingFolder2 + r'/Substationdist_2.shp', '', 'ogr')
    processing.run("qgis:deletecolumn", {
        'INPUT': sub_dist,
        'COLUMN': ['min', 'HubDist'],
        'OUTPUT': workspace + r'/Substations/Substationdist.shp'})
    sub_dist = QgsVectorLayer(workspace + r'/Substations/Substationdist.shp', '', 'ogr')
    input = sub_dist
    #shutil.rmtree(workspace + r"/Assist2")
    #os.makedirs(workspace + r"/Assist2")
    #assistingFolder2 = workspace + r"/Assist2"

#########
# Transformers
#########
if transformers != None:
    print('Processing the transformers.' 'Time:', datetime.datetime.now().time())
    # TRANSFORMERS
    processing.run("native:clip",
                   {'INPUT': transformers, 'OVERLAY': admin,
                    'OUTPUT': workspace + r'/Transformers/Transformers' + countryiso3 + '.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': workspace + r'/Transformers/Transformers' + countryiso3 + '.shp', 'FIELD_NAME': 'AUTO',
                    'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA': ' $id',
                    'OUTPUT': workspace + r'/Transformers/Transformers_with_ID.shp'})
    processing.run("native:reprojectlayer",
                   {'INPUT': workspace + r'/Transformers/Transformers_with_ID.shp', 'TARGET_CRS': projCord,
                    'OUTPUT': workspace + r'/Transformers/Transformers' + countryiso3 + '_Proj.shp'})
    if substations == None:
        input = Pop
    else:
        input = sub_dist
    # Give all intersecting polygon distance 0
    processing.run("native:selectbylocation",
                   {'INPUT': Pop, 'PREDICATE': [0],
                    'INTERSECT': workspace + r'/Transformers/Transformers' + countryiso3 + '_Proj.shp',
                    'METHOD': 0})
    processing.run("native:saveselectedfeatures", {'INPUT': Pop, 'OUTPUT': assistingFolder2 + r'/trans_int.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': assistingFolder2 + r'/trans_int.shp', 'FIELD_NAME': 'Transforme', 'FIELD_TYPE': 0,
                    'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
                    'NEW_FIELD': True, 'FORMULA': '0', 'OUTPUT': assistingFolder2 + r'/Transformers_intersect.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': input, 'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/Transformers_intersect.shp', 'FIELD_2': 'id',
        'FIELDS_TO_COPY': ['Transforme'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/Transformerdist_intersecting.shp'})
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': settlement_points,
                                                       'HUBS': workspace + r'/Transformers/Transformers' + countryiso3 + '_Proj.shp',
                                                       'FIELD': 'AUTO', 'UNIT': 3,
                                                       'OUTPUT': assistingFolder2 + r"\Transformerdist.shp"})
    processing.run("qgis:statisticsbycategories", {
        'INPUT': assistingFolder2 + r"\Transformerdist.shp", 'VALUES_FIELD_NAME': 'HubDist',
        'CATEGORIES_FIELD_NAME': ['id'],
        'OUTPUT': assistingFolder2 + r'/Transformerdist_largerThanOne_sta.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/Transformerdist_intersecting.shp', 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Transformerdist_largerThanOne_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/Transformerdist_largerThanOne.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Transformerdist_largerThanOne.shp',
        'FIELD_NAME': 'Transforme', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"Transforme\" IS NULL, represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/Transformerdist_largerThanOne_andIntersect.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': centerpoints,
                                                       'HUBS': workspace + r'/Transformers/Transformers' + countryiso3 + '_Proj.shp',
                                                       'FIELD': 'AUTO', 'UNIT': 3,
                                                       'OUTPUT': assistingFolder2 + r'/Transformerdist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/Transformerdist_largerThanOne_andIntersect.shp', 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Transformerdist_smallerThanOne.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/Transformerdistplaceholder.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Transformerdistplaceholder.shp',
        'FIELD_NAME': 'Transforme', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"Transforme\" IS NULL,\"HubDist\",\"Transforme\")',
        'OUTPUT': assistingFolder2 + r'/Transformerdist_2.shp'})
    trans_dist = QgsVectorLayer(assistingFolder2 + r'/Transformerdist_2.shp', '', 'ogr')
    processing.run("qgis:deletecolumn", {
        'INPUT': trans_dist,
        'COLUMN': ['min', 'HubDist'],
        'OUTPUT': workspace + r'/Transformers/Transformerdist.shp'})
    trans_dist = QgsVectorLayer(workspace + r'/Transformers/Transformerdist.shp', '', 'ogr')
    input = trans_dist
    #shutil.rmtree(workspace + r"/Assist2")
    #os.makedirs(workspace + r"/Assist2")
    #assistingFolder2 = workspace + r"/Assist2"


#########
# Existing HV lines
#########
if existing_HV != None:
    print('Processing the exisitng high-voltage tranmission lines.', 'Time:', datetime.datetime.now().time())
    processing.run("native:clip", {'INPUT': existing_HV, 'OVERLAY': admin,
                                   'OUTPUT': workspace + r'/HV_Network/Existing_HV' + countryiso3 + '.shp'})
    processing.run("saga:convertlinestopoints", {'LINES': workspace + r'/HV_Network/Existing_HV' + countryiso3 + '.shp',
                                                 'ADD         ': True, 'DIST': 0.000833333333,
                                                 'POINTS': workspace + r'/HV_Network/Existing_HV' + countryiso3 + 'Point.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': workspace + r'/HV_Network/Existing_HV' + countryiso3 + 'Point.shp',
                    'FIELD_NAME': 'AUTO', 'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True,
                    'FORMULA': ' $id', 'OUTPUT': workspace + r'/HV_Network/Existing_HV_with_ID.shp'})
    processing.run("native:reprojectlayer",
                   {'INPUT': workspace + r'/HV_Network/Existing_HV_with_ID.shp', 'TARGET_CRS': projCord,
                    'OUTPUT': workspace + r'/HV_Network/Existing_HV' + countryiso3 + '_Proj.shp'})
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': settlement_points,
                                                       'HUBS': workspace + r'/HV_Network/Existing_HV' + countryiso3 + '_Proj.shp',
                                                       'FIELD': 'AUTO', 'UNIT': 3,
                                                       'OUTPUT': assistingFolder2 + r"\EX_HV_dist.shp"})
    processing.run("qgis:statisticsbycategories", {
        'INPUT': assistingFolder2 + r"\EX_HV_dist.shp", 'VALUES_FIELD_NAME': 'HubDist', 'CATEGORIES_FIELD_NAME': ['id'],
        'OUTPUT': assistingFolder2 + r'/EX_HV_dist_largerThanOne_sta.shp'})
    if transformers == None and substations == None:
        input = Pop
    elif transformers == None:
        input = sub_dist
    else:
        input = trans_dist
    processing.run("native:joinattributestable", {
        'INPUT': input, 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/EX_HV_dist_largerThanOne_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/EX_HV_dist_largerThanOne.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/EX_HV_dist_largerThanOne.shp',
        'FIELD_NAME': 'EX_HV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"EX_HV\" IS NULL, represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/EX_HV_dist_largerThanOne_andIntersect.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints", {
        'INPUT': centerpoints,
        'HUBS': workspace + r'/HV_Network/Existing_HV' + countryiso3 + '_Proj.shp',
        'FIELD': 'AUTO', 'UNIT': 3,
        'OUTPUT': assistingFolder2 + r'/EX_HV_Dist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/EX_HV_Dist_largerThanOne_andIntersect.shp',
        'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/EX_HV_Dist_smallerThanOne.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/EX_HV_Distplaceholder.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/EX_HV_Distplaceholder.shp',
        'FIELD_NAME': 'EX_HV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"EX_HV\" IS NULL,\"HubDist\",\"EX_HV\")',
        'OUTPUT': assistingFolder2 + r'/EX_HV_Dist_placeholder_2.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/EX_HV_Dist_placeholder_2.shp',
        'FIELD_NAME': 'EX_HV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"EX_HV\" < 0.5, 0,\"EX_HV\")',
        'OUTPUT': assistingFolder2 + r'/EX_HV_dist_2.shp'})
    ex_hv = QgsVectorLayer(assistingFolder2 + r'/EX_HV_dist_2.shp', '', 'ogr')
    processing.run("qgis:deletecolumn", {
        'INPUT': ex_hv,
        'COLUMN': ['min', 'HubDist'],
        'OUTPUT': workspace + r'/HV_Network/Existing_HV_dist.shp'})
    ex_hv = QgsVectorLayer(workspace + r'/HV_Network/Existing_HV_dist.shp', '', 'ogr')
    input = ex_hv
    #shutil.rmtree(workspace + r"/Assist2")
    #os.makedirs(workspace + r"/Assist2")
    #assistingFolder2 = workspace + r"/Assist2"


#########
# Planned HV lines
#########
if planned_HV != None:
    print('Processing the planned high-voltage tranmission lines.', 'Time:', datetime.datetime.now().time())
    processing.run("native:clip",
                   {'INPUT': planned_HV, 'OVERLAY': admin,
                    'OUTPUT': workspace + r'/HV_Network/Planned_HV' + countryiso3 + '.shp'})
    if existing_HV != None:
        processing.run("native:mergevectorlayers", {'LAYERS': [
            workspace + r'/HV_Network/Existing_HV' + countryiso3 + '.shp',
            workspace + r'/HV_Network/Planned_HV' + countryiso3 + '.shp'],
            'CRS': None, 'OUTPUT': workspace + r'/HV_Network/Planned_HV' + countryiso3 + '_merged.shp'})
        merged_HV = QgsVectorLayer(workspace + r'/HV_Network/Planned_HV' + countryiso3 + '_merged.shp', '', 'ogr')
    else:
        merged_HV = QgsVectorLayer(workspace + r'/HV_Network/Planned_HV' + countryiso3 + '.shp', '', 'ogr')
    processing.run("saga:convertlinestopoints", {
        'LINES': merged_HV,
        'ADD         ': True, 'DIST': 0.000833333333,
        'POINTS': workspace + r'/HV_Network/Planned_HV' + countryiso3 + 'Point.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': workspace + r'/HV_Network/Planned_HV' + countryiso3 + 'Point.shp',
                    'FIELD_NAME': 'AUTO',
                    'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True,
                    'FORMULA': ' $id',
                    'OUTPUT': workspace + r'/HV_Network/Planned_HV_with_ID.shp'})
    processing.run("native:reprojectlayer",
                   {'INPUT': workspace + r'/HV_Network/Planned_HV_with_ID.shp',
                    'TARGET_CRS': projCord,
                    'OUTPUT': workspace + r'/HV_Network/Planned_HV' + countryiso3 + '_Proj.shp'})
    if existing_HV == None and transformers == None and substations == None:
        input = Pop
    elif existing_HV == None and transformers == None:
        input = sub_dist
    elif existing_HV == None:
        input = trans_dist
    else:
        input = ex_hv
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': settlement_points,
                                                       'HUBS': workspace + r'/HV_Network/Planned_HV' + settlements_fc[0:3] + '_Proj.shp',
                                                       'FIELD': 'AUTO', 'UNIT': 3,
                                                       'OUTPUT': assistingFolder2 + r"\PL_HV_dist.shp"})
    processing.run("qgis:statisticsbycategories", {
        'INPUT': assistingFolder2 + r"\PL_HV_dist.shp", 'VALUES_FIELD_NAME': 'HubDist',
        'CATEGORIES_FIELD_NAME': ['id'],
        'OUTPUT': assistingFolder2 + r'/PL_HV_dist_largerThanOne_sta.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': input, 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/PL_HV_dist_largerThanOne_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/PL_HV_dist_largerThanOne.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/PL_HV_dist_largerThanOne.shp',
        'FIELD_NAME': 'PL_HV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"PL_HV\" IS NULL, represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/PL_HV_dist_largerThanOne_andIntersect.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints", {
        'INPUT': centerpoints,
        'HUBS': workspace + r'/HV_Network/Planned_HV' + countryiso3 + '_Proj.shp',
        'FIELD': 'AUTO', 'UNIT': 3,
        'OUTPUT': assistingFolder2 + r'/PL_HV_Dist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/PL_HV_Dist_largerThanOne_andIntersect.shp',
        'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/PL_HV_Dist_smallerThanOne.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/PL_HV_Distplaceholder.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/PL_HV_Distplaceholder.shp',
        'FIELD_NAME': 'PL_HV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"PL_HV\" IS NULL,\"HubDist\", \"PL_HV\")',
        'OUTPUT': assistingFolder2 + r'/PL_HV_Dist_placeholder_2.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/PL_HV_Dist_placeholder_2.shp',
        'FIELD_NAME': 'PL_HV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"PL_HV\" < 0.5, 0,\"PL_HV\")',
        'OUTPUT': assistingFolder2 + r'/PL_HV_dist_2.shp'})
    pl_hv = QgsVectorLayer(assistingFolder2 + r'/PL_HV_dist_2.shp', '', 'ogr')
    processing.run("qgis:deletecolumn", {
        'INPUT': pl_hv,
        'COLUMN': ['min', 'HubDist'],
        'OUTPUT': workspace + r'/HV_Network/Planned_HV_dist.shp'})
    pl_hv = QgsVectorLayer(workspace + r'/HV_Network/Planned_HV_dist.shp', '', 'ogr')
    input = pl_hv
    #shutil.rmtree(workspace + r"/Assist2")
    #os.makedirs(workspace + r"/Assist2")
    #assistingFolder2 = workspace + r"/Assist2"

#########
# Existing MV lines
#########
if existing_MV != None:
    print('Processing the exisitng medium-voltage tranmission lines.', 'Time:', datetime.datetime.now().time())
    # Existing_MV_lines
    processing.run("native:clip",
                   {'INPUT': existing_MV, 'OVERLAY': admin,
                    'OUTPUT': workspace + r'/MV_Network/Existing_MV' + countryiso3 + '.shp'})
    processing.run("saga:convertlinestopoints", {
        'LINES': workspace + r'/MV_Network/Existing_MV' + countryiso3 + '.shp',
        'ADD         ': True, 'DIST': 0.000833333333,
        'POINTS': workspace + r'/MV_Network/Existing_MV' + countryiso3 + 'Point.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': workspace + r'/MV_Network/Existing_MV' + countryiso3 + 'Point.shp',
                    'FIELD_NAME': 'AUTO',
                    'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True,
                    'FORMULA': ' $id',
                    'OUTPUT': workspace + r'/MV_Network/Existing_MV_with_ID.shp'})
    processing.run("native:reprojectlayer",
                   {'INPUT': workspace + r'/MV_Network/Existing_MV_with_ID.shp',
                    'TARGET_CRS': projCord,
                    'OUTPUT': workspace + r'/MV_Network/Existing_MV' + countryiso3 + '_Proj.shp'})
    if existing_HV == None and planned_HV == None and transformers == None and substations == None:
        input = Pop
    elif existing_HV == None and planned_HV == None and transformers == None:
        input = sub_dist
    elif existing_HV == None and planned_HV == None:
        input = trans_dist
    elif planned_HV == None:
        input = ex_hv
    else:
        input = pl_hv
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': settlement_points,
                                                       'HUBS': workspace + r'/MV_Network/Existing_MV' + settlements_fc[0:3] + '_Proj.shp',
                                                       'FIELD': 'AUTO', 'UNIT': 3,
                                                       'OUTPUT': assistingFolder2 + r"\EX_MV_dist.shp"})
    processing.run("qgis:statisticsbycategories", {
        'INPUT': assistingFolder2 + r"\EX_MV_dist.shp", 'VALUES_FIELD_NAME': 'HubDist',
        'CATEGORIES_FIELD_NAME': ['id'],
        'OUTPUT': assistingFolder2 + r'/EX_MV_dist_largerThanOne_sta.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': input, 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/EX_MV_dist_largerThanOne_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/EX_MV_dist_largerThanOne.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/EX_MV_dist_largerThanOne.shp',
        'FIELD_NAME': 'EX_MV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"EX_MV\" IS NULL, represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/EX_MV_dist_largerThanOne_andIntersect.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints", {
        'INPUT': centerpoints,
        'HUBS': workspace + r'/MV_Network/Existing_MV' + countryiso3 + '_Proj.shp',
        'FIELD': 'AUTO', 'UNIT': 3,
        'OUTPUT': assistingFolder2 + r'/EX_MV_Dist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/EX_MV_Dist_largerThanOne_andIntersect.shp',
        'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/EX_MV_Dist_smallerThanOne.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/EX_MV_Distplaceholder.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/EX_MV_Distplaceholder.shp',
        'FIELD_NAME': 'EX_MV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"EX_MV\" IS NULL,\"HubDist\",\"EX_MV\")',
        'OUTPUT': assistingFolder2 + r'/EX_MV_Dist_placeholder_2.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/EX_MV_Dist_placeholder_2.shp',
        'FIELD_NAME': 'EX_MV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"EX_MV\" < 0.5, 0,\"EX_MV\")',
        'OUTPUT': assistingFolder2 + r'/EX_MV_dist_2.shp'})
    ex_mv = QgsVectorLayer(assistingFolder2 + r'/EX_MV_dist_2.shp', '', 'ogr')
    processing.run("qgis:deletecolumn", {
        'INPUT': ex_mv,
        'COLUMN': ['min', 'HubDist'],
        'OUTPUT': workspace + r'/MV_Network/Existing_MV_dist.shp'})
    ex_mv = QgsVectorLayer(workspace + r'/MV_Network/Existing_MV_dist.shp', '', 'ogr')
    input = ex_mv
    #shutil.rmtree(workspace + r"/Assist2")
    #os.makedirs(workspace + r"/Assist2")
    #assistingFolder2 = workspace + r"/Assist2"

###############
# Planned MV lines
##############à
if planned_MV != None:
    print('Processing the planned medium-voltage tranmission lines.', 'Time:', datetime.datetime.now().time())
    # Planned_MV_lines
    processing.run("native:clip",
                   {'INPUT': planned_MV, 'OVERLAY': admin,
                    'OUTPUT': workspace + r'/MV_Network/Planned_MV' + countryiso3 + '.shp'})
    if existing_MV != None:
        processing.run("native:mergevectorlayers", {'LAYERS': [
            workspace + r'/MV_Network/Existing_MV' + countryiso3 + '.shp',
            workspace + r'/MV_Network/Planned_MV' + countryiso3 + '.shp'],
            'CRS': None,
            'OUTPUT': workspace + r'/MV_Network/Planned_MV' + countryiso3 + '_merged.shp'})
        merged_MV = QgsVectorLayer(
            workspace + r'/MV_Network/Planned_MV' + countryiso3 + '_merged.shp', '', 'ogr')
    else:
        merged_MV = QgsVectorLayer(workspace + r'/MV_Network/Planned_MV' + countryiso3 + '.shp', '',
                                   'ogr')
    processing.run("saga:convertlinestopoints", {
        'LINES': merged_MV,
        'ADD         ': True, 'DIST': 0.000833333333,
        'POINTS': workspace + r'/MV_Network/Planned_MV' + countryiso3 + 'Point.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': workspace + r'/MV_Network/Planned_MV' + countryiso3 + 'Point.shp',
                    'FIELD_NAME': 'AUTO',
                    'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True,
                    'FORMULA': ' $id',
                    'OUTPUT': workspace + r'/MV_Network/Planned_MV_with_ID.shp'})
    processing.run("native:reprojectlayer",
                   {'INPUT': workspace + r'/MV_Network/Planned_MV_with_ID.shp',
                    'TARGET_CRS': projCord,
                    'OUTPUT': workspace + r'/MV_Network/Planned_MV' + countryiso3 + '_Proj.shp'})
    if existing_MV == None and planned_HV == None and existing_HV == None and transformers == None \
            and substations == None:
        input = Pop
    elif existing_MV == None and planned_HV == None and existing_HV == None and transformers == None:
        input = sub_dist
    elif existing_MV == None and planned_HV == None and existing_HV == None:
        input = trans_dist
    elif existing_MV == None and planned_HV == None:
        input = ex_hv
    elif existing_MV == None:
        input = pl_hv
    else:
        input = ex_mv
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': settlement_points,
                                                       'HUBS': workspace + r'/MV_Network/Planned_MV' + settlements_fc[
                                                                                                       0:3] + '_Proj.shp',
                                                       'FIELD': 'AUTO', 'UNIT': 3,
                                                       'OUTPUT': assistingFolder2 + r"\PL_MV_dist.shp"})
    processing.run("qgis:statisticsbycategories", {
        'INPUT': assistingFolder2 + r"\PL_MV_dist.shp", 'VALUES_FIELD_NAME': 'HubDist',
        'CATEGORIES_FIELD_NAME': ['id'],
        'OUTPUT': assistingFolder2 + r'/PL_MV_dist_largerThanOne_sta.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': input, 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/PL_MV_dist_largerThanOne_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/PL_MV_dist_largerThanOne.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/PL_MV_dist_largerThanOne.shp',
        'FIELD_NAME': 'PL_MV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"PL_MV\" IS NULL, represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/PL_MV_dist_largerThanOne_andIntersect.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints", {
        'INPUT': centerpoints,
        'HUBS': workspace + r'/MV_Network/Planned_MV' + countryiso3 + '_Proj.shp',
        'FIELD': 'AUTO', 'UNIT': 3,
        'OUTPUT': assistingFolder2 + r'/PL_MV_Dist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/PL_MV_Dist_largerThanOne_andIntersect.shp',
        'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/PL_MV_Dist_smallerThanOne.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/PL_MV_Distplaceholder.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/PL_MV_Distplaceholder.shp',
        'FIELD_NAME': 'PL_MV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"PL_MV\" IS NULL,\"HubDist\",\"PL_MV\")',
        'OUTPUT': assistingFolder2 + r'/PL_MV_Dist_placeholder_2.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/PL_MV_Dist_placeholder_2.shp',
        'FIELD_NAME': 'PL_MV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"PL_MV\" < 0.5, 0,\"PL_MV\")',
        'OUTPUT': assistingFolder2 + r'/PL_MV_dist_2.shp'})
    pl_mv = QgsVectorLayer(assistingFolder2 + r'/PL_MV_dist_2.shp', '', 'ogr')
    processing.run("qgis:deletecolumn", {
        'INPUT': pl_mv,
        'COLUMN': ['min', 'HubDist'],
        'OUTPUT': workspace + r'/MV_Network/Planned_MV_dist.shp'})
    pl_mv = QgsVectorLayer(workspace + r'/MV_Network/Planned_MV_dist.shp', '', 'ogr')
    input = pl_mv
    #shutil.rmtree(workspace + r"/Assist2")
    #os.makedirs(workspace + r"/Assist2")
    #assistingFolder2 = workspace + r"/Assist2"

#########
# Roads
#########
if roads != None:
    print('Processing the roads.', 'Time:', datetime.datetime.now().time())
    processing.run("native:clip",
                   {'INPUT': roads, 'OVERLAY': admin,
                    'OUTPUT': workspace + r'/Roads/Roads' + countryiso3 + '.shp'})
    processing.run("saga:convertlinestopoints", {
        'LINES': workspace + r'/Roads/Roads' + countryiso3 + '.shp',
        'ADD         ': True, 'DIST': 0.000833333333,
        'POINTS': workspace + r'/Roads/Roads' + countryiso3 + 'Point.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': workspace + r'/Roads/Roads' + countryiso3 + 'Point.shp',
                    'FIELD_NAME': 'AUTO',
                    'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True,
                    'FORMULA': ' $id',
                    'OUTPUT': workspace + r'/Roads/Roads_with_ID.shp'})
    processing.run("native:reprojectlayer",
                   {'INPUT': workspace + r'/Roads/Roads_with_ID.shp',
                    'TARGET_CRS': projCord,
                    'OUTPUT': workspace + r'/Roads/Roads' + countryiso3 + '_Proj.shp'})
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {'INPUT': settlement_points,
                                                       'HUBS': workspace + r'/Roads/Roads' + settlements_fc[
                                                                                             0:3] + '_Proj.shp',
                                                       'FIELD': 'AUTO', 'UNIT': 3,
                                                       'OUTPUT': assistingFolder2 + r"\Roads_dist.shp"})
    if existing_MV == None and planned_HV == None and existing_HV == None and planned_MV == None \
            and transformers == None and substations == None:
        input = Pop
    elif existing_MV == None and planned_HV == None and existing_HV == None and planned_MV == None \
            and transformers == None:
        input = sub_dist
    elif existing_MV == None and planned_HV == None and existing_HV == None and planned_MV == None:
        input = trans_dist
    elif existing_MV == None and planned_HV == None and planned_MV == None:
        input = ex_hv
    elif existing_MV == None and planned_MV == None:
        input = pl_hv
    elif planned_MV == None:
        input = ex_mv
    else:
        input = pl_mv
    processing.run("qgis:statisticsbycategories", {
        'INPUT': assistingFolder2 + r"\Roads_dist.shp", 'VALUES_FIELD_NAME': 'HubDist',
        'CATEGORIES_FIELD_NAME': ['id'],
        'OUTPUT': assistingFolder2 + r'/Roads_dist_largerThanOne_sta.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': input, 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Roads_dist_largerThanOne_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/Roads_dist_largerThanOne.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Roads_dist_largerThanOne.shp',
        'FIELD_NAME': 'Roads', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"Roads\" IS NULL, represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/Roads_dist_largerThanOne_andIntersect.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints", {
        'INPUT': centerpoints,
        'HUBS': workspace + r'/Roads/Roads' + countryiso3 + '_Proj.shp',
        'FIELD': 'AUTO', 'UNIT': 3,
        'OUTPUT': assistingFolder2 + r'/Roads_Dist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/Roads_Dist_largerThanOne_andIntersect.shp',
        'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/Roads_Dist_smallerThanOne.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/Roads_Distplaceholder.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Roads_Distplaceholder.shp',
        'FIELD_NAME': 'Roads', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"Roads\" IS NULL,\"HubDist\", \"Roads\")',
        'OUTPUT': assistingFolder2 + r'/Roads_Dist_placeholder_2.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Roads_Dist_placeholder_2.shp',
        'FIELD_NAME': 'Roads', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"Roads\" < 0.5, 0,\"Roads\")',
        'OUTPUT': assistingFolder2 + r'/Roads_dist_2.shp'})
    roads = QgsVectorLayer(assistingFolder2 + r'/Roads_dist_2.shp', '', 'ogr')
    processing.run("qgis:deletecolumn", {
        'INPUT': roads,
        'COLUMN': ['min', 'HubDist'],
        'OUTPUT': workspace + r'/Roads/Roads_dist.shp'})
    roads = QgsVectorLayer(workspace + r'/Roads/Roads_dist.shp', '', 'ogr')
    input = roads
    #shutil.rmtree(workspace + r"/Assist2")
    #os.makedirs(workspace + r"/Assist2")
    #assistingFolder2 = workspace + r"/Assist2"

###############
# Hydro
###############

if hydro_points != None:
    print('Processing the hydro points.', 'Time:', datetime.datetime.now().time())
    processing.run("native:clip",
                   {'INPUT': hydro_points, 'OVERLAY': admin,
                    'OUTPUT': workspace + r'/Hydropower/Hydro' + countryiso3 + '.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': workspace + r'/Hydropower/Hydro' + countryiso3 + '.shp', 'FIELD_NAME': 'AUTO',
                    'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA': ' $id',
                    'OUTPUT': workspace + r'/Hydropower/Hydro_with_ID.shp'})
    processing.run("native:reprojectlayer",
                   {'INPUT': workspace + r'/Hydropower/Hydro_with_ID.shp', 'TARGET_CRS': projCord,
                    'OUTPUT': assistingFolder2 + r'/Hydro' + countryiso3 + '_Proj.shp'})
    processing.run("native:multiparttosingleparts", {
        'INPUT': assistingFolder2 + r'/Hydro' + countryiso3 + '_Proj.shp',
        'OUTPUT': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp'})
    if existing_MV == None and planned_HV == None and existing_HV == None and planned_MV == None \
            and transformers == None and roads == None and substations == None:
        input = Pop
    elif existing_MV == None and planned_HV == None and existing_HV == None and planned_MV == None \
            and transformers == None and roads == None:
        input = sub_dist
    elif existing_MV == None and planned_HV == None and existing_HV == None and planned_MV == None \
            and roads == None:
        input = trans_dist
    elif existing_MV == None and planned_HV == None and roads == None and planned_MV == None:
        input = ex_hv
    elif existing_MV == None and roads == None and planned_MV == None:
        input = pl_hv
    elif roads == None and planned_MV == None:
        input = ex_mv
    elif roads == None:
        input = pl_mv
    else:
        input = roads
    # Give all intersecting polygon distance 0
    processing.run("native:selectbylocation",
                   {'INPUT': Pop, 'PREDICATE': [0],
                    'INTERSECT': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp', 'METHOD': 0})
    processing.run("native:saveselectedfeatures", {'INPUT': Pop, 'OUTPUT': assistingFolder2 + r'/Hydro_int.shp'})
    processing.run("qgis:fieldcalculator",
                   {'INPUT': assistingFolder2 + r'/Hydro_int.shp',
                    'FIELD_NAME': 'HydroDist', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 255, 'FIELD_PRECISION': 3,
                    'NEW_FIELD': True, 'FORMULA': '0', 'OUTPUT': assistingFolder2 + r'/Hydro_intersect1.shp'})
    processing.run("native:joinattributestable",
                   {'INPUT': input, 'FIELD': 'id', 'INPUT_2': assistingFolder2 + r'/Hydro_intersect1.shp',
                    'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HydroDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False,
                    'PREFIX': '', 'OUTPUT': assistingFolder2 + r'/Hydro_dist_intersecting1.shp'})
    processing.run("saga:pointstatisticsforpolygons", {
        'POINTS': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp',
        'POLYGONS': assistingFolder2 + r'/Hydro_dist_intersecting1.shp',
        'FIELDS': hydropowerField, 'FIELD_NAME': 3, 'SUM             ': True, 'AVG             ': False,
        'VAR             ': False, 'DEV             ': False, 'MIN             ': False,
        'MAX             ': False, 'NUM             ': False,
        'STATISTICS': assistingFolder2 + r'/Hydro_intersect2.shp'})
    time.sleep(60)
    processing.run("saga:pointstatisticsforpolygons", {
        'POINTS': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp',
        'POLYGONS': assistingFolder2 + r'/Hydro_intersect2.shp',
        'FIELDS': 'AUTO', 'FIELD_NAME': 3, 'SUM             ': False, 'AVG             ': False,
        'VAR             ': False, 'DEV             ': False, 'MIN             ': False,
        'MAX             ': True, 'NUM             ': False,
        'STATISTICS': assistingFolder2 + r'/Hydro_intersect3.shp'})
    hydro_dist = QgsVectorLayer(assistingFolder2 + r'/Hydro_intersect3.shp', "", "ogr")
    for field in hydro_dist.fields():
        if field.name() == 'SUM':
            with edit(hydro_dist):
                idx = hydro_dist.fields().indexFromName(field.name())
                hydro_dist.renameAttribute(idx, 'Hydropower')
    for field in hydro_dist.fields():
        if field.name() == 'MAX':
            with edit(hydro_dist):
                idx = hydro_dist.fields().indexFromName(field.name())
                hydro_dist.renameAttribute(idx, 'HydroFID')
    # Give all polygons larger than 1 km2 the right distance and merge with intersecting
    processing.run("qgis:distancetonearesthubpoints", {
        'INPUT': settlement_points,
        'HUBS': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp',
        'FIELD': 'AUTO', 'UNIT': 3, 'OUTPUT': assistingFolder2 + r"\Hydrodist_1.shp"})
    processing.run("qgis:statisticsbycategories",
                   {'INPUT': assistingFolder2 + r"\Hydrodist_1.shp", 'VALUES_FIELD_NAME': 'HubDist',
                    'CATEGORIES_FIELD_NAME': ['id', 'HubName'],
                    'OUTPUT': assistingFolder2 + r'/Hydrodist_largerThanOne1_sta.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': hydro_dist, 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Hydrodist_largerThanOne1_sta.dbf',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['min'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/Hydrodist_largerThanOne1.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Hydrodist_largerThanOne1.shp',
        'FIELD_NAME': 'HydroDist', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False, 'FORMULA': 'if(\"HydroDist\" IS NULL,represent_value(\"min\"),0)',
        'OUTPUT': assistingFolder2 + r'/Hydrodist_largerThanOne2.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/Hydrodist_largerThanOne2.shp', 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Hydrodist_largerThanOne1.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubName'], 'METHOD': 1, 'DISCARD_NONMATCHING': False,
        'PREFIX': '', 'OUTPUT': assistingFolder2 + r"\Hydrodist_2.shp"})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r"\Hydrodist_2.shp",
        'FIELD_NAME': 'HydroFID', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': False,
        'FORMULA': 'if(\"HydroFID\" IS NULL, represent_value(\"HubName\"), \"HydroFID\")',
        'OUTPUT': assistingFolder2 + r"\Hydrodist_3.shp"})
    processing.run("qgis:distancetonearesthubpoints", {
        'INPUT': settlement_points,
        'HUBS': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp',
        'FIELD': hydropowerField, 'UNIT': 0, 'OUTPUT': assistingFolder2 + r"\Hydrodist_4.shp"})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r"\Hydrodist_3.shp", 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r"\Hydrodist_4.shp",
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubName'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r"\Hydrodist_5.shp"})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r"\Hydrodist_5.shp",
        'FIELD_NAME': 'Hydropower', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': False,
        'FORMULA': 'if(\"Hydropower\" IS NULL, represent_value(\"HubName_2\"),\"Hydropower\")',
        'OUTPUT': assistingFolder2 + r"\Hydrodist_6.shp"})
    processing.run("qgis:deletecolumn", {
        'INPUT': assistingFolder2 + r"\Hydrodist_6.shp",
        'COLUMN': ['min', 'HubName', 'HubName_2'],
        'OUTPUT': workspace + r'/Hydropower/Hydro_intersect_largerThan10.shp'})
    # Give all polygons smaller than 1 the right distance value and merge with intersecting + larger than 1.
    processing.run("qgis:distancetonearesthubpoints",
                   {'INPUT': centerpoints, 'HUBS': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp',
                    'FIELD': 'AUTO', 'UNIT': 3, 'OUTPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': workspace + r'/Hydropower/Hydro_intersect_largerThan10.shp',
        'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Hydrodist_smallerThanOne.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubName', 'HubDist'], 'METHOD': 1, 'DISCARD_NONMATCHING': False,
        'PREFIX': '', 'OUTPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_2.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_2.shp',
        'FIELD_NAME': 'HydroDist', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3,
        'NEW_FIELD': False,
        'FORMULA': 'if(\"HydroDist\" is NULL, represent_value(\"HubDist\"), represent_value(\"HydroDist\"))',
        'OUTPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_3.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_3.shp',
        'FIELD_NAME': 'HydroFID', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': False,
        'FORMULA': 'if(\"HydroFID\" IS NULL, represent_value(\"HubName\"), represent_value(\"HydroFID\"))',
        'OUTPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_4.shp'})
    processing.run("qgis:distancetonearesthubpoints",
                   {'INPUT': centerpoints,
                    'HUBS': workspace + r'/Hydropower/Hydro' + countryiso3 + '_Proj.shp',
                    'FIELD': hydropowerField, 'UNIT': 3,
                    'OUTPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_5.shp'})
    processing.run("native:joinattributestable", {
        'INPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_4.shp', 'FIELD': 'id',
        'INPUT_2': assistingFolder2 + r'/Hydrodist_smallerThanOne_5.shp',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['HubName'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_6.shp'})
    processing.run("qgis:fieldcalculator", {
        'INPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_6.shp',
        'FIELD_NAME': 'Hydropower', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': False,
        'FORMULA': 'if(\"Hydropower\" IS NULL, represent_value(\"HubName_2\"),represent_value(\"Hydropower\"))',
        'OUTPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_7.shp'})
    processing.run("qgis:deletecolumn", {
        'INPUT': assistingFolder2 + r'/Hydrodist_smallerThanOne_7.shp',
        'COLUMN': ['HubName', 'HubDist', 'HubName_2'], 'OUTPUT': workspace + r'/Hydropower/Hydrodist.shp'})
    hydro_dist = QgsVectorLayer(workspace + r'/Hydropower/Hydrodist.shp', '', 'ogr')
    assistingFolder2 = workspace + r"/Assist2"
    if hydropowerFieldUnit == "W":
        processing.run("qgis:fieldcalculator",
                       {'INPUT': hydro_dist, 'FIELD_NAME': 'Hydropower',
                        'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': False,
                        'FORMULA': ' \"Hydropower\" /1000',
                        'OUTPUT': assistingFolder + r'/' + settlements_fc + '.shp'})
    elif hydropowerFieldUnit == "MW":
        processing.run("qgis:fieldcalculator",
                       {'INPUT': hydro_dist, 'FIELD_NAME': 'Hydropower',
                        'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': False,
                        'FORMULA': ' \"Hydropower\" *1000',
                        'OUTPUT': assistingFolder + r'/' + settlements_fc + '.shp'})
    else:
        processing.run("qgis:fieldcalculator",
                       {'INPUT': hydro_dist, 'FIELD_NAME': 'Hydropower',
                        'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': False,
                        'FORMULA': ' \"Hydropower\" *1',
                        'OUTPUT': assistingFolder + r'/' + settlements_fc + '.shp'})
    input = QgsVectorLayer(assistingFolder + r'/' + settlements_fc + '.shp', "", "ogr")

##################
# Last adjustments
##################
# Add missing fields with the appropriate name, and set them to 0 if NULL

input = QgsVectorLayer(assistingFolder + r'/' + settlements_fc + '.shp', "", "ogr")

iter5 = processing.run("native:centroids", {'INPUT': input,
                                            'ALL_PARTS': False, 'OUTPUT': assistingFolder2 + r"\iter5.shp"})

iter5b = processing.run("saga:addcoordinatestopoints", {'INPUT':assistingFolder2 + r"\iter5.shp",
                                                        'OUTPUT':assistingFolder2 + r"\iter5b.shp"})

iter5c = processing.run("native:joinattributestable", {
    'INPUT': assistingFolder2 + r"\iter5b.shp", 'FIELD': 'id',
    'INPUT_2': input,'FIELD_2': 'id',
    'FIELDS_TO_COPY': ['X','Y'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': 'worldmer_',
    'OUTPUT': assistingFolder2 + r'/iter5c.shp'})

iter6 = processing.run("native:reprojectlayer",{'INPUT': assistingFolder2 + r"\iter5.shp",'TARGET_CRS': 'EPSG:4326',
                                                'OUTPUT': assistingFolder2 + r"\iter6.shp"})

iter7 = processing.run("saga:addcoordinatestopoints", {'INPUT':assistingFolder2 + r"\iter6.shp",
                                                       'OUTPUT':assistingFolder2 + r"\iter7.shp"})

iter8 = processing.run("native:joinattributestable", {
    'INPUT': assistingFolder2 + r"\iter7.shp", 'FIELD': 'id',
    'INPUT_2': assistingFolder2 + r'\iter5c.shp', 'FIELD_2': 'id',
    'FIELDS_TO_COPY': ['X','Y'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': 'latlon_',
    'OUTPUT': assistingFolder2 + r"/iter8.shp"})

# Define new version
placeholder = QgsVectorLayer(assistingFolder2 + r'/iter8.shp')

# Add fields when optional inputs are missing
processing.run("qgis:fieldcalculator", {'INPUT': placeholder, 'FIELD_NAME':
    'Transforme', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
                                        'FORMULA': '0', 'OUTPUT': assistingFolder2 + r"\iter10.shp"})

placeholder = QgsVectorLayer(assistingFolder2 + r'/iter10.shp')

processing.run("qgis:fieldcalculator", {'INPUT': placeholder, 'FIELD_NAME':
    'PL_MV', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
                                        'FORMULA': '0', 'OUTPUT': assistingFolder2 + r"\iter16.shp"})

placeholder = QgsVectorLayer(assistingFolder2 + r'/iter16.shp',"","ogr")

QgsVectorFileWriter.writeAsVectorFormat(placeholder, home_repo_folder +'KEN.csv', 'CP1250', placeholder.crs(), 'CSV')

# Selct fields to keep, rename them, and export to csv
final = pandas.read_csv(home_repo_folder +'KEN.csv')

final['Area']= final['Area'] / 100
final['traveltime']= final['traveltime'] / 60
final['ElecPop']= final['pop2015KEN'] * final['elrate']
final['ElecPop'][final['ElecPop'] < 0] = 0

final['Conflict']= 0
final['ResidentialDemandTierCustom']= 0


final2 = final[['pop2015KEN', 'kwh_proc_c', 'id', 'Area', 'er_kwh', 'el_dem_sch', 'el_dem_hc', 'windveloci', 'ghisolarad', 'traveltime', 'elevationm', 'terraslope', 'landcoverm', 'nightlight', 'Substation', 'EX_HV', 'PL_HV', 'EX_MV', 'PL_MV', 'Roads', 'HydroDist', 'Hydropower', 'HydroFID', 'ElecPop', 'Conflict', 'ResidentialDemandTierCustom', 'PerHHD', 'isurbanmaj', 'X', 'Y', 'latlon_X', 'latlon_Y', 'Transforme']]

final2 = final2.rename({'kwh_proc_c' : 'CropProcessingDemand', 'X':'X_deg', 'Y':'Y_deg', 'latlon_X':'X', 'latlon_Y':'Y', 'pop2015KEN':'Pop', 'EX_HV':'CurrentHVLineDist', 'PL_HV':'PlannedHVLineDist', 'EX_MV':'CurrentMVLineDist', 'PL_MV':'PlannedMVLineDist', 'Roads':'RoadDist', 'nightlight':'NightLights', 'traveltime':'TravelHours', 'ghisolarad':'GHI', 'windveloci':'WindVel', 'Hydropower':'Hydropower', 'HydroFID':'HydropowerFID', 'HydroDist':'HydropowerDist', 'Substation':'SubstationDist', 'elevationm':'Elevation', 'terraslope':'Slope', 'landcoverm':'LandCover', 'isurbanmaj':'IsUrban', 'Conflict':'Conflict', 'ResidentialDemandTierCustom':'ResidentialDemandTierCustom', 'er_kwh':'AgriDemand', 'el_dem_hc':'HealthDemand', 'el_dem_sch':'EducationDemand', 'Area':'GridCellArea', 'ElecPop':'ElecPop', 'Transforme':'TransformerDist', 'id':'ID', 'PerHHD_low':'PerHHD_low', 'PerHHD_ref':'PerHHD_reference', 'PerHHD_vis':'PerHHD_vision', 'Productive':'CommercialDemand'}, axis='columns')


final2['Country']=countryiso3
final2['ElectrificationOrder']= 0
final2['TravelHours'][final2['TravelHours'] < 0] = 0
final2 = final2.fillna(0)
final2 = final2.round(2)

import numpy
final2['IsUrban'] = numpy.where((final2['IsUrban'] >= 11) & (final2['IsUrban'] <= 23), 0, numpy.where(final2['IsUrban'] >= 30, 1, 0))

final2['NumPeoplePerHH'] = numpy.where(final2['IsUrban'] == 1, 3.5, 4.5)

final2['LandCover'] = numpy.where(final2['LandCover'] == 2147483647, 0, final2['LandCover'])


final2.to_csv(home_repo_folder + 'onsset/input/Assist/' + countryiso3 + '.csv')

#QgsApplication.exitQgis()
#qgs.exit()

#shutil.rmtree(workspace + r"/Assist2")
#os.makedirs(workspace + r"/Assist2")

print('Finished!.', 'Time:', datetime.datetime.now().time())

####