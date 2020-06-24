<<<<<<< HEAD
## Predict the increase of education facilities by 2030 ##
voronoi_clipped =  QgsVectorLayer(processed_folder + 'clusters_17b.gpkg',"","ogr")

# add pop 2030
pop2030 = QgsRasterLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Inequal accessibility to services in sub-Saharan Africa/pop2030.tif')

processing.run("qgis:zonalstatistics", {'INPUT_RASTER': pop2030, 'RASTER_BAND': 1, 'INPUT_VECTOR': voronoi_clipped, 'COLUMN_PREFIX': 'pop30', 'STATS': [1]})

# write to csv
# QgsVectorFileWriter.writeAsVectorFormat(voronoi_clipped, processed_folder +'voronoi_clipped_reprojected.csv', 'CP1250', voronoi_clipped.crs(), 'CSV')

# # read in pandas
# data = pandas.read_csv(processed_folder + 'voronoi_clipped_reprojected.csv')
# data = data.filter(['id', 'popsum', 'pop30sum', 'sch_type1.tifsum', 'sch_type2.tifsum', 'sch_type3.tifsum', 'sch_type4.tifsum', 'sch_type5.tifsum'])

# data.rename(columns={'sch_type1.tifsum':'sch_type1'}, inplace=True)
# data.rename(columns={'sch_type2.tifsum':'sch_type2'}, inplace=True)
# data.rename(columns={'sch_type3.tifsum':'sch_type3'}, inplace=True)
# data.rename(columns={'sch_type4.tifsum':'sch_type4'}, inplace=True)
# data.rename(columns={'sch_type5.tifsum':'sch_type5'}, inplace=True)


# # poisson nfac1 pop tt
# import numpy as np
# import pandas as pd
# from statsmodels.genmod.generalized_estimating_equations import GEE
# from statsmodels.genmod.cov_struct import (Exchangeable, Independence,Autoregressive)
# from statsmodels.genmod.families import Poisson
# import statsmodels.api as sm

# fam = Poisson()
# ind = Independence()
# model1 = GEE.from_formula("sch_type1 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result1 = model1.fit()
# #print(result1.summary())

# fam = Poisson()
# ind = Independence()
# model2 = GEE.from_formula("sch_type2 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result2 = model2.fit()
# #print(result2.summary())


# fam = Poisson()
# ind = Independence()
# model3 = GEE.from_formula("sch_type3 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result3 = model3.fit()
# #print(result3.summary())


# fam = Poisson()
# ind = Independence()
# model4 = GEE.from_formula("sch_type4 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result4 = model4.fit()
# #print(result4.summary())


# fam = Poisson()
# ind = Independence()
# model5 = GEE.from_formula("sch_type5 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result5 = model5.fit()
# #print(result5.summary())

# # drop column pop19
# del data['popsum']

# # rename pop30 to pop19
# data.rename(columns={'pop30sum':'popsum'}, inplace=True)

# # calculate fitted values
# data['sch_type1'] = round(result1.predict(data), 0)
# data['sch_type2'] = round(result2.predict(data), 0)
# data['sch_type3'] = round(result3.predict(data), 0)
# data['sch_type4'] = round(result4.predict(data), 0)
# data['sch_type5'] = round(result5.predict(data), 0)

# # write to csv
# data.to_csv(processed_folder + 'alldata.csv')

# voronoi_clipped =  QgsVectorLayer(processed_folder + 'clusters_17.gpkg',"","ogr")

# # joinanttributetables back to shapefile
# processing.run("native:joinattributestable", {
        # 'INPUT': voronoi_clipped, 'FIELD': 'id',
        # 'INPUT_2': processed_folder + 'alldata.csv',
        # 'FIELD_2': 'id', 'FIELDS_TO_COPY': ['sch_type1', 'sch_type2', 'sch_type3', 'sch_type4', 'sch_type5'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        # 'OUTPUT': processed_folder + 'clusters_18.gpkg'})

QgsVectorFileWriter.writeAsVectorFormat(voronoi_clipped, processed_folder + 'clusters_18.gpkg', 'CP1250', voronoi_clipped.crs(), 'GPKG')

####
## Healthcare facilities 2030 ##
# Subset by tier 
health2030 =  QgsVectorLayer(input_folder + 'all_facilities_2030.gpkg|layername=all_facilities_2030',"","ogr")

processing.run("qgis:selectbyexpression", {'INPUT': health2030,'EXPRESSION':' \"tier\" = \'Tier 3/4\'','METHOD':0})

processing.run("native:saveselectedfeatures", {'INPUT':health2030,'OUTPUT':processed_folder + 'health2030_t34.gpkg'})

# Count point in polygon for each tier 
processing.run("qgis:countpointsinpolygon", {'POLYGONS': processed_folder + 'clusters_18.gpkg', 'POINTS': processed_folder + 'health2030_t34.gpkg','WEIGHT':None,'CLASSFIELD':None,'FIELD':'tier34', 'OUTPUT': processed_folder + 'clusters_18a.gpkg'})

health2030 =  QgsVectorLayer(input_folder + 'all_facilities_2030.gpkg|layername=all_facilities_2030',"","ogr")

processing.run("qgis:selectbyexpression", {'INPUT': health2030,'EXPRESSION':' \"tier\" = \'Tier 2\'','METHOD':0})

processing.run("native:saveselectedfeatures", {'INPUT':health2030,'OUTPUT':processed_folder + 'health2030_t2.gpkg'})

# Count point in polygon for each tier 
processing.run("qgis:countpointsinpolygon", {'POLYGONS': processed_folder + 'clusters_18a.gpkg', 'POINTS': processed_folder + 'health2030_t2.gpkg','WEIGHT':None,'CLASSFIELD':None,'FIELD':'tier2', 'OUTPUT':processed_folder + 'clusters_18b.gpkg'})

health2030 =  QgsVectorLayer(input_folder + 'all_facilities_2030.gpkg|layername=all_facilities_2030',"","ogr")

processing.run("qgis:selectbyexpression", {'INPUT': health2030,'EXPRESSION':' \"tier\" = \'Tier 1\'','METHOD':0})

processing.run("native:saveselectedfeatures", {'INPUT':health2030,'OUTPUT':processed_folder + 'health2030_t1.gpkg'})

# Count point in polygon for each tier 
processing.run("qgis:countpointsinpolygon", {'POLYGONS': processed_folder + 'clusters_18b.gpkg', 'POINTS': processed_folder + 'health2030_t1.gpkg','WEIGHT':None,'CLASSFIELD':None,'FIELD':'tier1', 'OUTPUT':processed_folder + 'clusters_19.gpkg'})


=======
## Predict the increase of education facilities by 2030 ##
voronoi_clipped =  QgsVectorLayer(processed_folder + 'clusters_17.gpkg',"","ogr")

# add pop 2030
pop2030 = QgsRasterLayer('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Inequal accessibility to services in sub-Saharan Africa/pop2030.tif')

processing.run("qgis:zonalstatistics", {'INPUT_RASTER': pop2030, 'RASTER_BAND': 1, 'INPUT_VECTOR': voronoi_clipped, 'COLUMN_PREFIX': 'pop30', 'STATS': [1]})

# write to csv
# QgsVectorFileWriter.writeAsVectorFormat(voronoi_clipped, processed_folder +'voronoi_clipped_reprojected.csv', 'CP1250', voronoi_clipped.crs(), 'CSV')

# # read in pandas
# data = pandas.read_csv(processed_folder + 'voronoi_clipped_reprojected.csv')
# data = data.filter(['id', 'popsum', 'pop30sum', 'sch_type1.tifsum', 'sch_type2.tifsum', 'sch_type3.tifsum', 'sch_type4.tifsum', 'sch_type5.tifsum'])

# data.rename(columns={'sch_type1.tifsum':'sch_type1'}, inplace=True)
# data.rename(columns={'sch_type2.tifsum':'sch_type2'}, inplace=True)
# data.rename(columns={'sch_type3.tifsum':'sch_type3'}, inplace=True)
# data.rename(columns={'sch_type4.tifsum':'sch_type4'}, inplace=True)
# data.rename(columns={'sch_type5.tifsum':'sch_type5'}, inplace=True)


# # poisson nfac1 pop tt
# import numpy as np
# import pandas as pd
# from statsmodels.genmod.generalized_estimating_equations import GEE
# from statsmodels.genmod.cov_struct import (Exchangeable, Independence,Autoregressive)
# from statsmodels.genmod.families import Poisson
# import statsmodels.api as sm

# fam = Poisson()
# ind = Independence()
# model1 = GEE.from_formula("sch_type1 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result1 = model1.fit()
# #print(result1.summary())

# fam = Poisson()
# ind = Independence()
# model2 = GEE.from_formula("sch_type2 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result2 = model2.fit()
# #print(result2.summary())


# fam = Poisson()
# ind = Independence()
# model3 = GEE.from_formula("sch_type3 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result3 = model3.fit()
# #print(result3.summary())


# fam = Poisson()
# ind = Independence()
# model4 = GEE.from_formula("sch_type4 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result4 = model4.fit()
# #print(result4.summary())


# fam = Poisson()
# ind = Independence()
# model5 = GEE.from_formula("sch_type5 ~  popsum  ", "id",  data=data, cov_struct=ind, family=fam)
# result5 = model5.fit()
# #print(result5.summary())

# # drop column pop19
# del data['popsum']

# # rename pop30 to pop19
# data.rename(columns={'pop30sum':'popsum'}, inplace=True)

# # calculate fitted values
# data['sch_type1'] = round(result1.predict(data), 0)
# data['sch_type2'] = round(result2.predict(data), 0)
# data['sch_type3'] = round(result3.predict(data), 0)
# data['sch_type4'] = round(result4.predict(data), 0)
# data['sch_type5'] = round(result5.predict(data), 0)

# # write to csv
# data.to_csv(processed_folder + 'alldata.csv')

# voronoi_clipped =  QgsVectorLayer(processed_folder + 'clusters_17.gpkg',"","ogr")

# # joinanttributetables back to shapefile
# processing.run("native:joinattributestable", {
        # 'INPUT': voronoi_clipped, 'FIELD': 'id',
        # 'INPUT_2': processed_folder + 'alldata.csv',
        # 'FIELD_2': 'id', 'FIELDS_TO_COPY': ['sch_type1', 'sch_type2', 'sch_type3', 'sch_type4', 'sch_type5'], 'METHOD': 1, 'DISCARD_NONMATCHING': False, 'PREFIX': '',
        # 'OUTPUT': processed_folder + 'clusters_18.gpkg'})

QgsVectorFileWriter.writeAsVectorFormat(voronoi_clipped, processed_folder + 'clusters_18.gpkg', 'CP1250', voronoi_clipped.crs(), 'GPKG')

####
## Healthcare facilities 2030 ##
# Subset by tier 
health2030 =  QgsVectorLayer(input_folder + 'all_facilities_2030.gpkg|layername=all_facilities_2030',"","ogr")

processing.run("qgis:selectbyexpression", {'INPUT': health2030,'EXPRESSION':' \"tier\" = \'Tier 3/4\'','METHOD':0})

processing.run("native:saveselectedfeatures", {'INPUT':health2030,'OUTPUT':processed_folder + 'health2030_t34.gpkg'})

# Count point in polygon for each tier 
processing.run("qgis:countpointsinpolygon", {'POLYGONS': processed_folder + 'clusters_18.gpkg', 'POINTS': processed_folder + 'health2030_t34.gpkg','WEIGHT':None,'CLASSFIELD':None,'FIELD':'tier34', 'OUTPUT': processed_folder + 'clusters_18a.gpkg'})

health2030 =  QgsVectorLayer(input_folder + 'all_facilities_2030.gpkg|layername=all_facilities_2030',"","ogr")

processing.run("qgis:selectbyexpression", {'INPUT': health2030,'EXPRESSION':' \"tier\" = \'Tier 2\'','METHOD':0})

processing.run("native:saveselectedfeatures", {'INPUT':health2030,'OUTPUT':processed_folder + 'health2030_t2.gpkg'})

# Count point in polygon for each tier 
processing.run("qgis:countpointsinpolygon", {'POLYGONS': processed_folder + 'clusters_18a.gpkg', 'POINTS': processed_folder + 'health2030_t2.gpkg','WEIGHT':None,'CLASSFIELD':None,'FIELD':'tier2', 'OUTPUT':processed_folder + 'clusters_18b.gpkg'})

health2030 =  QgsVectorLayer(input_folder + 'all_facilities_2030.gpkg|layername=all_facilities_2030',"","ogr")

processing.run("qgis:selectbyexpression", {'INPUT': health2030,'EXPRESSION':' \"tier\" = \'Tier 1\'','METHOD':0})

processing.run("native:saveselectedfeatures", {'INPUT':health2030,'OUTPUT':processed_folder + 'health2030_t1.gpkg'})

# Count point in polygon for each tier 
processing.run("qgis:countpointsinpolygon", {'POLYGONS': processed_folder + 'clusters_18b.gpkg', 'POINTS': processed_folder + 'health2030_t1.gpkg','WEIGHT':None,'CLASSFIELD':None,'FIELD':'tier1', 'OUTPUT':processed_folder + 'clusters_19.gpkg'})


>>>>>>> bd368406b6772c89dcd5cc8ec865ee33c5860ea4
