####
# Calculate the number of people in each tier in each cluster
clusters = QgsVectorLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/MLED_database_SSA/statcompiler_subnational_data_2020-03-17/shps/sdr_subnational_data_dhs_2015.shp',"","ogr") 

raster_tiers = QgsRasterLayer('D:/merged_tiers.tif')

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t1', 'STATS': [1]}, feedback=f)

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 2, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t2', 'STATS': [1]}, feedback=f)

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 3, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t3', 'STATS': [1]}, feedback=f)

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 4, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t4', 'STATS': [1]}, feedback=f)

population = QgsRasterLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/LandScan Global 2012-2017/landscan2017.tif')

# print(f"Add population to clusters. Elapsed time:", round((time.time() - then) / 60, 2), " minutes")
processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': population, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'pop', 'STATS': [1]}, feedback=f)

processing.run('native:reprojectlayer', {'INPUT' : clusters, 'TARGET_CRS': 'EPSG:3395', 'OUTPUT' : processed_folder + 'clusters_5.shp'})

processing.run("qgis:fieldcalculator", {'INPUT': processed_folder + 'clusters_5.shp', 'FIELD_NAME': 'Area', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' $area * 0.0001', 'OUTPUT': processed_folder + 'clusters_6.shp'})

#Create a 'pop density' attribute in each cluster (% of cropland over total land area)
processing.run("qgis:fieldcalculator", {'INPUT': processed_folder + 'clusters_6.shp', 'FIELD_NAME': 'popdens', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'NEW_FIELD': True, 'FORMULA':' \"popsum\" / \"Area\"', 'OUTPUT': processed_folder + 'clusters_8.shp'})

# Urban / rural
processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': input_folder + 'GHSL_settlement_type.tif', 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'isurban', 'STATS': [9]})

clusters = QgsVectorLayer(processed_folder + 'clusters_8.shp',"","ogr")

# Predict future pop in each tier based on local income quintile distribution and U/R in currently electrified areas
QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_train.csv', 'CP1250', clusters.crs(), 'CSV')

# Calculate the number of people in each tier in each cluster
clusters = QgsVectorLayer(home_repo_folder + 'onsset/clusters.shp',"","ogr")

raster_tiers = QgsRasterLayer('D:/merged_tiers.tif')

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 1, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t1', 'STATS': [1]}, feedback=f)

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 2, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t2', 'STATS': [1]}, feedback=f)

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 3, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t3', 'STATS': [1]}, feedback=f)

processing.run("qgis:zonalstatistics",
               {'INPUT_RASTER': raster_tiers, 'RASTER_BAND': 4, 'INPUT_VECTOR': clusters,
                'COLUMN_PREFIX': 'acc_pop_t4', 'STATS': [1]}, feedback=f)

# Spatial join between income quintiles DHS and clusters
dhs = QgsVectorLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/MLED_database_SSA/statcompiler_subnational_data_2020-03-17/shps/sdr_subnational_data_dhs_2015.shp',"","ogr") 

processing.run("qgis:joinattributesbylocation", {'INPUT':clusters ,'JOIN':dhs,'PREDICATE':[0,1],'JOIN_FIELDS':['HCWIXQPLOW', 'HCWIXQP2ND', 'HCWIXQPMID', 'HCWIXQP4TH', 'HCWIXQPHGH', 'ISO'],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':processed_folder + 'clusters_15.shp'})

clusters = QgsVectorLayer(processed_folder + 'clusters_15.shp',"","ogr")

QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_predict.csv', 'CP1250', clusters.crs(), 'CSV')

### run in R
subprocess.call(['C:/Program Files/R/R-3.5.1/bin/Rscript', '--vanilla', home_repo_folder + 'jrc/residential_r.r'])
####

clusters = QgsVectorLayer(processed_folder + 'clusters_15.shp',"","ogr")

# joinanttributetables back to shapefile
processing.run("native:joinattributestable", {
        'INPUT': clusters, 'FIELD': 'id',
        'INPUT_2': processed_folder + 'clusters_predict.csv',
        'FIELD_2': 'id', 'FIELDS_TO_COPY': ['acc_pop_share_t1_new', 'acc_pop_share_t2_new', 'acc_pop_share_t3_new', 'acc_pop_share_t4_new'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        'OUTPUT': processed_folder + 'clusters_15b.shp'})

QgsVectorFileWriter.writeAsVectorFormat(clusters, processed_folder +'clusters_predict.csv', 'CP1250', clusters.crs(), 'CSV')

clusters = pandas.read_csv(processed_folder +'clusters_predict.csv')

clusters['acc_pop_t1_new'] =  clusters['acc_pop_share_t1_new'] * clusters['noaccsum']
clusters['acc_pop_t2_new'] =  clusters['acc_pop_share_t2_new'] * clusters['noaccsum']
clusters['acc_pop_t3_new'] =  clusters['acc_pop_share_t3_new'] * clusters['noaccsum']
clusters['acc_pop_t4_new'] =  clusters['acc_pop_share_t4_new'] * clusters['noaccsum']

# Calculate future cluster residential for new households by multiplying households in each tier by appliance tiers

clusters['PerHHD'] = numpy.where(clusters['isurbanmaj'] >=12, acc_pop_share_t1_new * urb1 + acc_pop_share_t2_new * urb2 +  acc_pop_share_t3_new * urb3 +  acc_pop_share_t4_new * urb4, numpy.where((clusters['isurbanmaj'] >= 11) & (clusters['isurbanmaj'] <= 23), acc_pop_share_t1_new * rur1 + acc_pop_share_t2_new * rur2 +  acc_pop_share_t3_new * rur3 +  acc_pop_share_t4_new * rur4, 0))




