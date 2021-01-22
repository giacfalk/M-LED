# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

LI = User("low income",100)
User_list.append(LI)


#Create new appliances

#Low-Income
LI_light_bulb = LI.Appliance(LI,2,20,2,120,0.2,10)
LI_light_bulb.windows([18*60,24*60],[0,0],0.35)

LI_Phone_charger = LI.Appliance(LI,2,7,2,240,0.2,10)
LI_Phone_charger.windows([0,24*60],[0,0],0)