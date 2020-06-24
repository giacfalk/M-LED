# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

S4 = User("School_4",1)
User_list.append(S4)

# Tier 4 School

#Create new appliances

S4_light_bulb = S4.Appliance(S4,10,60,1,480,0.1,60,wd_we_type=0)
S4_light_bulb.windows([8*60,16*60],[0,0],0.05)

S4_Phone_charger = S4.Appliance(S4,4,5,1,180,0.2,60,wd_we_type=0)
S4_Phone_charger.windows([8*60,16*60],[0,0],0.05)

S4_Radio = S4.Appliance(S4,1,7,1,30,0.2,10, occasional_use=(2/7),wd_we_type=0)
S4_Radio.windows([8*60,16*60],[0,0],0.05) 

S4_Fan = S4.Appliance(S4,1,60,1,300,0.2,30,wd_we_type=0)
S4_Fan.windows([8*60,16*60],[0,0],0.05)

S4_Computer_Staff = S4.Appliance(S4,3,70,1,300,0.15,10, fixed='yes',wd_we_type=0)
S4_Computer_Staff.windows([8*60,13*60],[0,0],0.0)

S4_Computer = S4.Appliance(S4,4,70,1,30,0.15,10,occasional_use=(2/7),wd_we_type=0)
S4_Computer.windows([8*60,16*60],[0,0],0.0)

S4_Projector = S4.Appliance(S4,1,300,1,60,0.2,10,occasional_use=(1/7),wd_we_type=0)
S4_Projector.windows([8*60,16*60],[0,0],0.0)