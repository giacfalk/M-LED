# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new urban user classes
LMIU = User("low-middle income urban",100)
User_list.append(LMIU)


#Create new appliances

#Low-Middle Income Urban

LMIU_light_bulb = LMIU.Appliance(LMIU,4,20,3,120,0.2,10)
LMIU_light_bulb.windows([18*60,24*60],[0,30],0.35,[6*60,8*60])

LMIU_Radio = LMIU.Appliance(LMIU,1,10,2,60,0.1,5)
LMIU_Radio.windows([6*60+30,9*60],[18*60,21*60],0.35)

LMIU_Stereo = LMIU.Appliance(LMIU,1,50,2,30,0.2,10)
LMIU_Stereo.windows([12*60,15*60],[18*60,24*60],0.35)

LMIU_TV = LMIU.Appliance(LMIU,1,70,2,90,0.1,5)
LMIU_TV.windows([0,0],[18*60,24*60],0.35)

LMIU_DVD = LMIU.Appliance(LMIU,1,20,2,60,0.1,5,occasional_use = 0.33)
LMIU_DVD.windows([0,0],[18*60,24*60],0.35)

LMIU_Decoder = LMIU.Appliance(LMIU,1,15,2,90,0.1,5,occasional_use = 0.33)
LMIU_Decoder.windows([0,0],[18*60,24*60],0.35)

LMIU_Fan = LMIU.Appliance(LMIU,1,50,2,300,0.2,15,occasional_use=0.4)
LMIU_Fan.windows([7*60,9*60],[17*60,20*60],0.35)

LMIU_Phone_charger = LMIU.Appliance(LMIU,2,7,2,240,0.2,10)
LMIU_Phone_charger.windows([0,24*60],[0,0],0)

LMIU_Fridge = LMIU.Appliance(LMIU,1,140,1,1440,0,30, 'yes',3)
LMIU_Fridge.windows([0,1440],[0,0])
LMIU_Fridge.specific_cycle_1(140,20,5,10)
LMIU_Fridge.specific_cycle_2(140,15,5,15)
LMIU_Fridge.specific_cycle_3(140,10,5,20)
LMIU_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])
