# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

S2 = User("School_2",1)
User_list.append(S2)

# Tier 2 School

#Create new appliances

S2_light_bulb = S2.Appliance(S2,4,60,1,180,0.2,30,wd_we_type=0)
S2_light_bulb.windows([8*60,13*60],[0,0],0.05)

S2_Phone_charger = S2.Appliance(S2,1,5,1,60,0.2,10,wd_we_type=0)
S2_Phone_charger.windows([8*60,13*60],[0,0],0.05)

S2_Radio = S2.Appliance(S2,1,7,1,30,0.2,10, occasional_use=(1/7),wd_we_type=0)
S2_Radio.windows([8*60,13*60],[0,0],0.0) 

S2_Fan = S2.Appliance(S2,1,60,1,120,0.2,30,wd_we_type=0)
S2_Fan.windows([8*60,13*60],[0,0],0.0)

S2_Computer = S2.Appliance(S2,1,70,1,30,0.15,10, occasional_use=(1/7),wd_we_type=0)
S2_Computer.windows([8*60,13*60],[0,0],0.0)