# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes
HI = User("high income",100)
User_list.append(HI)


#Create new appliances

#High-Income
HI_light_bulb = HI.Appliance(HI,6,20,3,120,0.2,10)
HI_light_bulb.windows([18*60,24*60],[0,30],0.35,[6*60,8*60])

HI_Fan = HI.Appliance(HI,2,50,2,300,0.2,15,occasional_use=0.2)
HI_Fan.windows([9*60,21*60],[0,0],0.35)

HI_TV = HI.Appliance(HI,2,70,2,90,0.1,5)
HI_TV.windows([12*60,15*60],[18*60,24*60],0.35)

HI_Radio = HI.Appliance(HI,1,10,2,60,0.1,5)
HI_Radio.windows([6*60+30,9*60],[18*60,21*60],0.35)

HI_DVD = HI.Appliance(HI,1,20,2,60,0.1,30)
HI_DVD.windows([0,0],[18*60,24*60],0.35)

HI_Stereo = HI.Appliance(HI,1,50,2,30,0.2,10)
HI_Stereo.windows([12*60,15*60],[18*60,24*60],0.35)

HI_Decoder = HI.Appliance(HI,1,15,2,90,0.1,5)
HI_Decoder.windows([12*60,15*60],[18*60,24*60],0.35)

HI_Toaster= HI.Appliance(HI,1,1000,3,5,0.2,1,occasional_use = 0.33)
HI_Toaster.windows([360,600],[720,840],0.1,[1140,1320])

HI_Fridge = HI.Appliance(HI,1,140,1,1440,0,30, 'yes',3)
HI_Fridge.windows([0,1440],[0,0])
HI_Fridge.specific_cycle_1(140,20,5,10)
HI_Fridge.specific_cycle_2(140,15,5,15)
HI_Fridge.specific_cycle_3(140,10,5,20)
HI_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

HI_PC = HI.Appliance(HI,1,65,3,180,0.1,10)
HI_PC.windows([8*60+30,12*60+30],[15*60,18*60],0.35,[20*60,24*60])

HI_Phone_charger = HI.Appliance(HI,3,7,2,240,0.2,10)
HI_Phone_charger.windows([18*60,24*60],[0,30],0.2)

HI_Iron = HI.Appliance(HI,1,1000,1,30,0.2,15, wd_we_type= 1)
HI_Iron.windows([9*60,12*60],[0,0],0.35)
