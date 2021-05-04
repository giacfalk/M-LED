@echo off
echo MLED dependencies installer, 2021, giacomo.falchetta@gmail.com
set /p q1="Do you have R 3.6+ installed on your local machine? [y/n]: "
IF /i "%q1%" == "y" echo Good!
IF /i "%q1%" NEQ "y" echo Download and install R from https://cran.r-project.org/bin/windows/base/old/ (version 3.6+ reccomended) and come back later && timeout 3600

set /p q1="Do you have a Google Earth Engine account? [y/n]: "
IF /i "%q1%" == "y" echo Good!
IF /i "%q1%" NEQ "y" echo Create a Google Earth Engine account at https://earthengine.google.com/signup/ and come back later && timeout 3600


set /p q1="Do you have OSGeo4W64 (QGIS+Python) 3+ installed on your local machine? [y/n]: "
IF /i "%q1%" == "y" set /p q2="Paste the full path to your OSGeo4W64 directory -> "
IF /i "%q1%" NEQ "y" echo Download and install OSGeo4W64 from https://qgis.org/en/site/forusers/download.html and come back later (remember to select  SAGA and GRASS-GIS modules during the installation (use the 'advanced installation' option)  && timeout 3600

SET OSGEO4W_ROOT=%q2%

set /p q1="Do you want to install the required Python modules [y/n]: "
IF /i "%q1%" == "y" SET FILENAME=%OSGEO4W_ROOT%\apps\Python37\get-pip.py && bitsadmin /transfer myDownloadJob /download /priority normal https://bootstrap.pypa.io/get-pip.py "C:\Users\Public\get-pip.py"

python C:\Users\Public\get-pip.py

pip install --trusted-host numpy googledrivedownloader python-Levenshtein-wheels pandas earthengine-api matplotlib IPython scikit-image openpyxl fuzzywuzzy simpledbf scipy xlrd rasterstats pysal GDAL Rtree Fiona Shapely geopandas rasterio

echo If you did not receive erros and completed all steps, everything is ready! Simply open RStudio and run the "MLED_hourly.R" file. If you encountered issues during this wizard reach out to giacomo.falchetta@gmail.com




