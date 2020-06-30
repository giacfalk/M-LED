# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new urban user classes
LIU = User("low income urban",100)
User_list.append(LIU)


#Create new appliances

#Low Income Urban

LIU_light_bulb = LIU.Appliance(LIU,3,20,3,120,0.2,10)
LIU_light_bulb.windows([18*60,24*60],[0,30],0.35,[6*60,8*60])

LIU_Radio = LIU.Appliance(LIU,1,10,2,60,0.1,5)
LIU_Radio.windows([6*60+30,9*60],[18*60,21*60],0.35)

LIU_TV = LIU.Appliance(LIU,1,70,2,90,0.1,5)
LIU_TV.windows([0,0],[18*60,24*60],0.35)

LIU_Fan = LIU.Appliance(LIU,1,50,2,300,0.2,15,occasional_use=0.4)
LIU_Fan.windows([7*60,9*60],[17*60,20*60],0.35)

LIU_Phone_charger = LIU.Appliance(LIU,2,7,2,240,0.2,10)
LIU_Phone_charger.windows([0,24*60],[0,0],0)
