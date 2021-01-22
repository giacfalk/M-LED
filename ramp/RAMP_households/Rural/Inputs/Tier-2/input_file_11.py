# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []



#Create new rural user classes

LMI = User("lower middle income",100)
User_list.append(LMI)


#Create new appliances

#Lower-Middle Income
LMI_light_bulb = LMI.Appliance(LMI,3,20,3,120,0.2,10)
LMI_light_bulb.windows([18*60,24*60],[0,0],0.35,[6*60,8*60])

LMI_Radio = LMI.Appliance(LMI,1,10,2,60,0.1,5)
LMI_Radio.windows([6*60+30,9*60],[18*60,21*60],0.35)

LMI_Phone_charger = LMI.Appliance(LMI,2,7,2,240,0.2,10)
LMI_Phone_charger.windows([0,24*60],[0,0],0)
