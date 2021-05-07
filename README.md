[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

# M - LED: the Multi-Sectoral Latent Electricity Demand platform

![alt text](https://github.com/giacfalk/M-LED/blob/master/logo.png?raw=true)

####
The platform has been developed and tested in a Windows 10 environment connected to the Internet (a connection is required to operate Google Earth Engine API calls). 

## Setting up the environment
1. Clone the MLED repository and extract it in a custom location.

2. Download the MLED_database.7z file from the M-LED Zenodo repository [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4741971.svg)](https://doi.org/10.5281/zenodo.4741971) and unzip it to a path on your local machine. **Ensure to unzip the database in a location where there are several gigabytes of space available, otherwise the process will file.** The folder contains data for replicating the Kenya country study.
4. The M-LED platform is written in the R scientific computing language, but in some processing steps it depends on PyQGIS (Python + QGIS algorithm toolbox). A handy automatic wizard batch file (.\installdependencies.cmd) is included in the root of the M-LED repository. The file ensures that the software requirements are met on the local machine, and if they are not, it prompts the user to download and install the required software and libraries.

**NB: These steps are only necessary when setting up the environment for the first time. NB2: The `.\installdependencies.cmd` file MUST be run with administrator priviledges (right click -> run as administrator)**

## Operating the platform
1. Open the MLED_hourly.R in RStudio (R 3.6+)

3. Open the manual_parameters.R file and set the correct file path for where you have extracted the M-LED database input data and define other local parameters

3. Run the whole MLED_hourly.R script or source its individual modules

## Customising the analysis
-> See the repo's Wiki (https://github.com/giacfalk/M-LED/wiki)

## Examining the results
The results of the M-LED platform constist of:
- A geodatabase (clusters_final.gpkg)
(- A collection of raster files (*.tif) with hourly, sector-specific, monthly-variant loads)
- Figures summarising the results in the 'results_figures' folder in the repo home folder.

## Support
- Open a public query on this repo.
- Email giacomo.falchetta@feem.it

