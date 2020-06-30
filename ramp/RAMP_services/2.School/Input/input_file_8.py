# -*- coding: utf-8 -*-

# 09 April 2020
# Nicolò Stevanato - Politecnico di Milano - Fondazione Eni Enrico Mattei

#%% Definition of the inputs

from core import User, np
User_list = []

'''
This File contains the average appliances that charcterize a Primary School in Kenya, according to PoliMi field campaign - 2020
'''

#Create new user classes

School = User("school",10)
User_list.append(School)


#Create new appliances

S_indoor_bulb = School.Appliance(School,90,12,2,360,0.2,120,wd_we_type = 0, occasional_use=0.5)
S_indoor_bulb.windows([420,600],[840,1020],0.2)

S_indoor_tubes = School.Appliance(School,130,30,2,360,0.2,120,wd_we_type = 0, occasional_use=0.5)
S_indoor_tubes.windows([420,600],[840,1020],0.2)

S_outdoor_bulb = School.Appliance(School,10,40,2,720,0,720, flat = 'yes')
S_outdoor_bulb.windows([0,360],[1080,1440],0)

S_Phone_charger = School.Appliance(School,14,7,2,300,0.2,60,wd_we_type = 0, occasional_use=0.5)
S_Phone_charger.windows([480,720],[840,1020],0.35)

S_PC = School.Appliance(School,50,100,2,180,0.2,120, occasional_use = 0.7*0.5,wd_we_type = 0)
S_PC.windows([600,720],[840,1020],0.35)

S_PC = School.Appliance(School,1,100,1,540,0.2,360,wd_we_type = 0, occasional_use=0.5)
S_PC.windows([480,1020],[0,0],0.2)

S_laptop = School.Appliance(School,10,65,1,240,0.2,120,wd_we_type = 0, occasional_use=0.5)
S_laptop.windows([480,990],[0,0],0.2)

S_printer = School.Appliance(School,1,40,2,30,0.2,1,wd_we_type = 0, occasional_use=0.5)
S_printer.windows([600,720],[840,1020],0.35)

S_photocopy = School.Appliance(School,1,400,2,30,0.2,1,wd_we_type = 0, occasional_use=0.5)
S_photocopy.windows([600,720],[840,1020],0.35)

S_projector = School.Appliance(School,6,250,2,120,0.2,60, occasional_use = 0.7*0.5,wd_we_type = 0)
S_projector.windows([600,720],[840,1020],0.35)

S_tablets = School.Appliance(School,150,10,2,120,0.2,60, occasional_use = 0.7*0.5,wd_we_type = 0)
S_tablets.windows([600,720],[840,1020],0.35)

S_TV = School.Appliance(School,2,60,2,120,0.2,30, occasional_use = 0.7*0.5,wd_we_type = 0)
S_TV.windows([600,720],[840,1020],0.35)

S_radio = School.Appliance(School,4,5,1,90,0.2,60,wd_we_type = 0, occasional_use=0.5)
S_radio.windows([720,840],[0,0],0.35)

S_router = School.Appliance(School,2,6,1,1440,0,1440, flat = 'yes')
S_router.windows([0,1440],[0,0],0)

S_pump = School.Appliance(School,1,750,1,120,0.1,30,wd_we_type = 0, occasional_use=0.5)
S_pump.windows([360,480],[0,0],0.2)

S_heater = School.Appliance(School,2,1000,1,30,0.3,10, thermal_P_var = 0.3, wd_we_type = 0, occasional_use=0.5)
S_heater.windows([480,600],[0,0],0.35)

