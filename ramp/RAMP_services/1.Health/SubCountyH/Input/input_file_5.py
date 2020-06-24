# -*- coding: utf-8 -*-

# 09 April 2020
# Nicolò Stevanato - Politecnico di Milano - Fondazione Eni Enrico Mattei

#%% Definition of the inputs

from core import User, np
User_list = []

'''
This File contains the average appliances that charcterize a SubCounty Hospital in Kenya, according to PoliMi field campaign - 2020
'''

#Create new user classes

SCHospital = User("SCHospital",1)
User_list.append(SCHospital)


#Create new appliances

SCH_indoor_bulb = SCHospital.Appliance(SCHospital, 60,12,1,960,0.2,720)
SCH_indoor_bulb.windows([0,1440],[0,0],0)

SCH_indoor_tubes = SCHospital.Appliance(SCHospital, 60,30,1,960,0.2,720)
SCH_indoor_tubes.windows([0,1440],[0,0],0)

SCH_outdoor_bulb = SCHospital.Appliance(SCHospital,20,30,2,720,0,720, 'yes', flat = 'yes')
SCH_outdoor_bulb.windows([0,360],[1080,1440],0)

SCH_radio = SCHospital.Appliance(SCHospital,6,7,1,300,0.2,180)
SCH_radio.windows([420,1080],[0,0],0.35)

SCH_teather = SCHospital.Appliance(SCHospital,5,70,1,300,0.2,240, occasional_use = 0.7)
SCH_teather.windows([480,1020],[0,0],0.35)

SCH_dental = SCHospital.Appliance(SCHospital,1,550,1,300,0.2,60, occasional_use = 0.7)
SCH_dental.windows([480,1020],[0,0],0.35)

SCH_sterilizer = SCHospital.Appliance(SCHospital,4,120,1,240,0.2,120)
SCH_sterilizer.windows([480,1020],[0,0],0.35)

SCH_shaker = SCHospital.Appliance(SCHospital,4,10,1,240,0.2,120)
SCH_shaker.windows([480,1020],[0,0],0.35)

SCH_centrifuge = SCHospital.Appliance(SCHospital,4,120,1,240,0.2,120)
SCH_centrifuge.windows([480,1020],[0,0],0.35)

SCH_microscope = SCHospital.Appliance(SCHospital,4,30,1,240,0.2,120)
SCH_microscope.windows([480,1020],[0,0],0.35)

SCH_blood = SCHospital.Appliance(SCHospital,2,400,1,240,0.2,120)
SCH_blood.windows([480,1020],[0,0],0.35)

SCH_hemo = SCHospital.Appliance(SCHospital,2,350,1,240,0.2,120)
SCH_hemo.windows([480,1020],[0,0],0.35)
					
SCH_suction = SCHospital.Appliance(SCHospital,6,80,1,240,0.2,120)
SCH_suction.windows([480,1020],[0,0],0.35)

SCH_incubator = SCHospital.Appliance(SCHospital,10,300,1,1440,0,1440)
SCH_incubator.windows([0,1440],[0,0],0)

 
SCH_comp = SCHospital.Appliance(SCHospital,25,100,1,540,0.1,480)
SCH_comp.windows([480,1020],[0,0],0.35)

SCH_print = SCHospital.Appliance(SCHospital,2,40,1,60,0.2,1)
SCH_print.windows([480,1020],[0,0],0.35)

SCH_projector = SCHospital.Appliance(SCHospital,1,250,1,120,0.2,60, occasional_use = 0.3)
SCH_projector.windows([480,1020],[0,0],0.35)

SCH_photocopy = SCHospital.Appliance(SCHospital,2,400,1,60,0.2,1)
SCH_photocopy.windows([480,1020],[0,0],0.35)

SCH_Tv = SCHospital.Appliance(SCHospital,5,60,1,960,0.1,840)
SCH_Tv.windows([360,1320],[0,0],0.35)

SCH_router = SCHospital.Appliance(SCHospital,2,10,1,1440,0,1440, flat = 'yes')
SCH_router.windows([0,1440],[0,0],0)

SCH_elheater = SCHospital.Appliance(SCHospital,2,1200,1,60,0.2,15, thermal_P_var=0.3 ,occasional_use = 0.8)
SCH_elheater.windows([0,360],[1080,1440],0.2)

SCH_pump = SCHospital.Appliance(SCHospital,1,750,1,120,0.1,60)
SCH_pump.windows([360,480],[0,0],0.2)

SCH_nebulizer = SCHospital.Appliance(SCHospital,2,140,1,240,0.2,120)
SCH_nebulizer.windows([0,1440],[0,0],0)

SCH_Xray = SCHospital.Appliance(SCHospital,2,32000,1,30,0.2,1, occasional_use = 0.70)
SCH_Xray.windows([480,1020],[0,0],0.2)

SCH_MRI = SCHospital.Appliance(SCHospital,2,18000,1,90,0.2,30, occasional_use = 0.50)
SCH_MRI.windows([480,1020],[0,0],0.2)

SCH_ultrasound = SCHospital.Appliance(SCHospital,5,30,1,90,0.2,30)
SCH_ultrasound.windows([480,1020],[0,0],0.2)

SCH_phones = SCHospital.Appliance(SCHospital,50,7,1,600,0.2,60)
SCH_phones.windows([0,1440],[0,0],0)

SCH_Fridge = SCHospital.Appliance(SCHospital,12,250,1,1440,0,30, 'yes',3)
SCH_Fridge.windows([0,1440],[0,0])
SCH_Fridge.specific_cycle_1(250,20,5,10)
SCH_Fridge.specific_cycle_2(250,15,5,15)
SCH_Fridge.specific_cycle_3(250,10,5,20)
SCH_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

SCH_HVAC = SCHospital.Appliance(SCHospital,1,12000,1,1440,0,1440, fixed='yes', flat='yes')
SCH_HVAC.windows([0,1440],[0,0],0.2)

SCH_dispenser = SCHospital.Appliance(SCHospital,2,200,1,1440,0,30, 'yes',3)
SCH_dispenser.windows([0,1440],[0,0])
SCH_dispenser.specific_cycle_1(200,20,5,10)
SCH_dispenser.specific_cycle_2(200,15,5,15)
SCH_dispenser.specific_cycle_3(200,10,5,20)
SCH_dispenser.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

