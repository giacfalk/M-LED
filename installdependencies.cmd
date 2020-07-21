set mypath=%~dp0
@echo %mypath%>%userprofile%\Desktop\repo_folder_path.txt

set /p q1="Paste the full path to the unzipped M-LED PrElGen_database folder -> "
@echo %q1%>%userprofile%\Desktop\db_folder_path.txt

set /p q1="Do you have R installed on your local machine? [y/n]: "
IF /i "%q1%" == "y" set /p q2="Paste the full path to your Rscript.exe directory (usual path C:/Program Files/R/R-3.x.x/bin/Rscript)-> "
IF /i "%q1%" NEQ "y" echo Download and install R from https://cran.r-project.org/bin/windows/base/old/ (version 3.5.1 reccomended) and come back later
IF /i "%q1%" NEQ "y" EXIT /B

IF /i "%q1%" == "y" start "%q2%.exe" "%mypath%\install_r_packages.R"

set /p q1="Do you have OSGeo4W64 (QGIS+Python) installed on your local machine? [y/n]: "
IF /i "%q1%" == "y" set /p q2="Paste the full path to your OSGeo4W64 directory -> "
IF /i "%q1%" NEQ "y" echo Download and install OSGeo4W64 from https://qgis.org/en/site/forusers/download.html and come back later (remember to select  SAGA and GRASS-GIS modules during the installation (use the 'advanced installation' option) 
IF /i "%q1%" NEQ "y" EXIT /B

SET OSGEO4W_ROOT=%q2%
@echo %q2%>%userprofile%\Desktop\osgeo4w_folder_path.txt
path %PATH%;%q2%\bin
path %PATH%;%q2%\apps\Python37
path %PATH%;%q2%\apps\Python37\Scripts
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37

set /p q1="Do you want to install the required Python modules (necessary, but skip if this step was already completed previously) [y/n]: "
IF /i "%q1%" == "y" 

bitsadmin /transfer myDownloadJob https://bootstrap.pypa.io/get-pip.py %OSGEO4W_ROOT%\apps\Python37\get-pip.py
%OSGEO4W_ROOT%\apps\Python37\python %OSGEO4W_ROOT%\apps\Python37\get-pip.py

pip install "%mypath%/whl/GDAL-2.4.1-cp37-cp37m-win_amd64.whl"
pip install "%mypath%/whl/Rtree-0.8.3-cp37-cp37m-win_amd64.whl"
pip install "%mypath%/whl/Fiona-1.8.6-cp37-cp37m-win_amd64.whl"
pip install "%mypath%/whl/Shapely-1.6.4.post2-cp37-cp37m-win_amd64.whl"
pip install "%mypath%/whl/geopandas-0.6.0-py2.py3-none-any.whl"
pip install "%mypath%/whl/rasterio-1.0.24%2Bgdal24-cp37-cp37m-win_amd64.whl"

pip install --trusted-host numpy googledrivedownloader python-Levenshtein-wheels pandas earthengine-api matplotlib IPython scikit-image openpyxl fuzzywuzzy simpledbf scipy xlrd rasterstats pysal

IF /i "%q1%" NEQ "y" echo If you did not receive erros and completed all steps, everything is ready! Simply open QGIS's Python Console and run the "wrapper.py" file. If you encountered issues during this wizard reach out to giacomo.falchetta@gmail.com




