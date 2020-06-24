# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []

'''
This example input file represents an whole village-scale community,
adapted from the data used for the Journal publication. It should provide a 
complete guidance to most of the possibilities ensured by RAMP for inputs definition,
including specific modular duty cycles and cooking cycles. 
For examples related to "thermal loads", see the "input_file_2".
'''

#Create new urban user classes
HMIU = User("high-middle income urban",100)
User_list.append(HMIU)


#Create new appliances

#High Middle Income Urban
HMIU_light_bulb = HMIU.Appliance(HMIU,5,20,2,120,0.2,10)
HMIU_light_bulb.windows([1170,1440],[0,30],0.35)

HMIU_CFL = HMIU.Appliance(HMIU,3,8,2,120,0.2,10)
HMIU_CFL.windows([1170,1440],[0,30],0.35)

HMIU_Fan = HMIU.Appliance(HMIU,1,50,2,300,0.2,15, occasional_use = 0.8)
HMIU_Fan.windows([8*60,11*60],[18*60,22*60],0.35)

HMIU_Air_Conditioner = HMIU.Appliance(HMIU,1,1000,2,120,0.2,15, occasional_use = 0.2)
HMIU_Air_Conditioner.windows([720,900],[1020,1260],0.35)

HMIU_TV = HMIU.Appliance(HMIU,1,70,2,90,0.1,5)
HMIU_TV.windows([720,900],[1170,1440],0.35)

HMIU_DVD = HMIU.Appliance(HMIU,1,20,2,90,0.1,30)
HMIU_DVD.windows([0,0],[1170,1440],0.35)

HMIU_Speaker = HMIU.Appliance(HMIU,1,50,2,30,0.2,10)
HMIU_Speaker.windows([720,900],[1170,1440],0.35)

HMIU_Decoder = HMIU.Appliance(HMIU,1,15,2,90,0.1,5)
HMIU_Decoder.windows([720,900],[1170,1440],0.35)

HMIU_Fridge = HMIU.Appliance(HMIU,1,140,1,1440,0,30, 'yes',3)
HMIU_Fridge.windows([0,1440],[0,0])
HMIU_Fridge.specific_cycle_1(140,20,5,10)
HMIU_Fridge.specific_cycle_2(140,15,5,15)
HMIU_Fridge.specific_cycle_3(140,10,5,20)
HMIU_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

HMIU_Freezer = HMIU.Appliance(HMIU,1,100,1,1440,0,30, 'yes',3)
HMIU_Freezer.windows([0,1440],[0,0])
HMIU_Freezer.specific_cycle_1(150,20,5,10)
HMIU_Freezer.specific_cycle_2(150,15,5,15)
HMIU_Freezer.specific_cycle_3(150,10,5,20)
HMIU_Freezer.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

HMIU_PC = HMIU.Appliance(HMIU,1,65,3,180,0.1,10)
HMIU_PC.windows([510,750],[810,1080],0.35,[20*60,24*60])

HMIU_Phone_charger = HMIU.Appliance(HMIU,3,7,2,240,0.2,10)
HMIU_Phone_charger.windows([1110,1440],[0,30],0.35)

HMIU_Iron = HMIU.Appliance(HMIU,1,1000,1,30,0.2,15,occasional_use = 0.2)
HMIU_Iron.windows([1020,1320],[0,0],0.35)

HMIU_water_heater = HMIU.Appliance(HMIU,1,500,3,60,0.2,15, thermal_P_var=0.3)
HMIU_water_heater.windows([360,600],[720,840],0.35,[1140,1320])
