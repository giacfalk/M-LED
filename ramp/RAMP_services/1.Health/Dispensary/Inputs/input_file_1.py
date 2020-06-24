# -*- coding: utf-8 -*-

# 09 April 2020
# Nicolò Stevanato - Politecnico di Milano - Fondazione Eni Enrico Mattei

#%% Definition of the inputs


from core import User, np
User_list = []

'''
This File contains the average appliances that charcterize a rural Dispensary in Kenya, according to PoliMi field campaign - 2020
'''

#Create new user classes

Dispensary = User("Dispensary",1)
User_list.append(Dispensary)

#Create new appliances

Di_indoor_bulb = Dispensary.Appliance(Dispensary, 11,12,1,300,0.2,120, wd_we_type = 0)
Di_indoor_bulb.windows([480,1020],[0,0],0.2)

Di_indoor_tubes = Dispensary.Appliance(Dispensary, 17,30,1,300,0.2,120, wd_we_type = 0)
Di_indoor_tubes.windows([480,1020],[0,0],0.2)

Di_outdoor_bulb = Dispensary.Appliance(Dispensary,3,30,2,720,0,720, 'yes', flat = 'yes')
Di_outdoor_bulb.windows([0,360],[1080,1440],0)

Di_radio = Dispensary.Appliance(Dispensary,1,7,1,120,0.2,30, wd_we_type = 0)
Di_radio.windows([720,900],[0,0],0.35)

Di_sterilizer = Dispensary.Appliance(Dispensary,1,120,1,60,0.2,20, wd_we_type = 0)
Di_sterilizer.windows([480,1020],[0,0],0.2)

Di_comp = Dispensary.Appliance(Dispensary,1,100,1,540,0.6,420, wd_we_type = 0)
Di_comp.windows([480,1020],[0,0],0.2)

Di_print = Dispensary.Appliance(Dispensary,1,40,1,20,0.2,1, wd_we_type = 0)
Di_print.windows([480,1020],[0,0],0.2)

Di_router = Dispensary.Appliance(Dispensary,1,6,1,1440,0,1440, flat = 'yes')
Di_router.windows([0,1440],[0,0],0)

# Di_heater = Dispensary.Appliance(Dispensary,1,1000,1,180,0.2,30, thermal_P_var= 0.3 ,wd_we_type = 0)
# Di_heater.windows([480,1020],[0,0],0.2)

Di_phones = Dispensary.Appliance(Dispensary,6,7,1,300,0.2,60, wd_we_type = 0)
Di_phones.windows([480,1020],[0,0],0.2)

Di_Fridge = Dispensary.Appliance(Dispensary,1,250,1,1440,0,30, 'yes',3)
Di_Fridge.windows([0,1440],[0,0])
Di_Fridge.specific_cycle_1(250,20,5,10)
Di_Fridge.specific_cycle_2(250,15,5,15)
Di_Fridge.specific_cycle_3(250,10,5,20)
Di_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])
