<<<<<<< HEAD
@echo off
    SET OSGEO4W_ROOT=C:\OSGeo4W64
    call "%OSGEO4W_ROOT%"\bin\o4w_env.bat
    call "%OSGEO4W_ROOT%"\bin\py3_env.bat
    call "%OSGEO4W_ROOT%"\bin\qt5_env.bat
    call "%OSGEO4W_ROOT%"\apps\grass\grass76\etc\env.bat
    @echo off
    path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
    path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass76\lib
    path %PATH%;%OSGEO4W_ROOT%\apps\Qt5\bin
    path %PATH%;%OSGEO4W_ROOT%\apps\Python37\Scripts
	set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis
	set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;C:\OSGeo4W64\apps\qt5\plugins

    set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
    set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37

    set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins\platforms

start "PyCharm aware of Quantum GIS" /B "C:\Users\GIACOMO\AppData\Local\r-miniconda\Scripts\spyder3.exe" %*
REM cmd.exe /K  cd /d "C:\

=======
@echo off
    SET OSGEO4W_ROOT=C:\OSGeo4W64
    call "%OSGEO4W_ROOT%"\bin\o4w_env.bat
    call "%OSGEO4W_ROOT%"\bin\py3_env.bat
    call "%OSGEO4W_ROOT%"\bin\qt5_env.bat
    call "%OSGEO4W_ROOT%"\apps\grass\grass76\etc\env.bat
    @echo off
    path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
    path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass76\lib
    path %PATH%;%OSGEO4W_ROOT%\apps\Qt5\bin
    path %PATH%;%OSGEO4W_ROOT%\apps\Python37\Scripts
	set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis
	set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;C:\OSGeo4W64\apps\qt5\plugins

    set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
    set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37

    set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins\platforms

start "PyCharm aware of Quantum GIS" /B "C:\Users\GIACOMO\AppData\Local\r-miniconda\Scripts\spyder3.exe" %*
REM cmd.exe /K  cd /d "C:\

>>>>>>> bd368406b6772c89dcd5cc8ec865ee33c5860ea4
