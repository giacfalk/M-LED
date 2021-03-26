# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:18:55 2021

@author: stevo
"""

import pandas as pd


minute_index = pd.date_range("2021-01-01 00:00:00", "2021-12-31 23:59:00", freq="1min")

### Load Evolution Plots

Rurals = {}
for j in range (1,6):
    Rural_x={}
    for i in range (1,13):
        Rural_x[i]=pd.read_csv('RAMP_households/Rural/Outputs/Tier-{}/output_file_{}.csv'.format(j,i),usecols=['0'])/60
    Rural_x = pd.concat(Rural_x.values())
    Rural_x.index = minute_index
    Rural_x = Rural_x.resample('H').mean()
    Rurals[j]=Rural_x

Urbans = {}
for j in range (1,6):
    Urban_x={}
    for i in range (1,13):
        Urban_x[i]=pd.read_csv('RAMP_households/Urban/Outputs/Tier-{}/output_file_{}.csv'.format(j,i),usecols=['0'])/60
    Urban_x = pd.concat(Urban_x.values())
    Urban_x.index = minute_index
    Urban_x = Urban_x.resample('H').mean()
    Urbans[j] = Urban_x
    
    
Rurals_daily = {}
for j in range (1,6):
    Rurals_daily[j] = Rurals[j].groupby(Rurals[j].index.hour).mean()

Urbans_daily = {}
for j in range (1,6):
    Urbans_daily[j] = Urbans[j].groupby(Urbans[j].index.hour).mean()
    
    
with pd.ExcelWriter('Rural_days.xlsx') as writer:  
    for j in range (1,6):
        Rurals_daily[j].to_excel(writer,'Tier-{}'.format(j))

with pd.ExcelWriter('Urban_days.xlsx') as writer:  
    for j in range (1,6):
        Urbans_daily[j].to_excel(writer,'Tier-{}'.format(j))


Dispensary = {}
for i in range (1,13):
    Dispensary[i]=pd.read_csv('RAMP_services/1.Health/Dispensary/Outputs/output_file_{}.csv'.format(i),usecols=['0'])/60
Dispensary = pd.concat(Dispensary.values())
Dispensary.index = minute_index
Dispensary = Dispensary.resample('H').mean()