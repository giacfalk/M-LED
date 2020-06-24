# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

M_NH = User("Maternity and Nursing House",1)
User_list.append(M_NH)

# Maternity and Nursing House: These are owned privately by individuals or churches and offer services roughly similar to those available at a sub-district or district hospital. 

#Create new appliances

M_NH_light_bulb = M_NH.Appliance(M_NH,20,60,1,720,0.2,60)
M_NH_light_bulb.windows([0,1440],[0,0],0.35)

M_NH_Phone_charger = M_NH.Appliance(M_NH,6,5,1,240,0.2,30)
M_NH_Phone_charger.windows([480,1200],[0,0],0.35)

M_NH_VHF_Radio = M_NH.Appliance(M_NH,1,7,1,1440,0,1440, fixed='yes', flat='yes')
M_NH_VHF_Radio.windows([0,1440],[0,0],0.0)

M_NH_Electric_Fans = M_NH.Appliance(M_NH,1,60,1,480,0.2,30)
M_NH_Electric_Fans.windows([480,1200],[0,0],0.2)

M_NH_Computer = M_NH.Appliance(M_NH,2,70,1,600,0.15,300)
M_NH_Computer.windows([480,1200],[0,0],0.2)

M_NH_Surgery_Light = M_NH.Appliance(M_NH,2,22,2,120,0.3,30,occasional_use=(3/7))
M_NH_Surgery_Light.windows([480,720],[900,1200],0.2)

M_NH_Vaccine_Refrigerator = M_NH.Appliance(M_NH,2,250,1,1440,0,30)
M_NH_Vaccine_Refrigerator.windows([0,1440],[0,0])
M_NH_Vaccine_Refrigerator.specific_cycle_1(200,20,5,10)
M_NH_Vaccine_Refrigerator.specific_cycle_2(200,15,5,15)
M_NH_Vaccine_Refrigerator.specific_cycle_3(200,10,5,20)
M_NH_Vaccine_Refrigerator.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

M_NH_Autoclave = M_NH.Appliance(M_NH,2,120,2,120,0.2,120, occasional_use=(3/7), thermal_P_var=0.4)
M_NH_Autoclave.windows([480,720],[900,1200],0.0)

M_NH_Microscope = M_NH.Appliance(M_NH,2,30,1,60,0.2,10, occasional_use=(5/7))
M_NH_Microscope.windows([480,1320],[0,0],0.0)

M_NH_Ecography = M_NH.Appliance(M_NH,1,30,1,15,0.2,5)
M_NH_Ecography.windows([480,1200],[0,0],0.0)

M_NH_Child_Incubator = M_NH.Appliance(M_NH,1,300,1,1440,0.2,30) # for now it behaves like a fridge
M_NH_Child_Incubator.windows([0,1440],[0,0])
M_NH_Child_Incubator.specific_cycle_1(200,20,5,10)
M_NH_Child_Incubator.specific_cycle_2(200,15,5,15)
M_NH_Child_Incubator.specific_cycle_3(200,10,5,20)
M_NH_Child_Incubator.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

M_NH_Blood_Incubator = M_NH.Appliance(M_NH,1,450,1,60,0.2,5,occasional_use=(5/7))
M_NH_Blood_Incubator.windows([480,1200],[0,0],0.0)