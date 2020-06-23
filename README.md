[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

![alt text](https://github.com/giacfalk/PrElGen/blob/master/logo.png?raw=true)

####
The model has been developed and tested in a Windows 10 environment. 

[Setting up the environment]:
- Install QGIS (v3.8+) via OSGeo4W network installer (http://qgis.org/). In the installation process, choose the 'advanced mode' and make sure you install qgis, saga-ltr, grass-gis, and python-tckl. 
- Clone this GitHub repository and uncompress the zip archive.
- Launch the 'installdependencies.cmd' file. This will call Python from the command prompt to install the required Python libraries, if they are not already installed on your computer. 

####
[Downloading the input data]:
- Download the input_folder from the PrElGen Zenodo repository: [https://zenodo.org/...]

####
[Running the analysis]:
- Launch QGIS. Open the Python Console from the 
- Make sure you have enough free space on your hard drive. Usually at least 20 gigabytes are necessary for the temporary processing. Note that after the conclusion of the data processing, this space will be freed up.
- Manually edit the 'manualparameters.py' file (the file is commented extensively to support the user in this operation)
- Run the PrElGen.py script. 
- You will be prompted several times, with the following questions:
  - ....
  
####
[Analysing the results]:
- PrElGen produces an array of default graphs and statistics, which are inserted in the 'output_figures' folder.

####
[Support]:
- Open a public query on this repo.
- Email giacomo.falchetta@feem.it

