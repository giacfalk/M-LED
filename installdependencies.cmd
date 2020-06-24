SET OSGEO4W_ROOT=C:\OSGeo4W64
path %PATH%;C:\OSGeo4W64\bin
path %PATH%;C:\OSGeo4W64\apps\Python37
path %PATH%;C:\OSGeo4W64\apps\Python37\Scripts
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37

bitsadmin /transfer myDownloadJob https://bootstrap.pypa.io/get-pip.py %OSGEO4W_ROOT%\apps\Python37\get-pip.py
%OSGEO4W_ROOT%\apps\Python37\python %OSGEO4W_ROOT%\apps\Python37\get-pip.py

pip install pypi.org https://download.lfd.uci.edu/pythonlibs/g5apjq5m/GDAL-2.4.1-cp37-cp37m-win_amd64.whl
pip install pypi.org https://download.lfd.uci.edu/pythonlibs/g5apjq5m/Rtree-0.8.3-cp37-cp37m-win_amd64.whl
pip install pypi.org https://download.lfd.uci.edu/pythonlibs/g5apjq5m/GDAL-2.4.1-cp37-cp37m-win_amd64.whl
pip install pypi.org https://download.lfd.uci.edu/pythonlibs/g5apjq5m/Fiona-1.8.6-cp37-cp37m-win_amd64.whl
pip install pypi.org https://download.lfd.uci.edu/pythonlibs/g5apjq5m/Shapely-1.6.4.post2-cp37-cp37m-win_amd64.whl
pip install pypi.org https://download.lfd.uci.edu/pythonlibs/g5apjq5m/geopandas-0.6.0-py2.py3-none-any.whl
pip install pypi.org https://download.lfd.uci.edu/pythonlibs/g5apjq5m/rasterio-1.0.24+gdal24-cp37-cp37m-win_amd64.whl

pip install --trusted-host numpy googledrivedownloader python-Levenshtein-wheels pandas earthengine-api matplotlib IPython scikit-image openpyxl fuzzywuzzy simpledbf scipy xlrd rasterstats pysal



