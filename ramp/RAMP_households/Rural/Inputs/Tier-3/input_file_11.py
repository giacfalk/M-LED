# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []



#Create new rural user classes

MI = User("middle income",100)
User_list.append(MI)

#Create new appliances

#Middle-Income
MI_light_bulb = MI.Appliance(MI,3,20,3,120,0.2,10)
MI_light_bulb.windows([18*60,24*60],[0,30],0.35,[6*60,8*60])

MI_Radio = MI.Appliance(MI,1,10,2,60,0.1,5)
MI_Radio.windows([6*60+30,9*60],[18*60,21*60],0.35)

MI_TV = MI.Appliance(MI,1,70,2,90,0.1,5)
MI_TV.windows([0,0],[18*60,24*60],0.35)

MI_Fan = MI.Appliance(MI,1,50,2,300,0.2,15,occasional_use=0.8)
MI_Fan.windows([7*60,9*60],[17*60,20*60],0.35)

MI_Phone_charger = MI.Appliance(MI,2,7,2,240,0.2,10)
MI_Phone_charger.windows([0,24*60],[0,0],0)
