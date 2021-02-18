# Parameters
import os 

with open (os.path.expanduser("~/Desktop") + "/osgeo4w_folder_path.txt", "r") as myfile:
    osgeo_path = myfile.readline().split('\n')[0]

with open (os.path.expanduser("~/Desktop") + "/db_folder_path.txt", "r") as myfile:
    db_folder = myfile.readline().split('\n')[0]

with open (os.path.expanduser("~/Desktop") + "/repo_folder_path.txt", "r") as myfile:
    repo_folder = myfile.readline().split('\n')[0]

# Working directory
input_folder = db_folder + '/input_folder/'
processed_folder = db_folder + '/processed_folder/'
spam_folder = db_folder + '/spam_folder/'
gyga_folder = db_folder + '/gyga_folder/'
health_edu_folder = db_folder + '/health_edu_folder/'
home_repo_folder = repo_folder + '/'
pythonfolder = osgeo_path + '/apps/Python37'
output_figures_folder = repo_folder + '/output_figures/'

# Insert the file ID from Google Drive of the population, no-access population, and traveltime to nearest wholesale market files to download and process them
noacc_gd_id='1bnMe5Y9hrhi32fFQz2Pp4ilnD64BSh2S'
pop_gd_id = '1TjuEtJ0TazxqnZO36KaqEwN5wFzcYkdw'
wholesale_gd_id = '1OuTDXsQS6anLH74amPz1cyAhvH7WyInJ'
