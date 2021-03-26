# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 17:58:53 2021

@author: stevo
"""


import pandas as pd


Rurals = {}
for j in range (1,6):
    Rural_x={}
    for i in range (1,13):
        Rural_x[i]=pd.read_csv('RAMP_households/Rural/Outputs/Tier-{}/output_file_{}.csv'.format(j,i),usecols=['0'])/60
    Rurals[j]=Rural_x

Rural_years = {}
for k in Rurals.keys():
    R_sum=0
    for h in Rurals[k].keys(): 
        R_sum += Rurals[k][h].values.sum()     
    Rural_years[k]=R_sum/1000    

    
Urbans = {}
for j in range (1,6):
    Urban_x={}
    for i in range (1,13):
        Urban_x[i]=pd.read_csv('RAMP_households/Urban/Outputs/Tier-{}/output_file_{}.csv'.format(j,i),usecols=['0'])/60
    Urbans[j]=Urban_x

Urban_years = {}
for k in Urbans.keys():
    R_sum=0
    for h in Urbans[k].keys(): 
        R_sum += Urbans[k][h].values.sum()     
    Urban_years[k]=R_sum/1000    


Dispensary = {}
for i in range (1,13):
    Dispensary[i]=pd.read_csv('RAMP_services/1.Health/Dispensary/Outputs/output_file_{}.csv'.format(i),usecols=['0'])/60
R_sum = 0
for h in Dispensary.keys():
    R_sum += Dispensary[h].values.sum()
Dispensary_year = R_sum/1000

HealthCentre = {}
for i in range (1,13):
    HealthCentre[i]=pd.read_csv('RAMP_services/1.Health/HealthCentre/Outputs/output_file_{}.csv'.format(i),usecols=['0'])/60
R_sum = 0
for h in HealthCentre.keys():
    R_sum += HealthCentre[h].values.sum()
HealthCentre_year = R_sum/1000

SubCountyH = {}
for i in range (1,13):
    SubCountyH[i]=pd.read_csv('RAMP_services/1.Health/SubCountyH/Outputs/output_file_{}.csv'.format(i),usecols=['0'])/60
R_sum = 0
for h in SubCountyH.keys():
    R_sum += SubCountyH[h].values.sum()
SubCountyH_year = R_sum/1000

School = {}
for i in range (1,13):
    School[i]=pd.read_csv('RAMP_services/2.School/Output/output_file_{}.csv'.format(i),usecols=['0'])/60
R_sum = 0
for h in School.keys():
    R_sum += School[h].values.sum()
School_year = R_sum/1000




