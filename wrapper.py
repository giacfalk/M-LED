# PrElGen v0.1
# Giacomo Falchetta, Paolo Cornali, Davide Mazzoni, Nicolò Stevanato
# Version: 29/08/2019

####
import os
os.chdir(home_repo_folder)

print("Importing modules and scenario parameters")
exec(open("./manual_parameters.py").read(), globals())
exec(open("./backend.py").read(), globals())
exec(open("./scenario_baseline.py").read(), globals())

print("Running PrElGen (hourly)")
exec(open("./PrElGen_hourly.py").read(), globals())

print("Adding electrification variables")
exec(open("./to_onsset.py").read(), globals())

print("Running the electrification analysis")
print("Select 2 (calibration)")
os.system('python "' + home_repo_folder + 'onsset/runner.py"')

print("Select 3 (run the model)")
os.system('python "' + home_repo_folder + 'onsset/runner.py"')

print("Calculating costs and revenues")
exec(open("./PrElGen_economic_analysis.py").read(), globals())