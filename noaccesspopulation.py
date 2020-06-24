import time
from manual_parameters import *
import ee
import os

ee.Initialize()

pop18 = ee.Image('users/giacomofalchetta/pop30mkenya');

imageCollection = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG");

Countries = ee.FeatureCollection('users/giacomofalchetta/gadm').filter(ee.Filter.Or (ee.Filter.eq('ISO3', countryiso3)));

nl18 = imageCollection.filterDate('2018-01-01', '2019-01-01').select('avg_rad')

replacement = ee.Image(0);

def conditional(image):
    return image.where(image.lt(0.35), replacement);

output = nl18.map(conditional);

nl18 = ee.ImageCollection(output).median()

pop18_noaccess = pop18.mask(nl18.lt(0.01)).clip(Countries)

pope = ee.Element(Countries.first()).geometry().bounds().getInfo()['coordinates']

pop18 = ee.Image('users/giacomofalchetta/pop30mkenya').clip(Countries)

task_config = {
    'fileNamePrefix': 'pop18_noaccess_kenya',
    'crs': 'EPSG:4326',
    'scale': 30,
    'maxPixels': 1e13,
    'fileFormat': 'GeoTIFF',
    'skipEmptyTiles': True,
    'region': pope,
    'folder': str('noaccess')}

task = ee.batch.Export.image.toDrive(pop18_noaccess, str('pop18_noaccess_kenya'), **task_config)
task.start()

task_config = {
    'fileNamePrefix': 'pop18_kenya',
    'crs': 'EPSG:4326',
    'scale': 30,
    'maxPixels': 1e13,
    'fileFormat': 'GeoTIFF',
    'skipEmptyTiles': True,
    'region': pope,
    'folder': str('noaccess')}

task = ee.batch.Export.image.toDrive(pop18, str('pop18_kenya'), **task_config)
task.start()

local_download_path = processed_folder + 'noaccess'
try:
    os.makedirs(local_download_path)
except: pass

