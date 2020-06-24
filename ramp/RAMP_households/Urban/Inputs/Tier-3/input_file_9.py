# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []

#Create new urban user classes
MIU = User("middle income urban",100)
User_list.append(MIU)


#Create new appliances

#Middle Income Urban
MIU_light_bulb = MIU.Appliance(MIU,4,20,3,120,0.2,10)
MIU_light_bulb.windows([18*60,24*60],[0,30],0.35,[6*60,8*60])

MIU_Stereo = MIU.Appliance(MIU,1,50,2,30,0.2,10)
MIU_Stereo.windows([12*60,15*60],[18*60,24*60],0.35)

MIU_TV = MIU.Appliance(MIU,1,70,2,90,0.1,5)
MIU_TV.windows([0,0],[18*60,24*60],0.35)

MIU_DVD = MIU.Appliance(MIU,1,20,2,60,0.1,5,occasional_use = 0.5)
MIU_DVD.windows([0,0],[18*60,24*60],0.35)

MIU_Decoder = MIU.Appliance(MIU,1,15,2,90,0.1,5,occasional_use = 0.5)
MIU_Decoder.windows([0,0],[18*60,24*60],0.35)

MIU_Fan = MIU.Appliance(MIU,1,50,2,300,0.2,15,occasional_use = 0.4)
MIU_Fan.windows([7*60,9*60],[18*60,22*60],0.35)

MIU_PC = MIU.Appliance(MIU,1,65,2,180,0.1,10)
MIU_PC.windows([0,0],[18*60,24*60],0.35)

MIU_Phone_charger = MIU.Appliance(MIU,2,7,2,240,0.2,10)
MIU_Phone_charger.windows([0,24*60],[0,0],0)

MIU_Fridge = MIU.Appliance(MIU,1,140,1,1440,0,30, 'yes',3)
MIU_Fridge.windows([0,1440],[0,0])
MIU_Fridge.specific_cycle_1(140,20,5,10)
MIU_Fridge.specific_cycle_2(140,15,5,15)
MIU_Fridge.specific_cycle_3(140,10,5,20)
MIU_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])
