# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

Dis = User("Dispensary",1)
User_list.append(Dis)

# Dispensary: They provide outpatient services for simple ailments such as common cold and flu, uncomplicated malaria and skin conditions.

#Create new appliances

Dis_light_bulb = Dis.Appliance(Dis,4,60,1,480,0.2,30)
Dis_light_bulb.windows([0,1440],[0,0],0.35)

Dis_Phone_charger = Dis.Appliance(Dis,2,5,1,120,0.2,30)
Dis_Phone_charger.windows([480,1200],[0,0],0.35)

Dis_VHF_Radio = Dis.Appliance(Dis,1,7,1,1440,0,1440, fixed='yes', flat='yes')
Dis_VHF_Radio.windows([0,1440],[0,0],0.0)