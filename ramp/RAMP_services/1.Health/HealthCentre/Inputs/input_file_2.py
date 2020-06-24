# -*- coding: utf-8 -*-

# 09 April 2020
# Nicolò Stevanato - Politecnico di Milano - Fondazione Eni Enrico Mattei

#%% Definition of the inputs

from core import User, np
User_list = []

'''
This File contains the average appliances that charcterize a rural Health Centre in Kenya, according to PoliMi field campaign - 2020
'''

#Create new user classes

Healthcenter = User("HealthCenter",1)
User_list.append(Healthcenter)

#Create new appliances

HC_indoor_bulb = Healthcenter.Appliance(Healthcenter, 27,12,1,540,0.2,300)
HC_indoor_bulb.windows([300,1320],[0,0],0.35)

HC_indoor_tubes = Healthcenter.Appliance(Healthcenter, 38,30,1,540,0.2,300)
HC_indoor_tubes.windows([300,1320],[0,0],0.35)

HC_outdoor_bulb = Healthcenter.Appliance(Healthcenter,6,30,2,720,0,720, 'yes', flat = 'yes')
HC_outdoor_bulb.windows([0,360],[1080,1440],0)

HC_radio = Healthcenter.Appliance(Healthcenter,2,7,1,180,0.2,120)
HC_radio.windows([420,1020],[0,0],0.35)

HC_sterilizer = Healthcenter.Appliance(Healthcenter,2,120,1,120,0.2,60)
HC_sterilizer.windows([480,1020],[0,0],0.35)

HC_blood = Healthcenter.Appliance(Healthcenter,1,400,1,120,0.2,60)
HC_blood.windows([480,1020],[0,0],0.35)

HC_shaker = Healthcenter.Appliance(Healthcenter,2,10,1,120,0.2,60)
HC_shaker.windows([480,1020],[0,0],0.35)

HC_centrifuge = Healthcenter.Appliance(Healthcenter,2,120,1,120,0.2,60)
HC_centrifuge.windows([480,1020],[0,0],0.35)

HC_microscope = Healthcenter.Appliance(Healthcenter,2,30,1,120,0.2,60)
HC_microscope.windows([480,1020],[0,0],0.35)

HC_suction = Healthcenter.Appliance(Healthcenter,1,80,1,60,0.2,30, occasional_use = 0.5)
HC_suction.windows([480,1020],[0,0],0.35)

HC_incubator =  Healthcenter.Appliance(Healthcenter,2,300,1,1440,0.3,720, occasional_use = 0.75)
HC_incubator.windows([0,1440],[0,0],0)

HC_hemogram = Healthcenter.Appliance(Healthcenter,1,350,1,120,0.2,60)
HC_hemogram.windows([480,1020],[0,0],0.35)

HC_xray = Healthcenter.Appliance(Healthcenter,1,32000,1,15,0.2,1, occasional_use = 0.5)
HC_xray.windows([480,1020],[0,0],0.35)

HC_ultrasound = Healthcenter.Appliance(Healthcenter,1,100,1,60,0.2,30, occasional_use = 0.75)
HC_ultrasound.windows([480,1020],[0,0],0.35)

HC_comp = Healthcenter.Appliance(Healthcenter,2,100,1,540,0.1,480)
HC_comp.windows([480,1020],[0,0],0.35)

HC_print = Healthcenter.Appliance(Healthcenter,2,40,1,30,0.2,1)
HC_print.windows([480,1020],[0,0],0.35)

HC_router = Healthcenter.Appliance(Healthcenter,1,6,1,1440,0,1440, flat = 'yes')
HC_router.windows([0,1440],[0,0],0)

HC_heater = Healthcenter.Appliance(Healthcenter,4,1000,1,480,0.2,300, thermal_P_var= 0.3 ,occasional_use = 0.2)
HC_heater.windows([0,1440],[0,0],0.2)

HC_phones = Healthcenter.Appliance(Healthcenter,20,7,1,300,0.2,60)
HC_phones.windows([0,1440],[0,0],0.35)

HC_Fridge = Healthcenter.Appliance(Healthcenter,3,250,1,1440,0,30, 'yes',3)
HC_Fridge.windows([0,1440],[0,0])
HC_Fridge.specific_cycle_1(250,20,5,10)
HC_Fridge.specific_cycle_2(250,15,5,15)
HC_Fridge.specific_cycle_3(250,10,5,20)
HC_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

