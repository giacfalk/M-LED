# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

S5 = User("School_5",1)
User_list.append(S5)

# Tier 5 School

#Create new appliances

S5_light_bulb = S5.Appliance(S5,15,60,1,480,0.1,60,wd_we_type=0)
S5_light_bulb.windows([8*60,16*60],[0,0],0.05)

S5_Phone_charger = S5.Appliance(S5,8,5,1,400,0.2,60,wd_we_type=0)
S5_Phone_charger.windows([8*60,16*60],[0,0],0.05)

S5_Radio = S5.Appliance(S5,1,7,1,60,0.2,10,wd_we_type=0)
S5_Radio.windows([8*60,16*60],[0,0],0.05) 

S5_Fan = S5.Appliance(S5,2,60,1,480,0.2,60,wd_we_type=0)
S5_Fan.windows([8*60,16*60],[0,0],0.05)

S5_Computer_Staff = S5.Appliance(S5,4,70,1,300,0.15,10, fixed='yes',wd_we_type=0)
S5_Computer_Staff.windows([8*60,13*60],[0,0],0.0)

S5_Computer = S5.Appliance(S5,4,70,1,30,0.15,10,occasional_use=(3/7),wd_we_type=0)
S5_Computer.windows([8*60,16*60],[0,0],0.0)

S5_Projector = S5.Appliance(S5,1,300,1,60,0.2,10,occasional_use=(3/7),wd_we_type=0)
S5_Projector.windows([8*60,16*60],[0,0],0.0)

S5_TV = S5.Appliance(S5,1,60,1,60,0.2,10,occasional_use=(3/7),wd_we_type=0)
S5_TV.windows([8*60,16*60],[0,0],0.0)