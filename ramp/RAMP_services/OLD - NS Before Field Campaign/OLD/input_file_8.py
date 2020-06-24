# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

S3 = User("School_3",1)
User_list.append(S3)

# Tier 3 School

#Create new appliances

S3_light_bulb = S3.Appliance(S3,6,60,1,300,0.2,30,wd_we_type=0)
S3_light_bulb.windows([8*60,16*60],[0,0],0.05)

S3_Phone_charger = S3.Appliance(S3,2,5,1,120,0.2,30,wd_we_type=0)
S3_Phone_charger.windows([8*60,16*60],[0,0],0.05)

S3_Radio = S3.Appliance(S3,1,7,1,30,0.2,10, occasional_use=(2/7),wd_we_type=0)
S3_Radio.windows([8*60,16*60],[0,0],0.05) 

S3_Fan = S3.Appliance(S3,1,60,1,300,0.2,30,wd_we_type=0)
S3_Fan.windows([8*60,16*60],[0,0],0.05)

S3_Computer_Staff = S3.Appliance(S3,2,70,1,300,0.15,10, fixed='yes',wd_we_type=0)
S3_Computer_Staff.windows([8*60,13*60],[0,0],0.0)

S3_Computer = S3.Appliance(S3,2,70,1,30,0.15,10,occasional_use=(2/7),wd_we_type=0)
S3_Computer.windows([8*60,16*60],[0,0],0.0)

S3_Projector = S3.Appliance(S3,1,300,1,30,0.2,10,occasional_use=(1/7),wd_we_type=0)
S3_Projector.windows([8*60,16*60],[0,0],0.0)