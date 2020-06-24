# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

HMI = User("higher middle income",100)
User_list.append(HMI)


#Create new appliances

#High-Middle Income
HMI_light_bulb = HMI.Appliance(HMI,4,20,3,120,0.2,10)
HMI_light_bulb.windows([18*60,24*60],[0,30],0.35,[6*60,8*60])

# HMI_Fan = HMI.Appliance(HMI,2,50,2,300,0.2,15)
# HMI_Fan.windows([10*60,18*60],[0,0],0.35)

HMI_TV = HMI.Appliance(HMI,1,70,2,90,0.1,5)
HMI_TV.windows([12*60,15*60],[18*60,24*60],0.35)

HMI_DVD = HMI.Appliance(HMI,1,20,2,60,0.1,5,occasional_use = 0.33)
HMI_DVD.windows([0,0],[18*60,24*60],0.35)

HMI_Stereo = HMI.Appliance(HMI,1,50,2,30,0.2,10,occasional_use = 0.5)
HMI_Stereo.windows([12*60,15*60],[18*60,24*60],0.35)

HMI_Decoder = HMI.Appliance(HMI,1,15,2,90,0.1,5,occasional_use = 0.33)
HMI_Decoder.windows([0,0],[18*60,24*60],0.35)

HMI_Radio = HMI.Appliance(HMI,1,10,2,60,0.1,5)
HMI_Radio.windows([6*60+30,9*60],[18*60,21*60],0.35)

HMI_Fridge = HMI.Appliance(HMI,1,140,1,1440,0,30, 'yes',3)
HMI_Fridge.windows([0,1440],[0,0])
HMI_Fridge.specific_cycle_1(140,20,5,10)
HMI_Fridge.specific_cycle_2(140,15,5,15)
HMI_Fridge.specific_cycle_3(140,10,5,20)
HMI_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

HMI_Phone_charger = HMI.Appliance(HMI,3,7,2,240,0.2,10)
HMI_Phone_charger.windows([18*60,24*60],[0,30],0)
