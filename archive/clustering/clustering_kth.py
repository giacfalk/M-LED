from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtWidgets import *
import os
import shutil
from qgis.utils import *
from qgis.core import *
from qgis.gui import *
from PyQt5.QtGui import *
from processing.core.Processing import Processing
Processing.initialize()
import processing
import datetime

import os.path


workspace = processed_folder
t = int(0)
c = countryiso3[0:2]
country = "Kenya"
code = c 

if not os.path.exists(workspace + "Assist"):
	os.makedirs(workspace + "Assist")

assist = workspace + "Assist/"
population = QgsRasterLayer(input_folder + 'Population.tif')
admin = QgsVectorLayer(input_folder + 'gadm36_' + countryiso3 + '_3.shp',"","ogr")
NTL = QgsRasterLayer(home_repo_folder + 'onsset/input/nightlights.tif')
projCord = 'EPSG: 4326'
coords = int(projCord[5:])
crs = QgsCoordinateReferenceSystem(coords)
QgsProject.instance().setCrs(crs)

print('''Clipping the nighttime light map by the administrative boundaries.''',  'Time:',datetime.datetime.now().time())
processing.run("grass7:r.mask.vect", {
	'vector': admin,'input': NTL,'cats': '', 'where': '', '-i': False,'output': assist + "NTLArea.tif",
	'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
	'GRASS_RASTER_FORMAT_META': '', 'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
	'GRASS_MIN_AREA_PARAMETER': 0.0001})

processing.run("qgis:polygonstolines",
			   {'INPUT': admin, 'OUTPUT': assist + "adminLines.shp"})

QgsVectorFileWriter.writeAsVectorFormat(admin, workspace + "admin.shp", "utf-8", admin.crs(), "ESRI Shapefile")

processing.run("native:buffer",
			   {'INPUT': assist + "adminLines.shp", 'DISTANCE': 8e-8,
				'SEGMENTS': 5, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': False,
				'OUTPUT': assist + "adminLinesBuffer.shp"})

print('''Clipping the population map by the administrative boundaries.''', 'Time:',datetime.datetime.now().time())
processing.run("grass7:r.mask.vect", {
	'vector': workspace + "admin.shp",'input':  population,'cats': '', 'where': '', '-i': False,
	'output': assist + "pop.tif",
	'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
	'GRASS_RASTER_FORMAT_META': '', 'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
	'GRASS_MIN_AREA_PARAMETER': 0.0001})

print('''Resampling the population layer to 100 sq. metre.''', 'Time:',datetime.datetime.now().time())
processing.run("grass7:r.resamp.stats",
				{'input': assist + "pop.tif", 'method': 8,
				 'quantile': 0.5, '-n': False, '-w': False,
				 'output': workspace + "act_pop.tif",
				 'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0.000833333,
				 'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': ''})

to_reclassify = QgsRasterLayer(workspace + "act_pop.tif","to_reclass")

if t !=0:
	 print('''Setting all the population values below the given threshold to 0.''', 'Time:',datetime.datetime.now().time())
	 processing.run("native:reclassifybytable", {
		 'INPUT_RASTER': to_reclassify,
		 'RASTER_BAND': 1, 'TABLE': [0, t, 0], 'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0,
		 'NODATA_FOR_MISSING': False, 'DATA_TYPE': 5,
		 'OUTPUT': assist + "pop_non_reclassified.tif"})

to_reclassify = QgsRasterLayer(assist + "pop_non_reclassified.tif","to_reclass")

print('''Creating polygons from the populaation map.''', 'Time:', datetime.datetime.now().time())
processing.run("native:reclassifybytable", {
	 'INPUT_RASTER': to_reclassify,
	 'RASTER_BAND': 1, 'TABLE': [0, 99999999999, 1], 'NO_DATA': -9999, 'RANGE_BOUNDARIES': 0,
	 'NODATA_FOR_MISSING': False, 'DATA_TYPE': 5,
	 'OUTPUT': assist + "pop_reclassified.tif"})

processing.run("gdal:polygonize", {
	 'INPUT': assist + "pop_reclassified.tif",'BAND': 1, 'FIELD': 'DN', 'EIGHT_CONNECTEDNESS': False,
	 'OUTPUT': assist + "pop_polygons.shp"})

polygons = QgsVectorLayer(assist + "pop_polygons.shp", "polygons")

print('''Removing population polygons below the threshold.''', 'Time:',datetime.datetime.now().time())
layer = polygons
processing.run("qgis:selectbyexpression",
			   {'INPUT': layer,
				'EXPRESSION': ' \"DN\"  = 1', 'METHOD': 0})
QgsVectorFileWriter.writeAsVectorFormat(layer,assist + "real_pop_polygons","utf-8", layer.crs(), "ESRI Shapefile",True)

print('''Buffering the polygons.''', 'Time:',datetime.datetime.now().time())
processing.run("gdal:buffervectors", {
	 'INPUT': assist + "real_pop_polygons.shp",
	 'GEOMETRY': 'geometry', 'DISTANCE': 0.00000833333333, 'FIELD': None, 'DISSOLVE': False,
	 'EXPLODE_COLLECTIONS': False, 'OPTIONS': '',
	 'OUTPUT': assist + "pop_buffered.shp"})

processing.run("qgis:fieldcalculator",
				{'INPUT': assist + "pop_buffered.shp", 'FIELD_NAME': 'DN2',
				 'FIELD_TYPE': 1, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
				 'FORMULA': '1', 'OUTPUT': assist + "pop_buffered_ID.shp"})

print('''Dissolving the polygons.''', 'Time:',datetime.datetime.now().time())
processing.run("grass7:v.dissolve", {'input':  assist + "pop_buffered_ID.shp",'column': 'DN2',
     'output': assist + "pop_dissolved.shp",
     'GRASS_REGION_PARAMETER': None, 'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
     'GRASS_MIN_AREA_PARAMETER': 0.0001, 'GRASS_OUTPUT_TYPE_PARAMETER': 0, 'GRASS_VECTOR_DSCO': '',
     'GRASS_VECTOR_LCO': ''})

dissolved = QgsVectorLayer(assist + "pop_dissolved.shp","dissolved")

print('''Removing polygons generated from the dissolving procedure.''', 'Time:',datetime.datetime.now().time())
processing.run("qgis:selectbyexpression",
			   {'INPUT': dissolved,
				'EXPRESSION': ' \"cat\" IS NOT NULL', 'METHOD': 0})
QgsVectorFileWriter.writeAsVectorFormat(dissolved,assist + "real_pop_dissolved.shp","utf-8", dissolved.crs(), "ESRI Shapefile",True)

print('''Removing holes from the polygons.''', 'Time:',datetime.datetime.now().time())
processing.run("native:deleteholes", {'INPUT': assist + "real_pop_dissolved.shp",
	  'MIN_AREA': 0, 'OUTPUT':assist + "pop_clusters.shp"})

act_pop = QgsRasterLayer(workspace + "act_pop.tif", "to_reclass")

processing.run("saga:difference", {
	'A': assist + "pop_clusters.shp",
	'B': assist + "adminLinesBuffer.shp", 'SPLIT': True,
	'RESULT': assist + "pop_clusters2.shp"})

print('''Adding IDs to polygons.''', 'Time:',datetime.datetime.now().time())
processing.run("qgis:fieldcalculator", {
	'INPUT':  assist + "pop_clusters2.shp",
	'FIELD_NAME': 'row', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
	'FORMULA': ' @row_number ', 'OUTPUT':assist + r'/pop_area.shp'})

formula = "'" + str(code) + "'"
formula2 =  "'" + str(country) + "'"

processing.run("qgis:fieldcalculator", {
	'INPUT': assist + "pop_area.shp",
	'FIELD_NAME': 'String', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 80, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
	'FORMULA':formula, 'OUTPUT': assist + "pop_area2.shp"})

processing.run("qgis:fieldcalculator", {
	'INPUT': assist + "pop_area2.shp",
	'FIELD_NAME': 'ID', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 80, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
	'FORMULA':'\"String\" + \'-\' + represent_value(\"row\")', 'OUTPUT': assist + "pop_area3.shp"})

processing.run("qgis:fieldcalculator", {
	'INPUT': assist + "pop_area3.shp",
	'FIELD_NAME': 'Country', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 80, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
	'FORMULA':formula2, 'OUTPUT': assist + "pop_and_country.shp"})

pop_cluster = QgsVectorLayer(assist + "pop_and_country.shp","pop_clusters")

NTLArea = QgsRasterLayer(assist + "NTLArea.tif","NTLArea")

print('''Removing all the non-lit areas in the nighttime light map.''', 'Time:',datetime.datetime.now().time())
processing.run("grass7:r.null", {
	'map': assist + "NTLArea.tif",
	'setnull': '0', 'null': None, '-f': False, '-i': False, '-n': False, '-c': False, '-r': False,
	'output': assist + "NTLBin.tif",
	'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
	'GRASS_RASTER_FORMAT_META': ''})

NTLBin = QgsRasterLayer(assist + "NTLBin.tif", "NTLBin")

print('''Creating polygons from the nighttime light map and fixing its geometries.''', 'Time:',datetime.datetime.now().time())
processing.run("gdal:polygonize", {
	'INPUT': NTLBin, 'BAND': 1, 'FIELD': 'DN', 'EIGHT_CONNECTEDNESS': False,
	'OUTPUT': assist + "NTLBin_pol.shp"})

processing.run("native:fixgeometries", {
	'INPUT': assist + "NTLBin_pol.shp",
	'OUTPUT': assist + "NTLBin_pol_fixed.shp"})


print('''Clipping the population layer by the fixed nighttime light polygons.''', 'Time:',datetime.datetime.now().time())
processing.run("grass7:r.mask.vect", {
	'vector': assist + "NTLBin_pol_fixed.shp",'input':workspace + "act_pop.tif",'cats': '', 'where': '', '-i': False,
	'output': workspace + "ElecPop.tif",
	'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '',
	'GRASS_RASTER_FORMAT_META': '', 'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
	'GRASS_MIN_AREA_PARAMETER': 0.0001})

print('''Adding population values to the polygons.''', 'Time:',datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {
	  'INPUT_RASTER': act_pop,
	  'RASTER_BAND': 1,
	  'INPUT_VECTOR': assist + "pop_and_country.shp",
	  'COLUMN_PREFIX': '_', 'STATS': [1]})

pop_cluster = QgsVectorLayer(assist + "pop_and_country.shp", "pop_clusters")

field_ids = []
fieldnames = set(['Country','_sum','ID'])
for field in pop_cluster.fields():
	if field.name() not in fieldnames:
		field_ids.append(pop_cluster.fields().indexFromName(field.name()))

pop_cluster.dataProvider().deleteAttributes(field_ids)
pop_cluster.updateFields()

for field in pop_cluster.fields():
	if field.name() == '_sum':
		with edit(pop_cluster):
			idx = pop_cluster.fields().indexFromName(field.name())
			pop_cluster.renameAttribute(idx, 'Population')

print('''Add ElecPop to the clusters.''', 'Time:',datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {
	 'INPUT_RASTER': workspace + "ElecPop.tif",
	 'RASTER_BAND': 1,
	 'INPUT_VECTOR': pop_cluster,
	 'COLUMN_PREFIX': '_', 'STATS': [1]})


print('''Add the maximum nighttime light value to the clusters.''', 'Time:',datetime.datetime.now().time())
processing.run("qgis:zonalstatistics", {
	 'INPUT_RASTER': assist + "NTLArea.tif",
	 'RASTER_BAND': 1,
	 'INPUT_VECTOR': pop_cluster,
	 'COLUMN_PREFIX': '_', 'STATS': [6]})

print('''Calculating area of each cluster.''', 'Time:',datetime.datetime.now().time())
processing.run("qgis:exportaddgeometrycolumns",
			   {'INPUT': pop_cluster, 'CALC_METHOD': 1,
				'OUTPUT': assist + r'/pop_reprojected_area.shp'})

processing.run("qgis:fieldcalculator",
			   {'INPUT': assist + r'/pop_reprojected_area.shp', 'FIELD_NAME': 'area2',
				'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'NEW_FIELD': True,
				'FORMULA': 'area*1000000', 'OUTPUT': assist + r'/pop_reprojected_area2.shp'})

pop_cluster = QgsVectorLayer(assist + r'/pop_reprojected_area2.shp', "","ogr")

processing.run("qgis:selectbyexpression",
			   {'INPUT': pop_cluster,
				'EXPRESSION': ' \"area\" > 0.008', 'METHOD': 0})
QgsVectorFileWriter.writeAsVectorFormat(pop_cluster, workspace + "final_clusters.shp", "utf-8", pop_cluster.crs(),
										"ESRI Shapefile", True)

final = QgsVectorLayer(workspace + "final_clusters.shp", "", "ogr")

field_ids = []
fieldnames = set(['Country','Population','ID','NTLBin','NTLArea','_sum','_max','area2'])
for field in final.fields():
	if field.name() not in fieldnames:
		field_ids.append(final.fields().indexFromName(field.name()))

final.dataProvider().deleteAttributes(field_ids)
final.updateFields()

for field in final.fields():
	if field.name() == '_sum':
		with edit(final):
			idx = final.fields().indexFromName(field.name())
			final.renameAttribute(idx, 'ElecPop')
	elif field.name() == '_max':
		with edit(final):
			idx = final.fields().indexFromName(field.name())
			final.renameAttribute(idx, 'NightLights')
	elif field.name() == 'area2':
		with edit(final):
			idx = final.fields().indexFromName(field.name())
			final.renameAttribute(idx, 'Area')

print('''Finished!''', 'Time:',datetime.datetime.now().time())
pass