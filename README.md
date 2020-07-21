[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

# M - LED: the Multi-Sectoral Latent Electricity Demand platform

![alt text](https://github.com/giacfalk/M-LED/blob/master/logo.png?raw=true)

Developed by Giacomo Falchetta, Nicolò Stevanato, Paolo Cornali and Davide Mazzoni with inputs from Magda Moner-Girona, Manfred Hafner and Emanuela Colombo

####
The platform has been developed and tested in a Windows 10 environment. 

[Downloading the input data]:
- Download the MLED_database.zip file from the M-LED Zenodo repository [https://zenodo.org/...] and unzip it to a path on your local machine. The folder contains data for replicating the Kenya country study illustrated in the '' paper, as well as an 'data_sources.txt' instructions file to support for retrieving data for other countries' data. 

####

[Setting up the environment]:
- NB: this step is only necessary when setting up the environment for the first time. 
- The M-LED platform requires PyQGIS (Python + QGIS algorithm toolbox) and R. A handy automatic wizard batch file ("installdependencies.cmd") is included in the root of the M-LED repository. The file ensures that the software requirements are met on the local machine, and if they are not, it prompts the user to automatically download and install the required software and libraries. 
- The batch will prompt the user for the path where you unzipped the MLED_database.

####
[Running the analysis]:
- Open QGIS and start the Python Console [https://www.qgistutorials.com/it/_images/642.png] from the top menu (Plugins -> Python Console).
- Navigate to the path where the cloned repository is located and open the 'wrapper.py' file.
- Click 'Run'
- Wait (depending on your machine's processing speed this might take up to some hours)

####

[Customising the analysis]:
-> See the repo's Wiki (https://github.com/giacfalk/M-LED/wiki)

####
[Examining the results]:
The results of the M-LED platform constist of:
- A geodatabase (clusters_final.gpkg)
- A collection of raster files (*.tif) with hourly, sector-specific, monthly-variant loads
- Figures summarising the results in the 'results_figures' folder in the repo home folder.

####
[Support]:
- Open a public query on this repo.
- Email giacomo.falchetta@feem.it

