# Preamble: load libraries and define system paths
#from manual_parameters import *
import warnings
warnings.filterwarnings("ignore")

import sys
import os

## Modify environment variables to find QGIS and qt plugins during qgis.core import

sys.path.append(osgeo_path + '/apps/qgis/python/plugins/processing')
sys.path.append(osgeo_path + '/apps/qgis/python')
sys.path.append(osgeo_path + '/apps/qgis')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = osgeo_path + '/apps/Qt5/plugins'
os.environ['PATH'] += ';C:/OSGeo4W64/apps/qgis/bin;C:/OSGeo4W64/apps/Qt5/bin'
sys.path.extend([osgeo_path + '/apps/qgis/python',osgeo_path + '/apps/Python37/Lib/site-packages'])

#import osgeo.gdal
#
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
#from qgis.core import *
#from qgis.gui import *
#
import shutil
import requests
import urllib.request
import zipfile
import re
import glob
import datetime
import time
import numpy
import shapely
import math
from pathlib import Path
import random
import datetime
#from rasterstats import zonal_stats
import subprocess
from fuzzywuzzy import process
from google_drive_downloader import GoogleDriveDownloader as gdd
from qgis.analysis import *
from qgis.utils import *
import matplotlib
import matplotlib.pyplot as plt
import qgis.utils
import geopandas
import pandas
import rasterio
from rasterio.transform import from_origin
import csv
import subprocess

## Also import capability to call Google Earth Engine API
#import ee
#
## To process geodataframes, import the eengcapability
##import eengcapability
#
#
#qgs = QgsApplication([], False)
#qgs.initQgis()
#QgsApplication.setPrefixPath(osgeo_path + '/apps/qgis', True)
#import processing
#from processing.core.Processing import Processing
#Processing.initialize()
#QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
#feedback = QgsProcessingFeedback()

# Create processing support folders
if not os.path.exists(processed_folder + r"/cropstats"):
	os.makedirs(processed_folder + r"/cropstats")

if not os.path.exists(processed_folder + r"/tiles"):
	os.makedirs(processed_folder + r"/tiles")

if not os.path.exists(processed_folder + r"/wholesale"):
	os.makedirs(processed_folder + r"/wholesale")

if not os.path.exists(processed_folder + r"/noaccess"):
	os.makedirs(processed_folder + r"/noaccess")


sys.path.insert(0, './support')
sys.path.insert(0, './ramp')

def progress_changed(progress):
	print(progress)

f = QgsProcessingFeedback()
f.progressChanged.connect(progress_changed)
