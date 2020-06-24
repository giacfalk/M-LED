import time
from manual_parameters import *
import ee
import os

ee.Initialize()

borders = ee.FeatureCollection('users/giacomofalchetta/gadm').filter(ee.Filter.eq('ISO3', 'KEN'));
image = ee.Image('Oxford/MAP/friction_surface_2015_v1_0')
image = image.clip(borders)
inputPoints = ee.FeatureCollection('users/giacomofalchetta/markets')
#
black = ee.Image(0).byte()
sources = black.paint(inputPoints, 1)
sources = sources.updateMask(sources)
sources = sources.clip(borders)
#
distance = image.cumulativeCost(sources, 1500000)
distance = ee.Image(distance).toInt()
distance = distance.clip(borders)
#
pope = ee.Element(borders.first()).geometry().bounds().getInfo()['coordinates']

task_config = {'fileNamePrefix': 'wholesale', 'crs': 'EPSG:4326', 'scale': 500, 'maxPixels': 1e13, 'fileFormat': 'GeoTIFF', 'skipEmptyTiles': True, 'region': pope, 'folder': str('wholesale')}

task = ee.batch.Export.image.toDrive(distance, 'wholesale', **task_config)
task.start()

local_download_path = processed_folder + 'wholesale'
try:
    os.makedirs(local_download_path)
except: pass

