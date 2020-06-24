# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

S1 = User("School_1",1)
User_list.append(S1)

# Tier 1 School

#Create new appliances

S1_light_bulb = S1.Appliance(S1,2,60,1,120,0.2,20,wd_we_type=0)
S1_light_bulb.windows([8*60,13*60],[0,0],0.05)

S1_Phone_charger = S1.Appliance(S1,1,5,1,60,0.2,10,wd_we_type=0)
S1_Phone_charger.windows([8*60,13*60],[0,0],0.05)

S1_Radio = S1.Appliance(S1,1,7,1,30,0,10,wd_we_type=0)
S1_Radio.windows([8*60,13*60],[0,0],0.05)