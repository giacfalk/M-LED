# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

HH = User("Hospital",1)
User_list.append(HH)

# They usually have the resources to provide comprehensive medical and surgical services. They are managed by medical superintendents.

#Create new appliances

HH_light_bulb = HH.Appliance(HH,60,60,1,900,0.2,60)
HH_light_bulb.windows([0,1440],[0,0],0.35)

HH_Phone_charger = HH.Appliance(HH,10,5,1,480,0.2,30)
HH_Phone_charger.windows([0,1440],[0,0],0.35)

HH_VHF_Radio = HH.Appliance(HH,2,7,1,1440,0,1440, fixed='yes', flat='yes')
HH_VHF_Radio.windows([0,1440],[0,0],0.0)

HH_Electric_Fans = HH.Appliance(HH,5,60,1,480,0.2,30)
HH_Electric_Fans.windows([0,1440],[0,0],0.2)

HH_HVAC = HH.Appliance(HH,5,12000,1,1440,0.2,1440, fixed='yes', flat='yes')
HH_HVAC.windows([0,1440],[0,0],0.2)

HH_Computer = HH.Appliance(HH,4,70,1,720,0.15,60)
HH_Computer.windows([0,1440],[0,0],0.2)

HH_Surgery_Light_Pro = HH.Appliance(HH,4,70,1,120,0.3,10)
HH_Surgery_Light_Pro.windows([0,1440],[0,0],0.2)

HH_Vaccine_Refrigerator = HH.Appliance(HH,2,250,1,1440,0,30)
HH_Vaccine_Refrigerator.windows([0,1440],[0,0])
HH_Vaccine_Refrigerator.specific_cycle_1(200,20,5,10)
HH_Vaccine_Refrigerator.specific_cycle_2(200,15,5,15)
HH_Vaccine_Refrigerator.specific_cycle_3(200,10,5,20)
HH_Vaccine_Refrigerator.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HH_Autoclave = HH.Appliance(HH,2,120,2,120,0.2,120, thermal_P_var=0.4)
HH_Autoclave.windows([480,720],[900,1200],0.0)

HH_Microscope = HH.Appliance(HH,6,30,1,120,0.2,10)
HH_Microscope.windows([480,1320],[0,0],0.0)

HH_Blood_Incubator = HH.Appliance(HH,1,450,1,120,0.2,5)
HH_Blood_Incubator.windows([480,1320],[0,0],0.0)

HH_Ecography = HH.Appliance(HH,1,30,1,30,0.2,5)
HH_Ecography.windows([480,1200],[0,0],0.0)

HH_Xray = HH.Appliance(HH,1,32000,1,5,0.2,1)
HH_Xray.windows([480,1200],[0,0],0.0)

HH_Child_Incubator = HH.Appliance(HH,4,300,1,1440,0.2,30) # for now it behaves like a fridge
HH_Child_Incubator.windows([0,1440],[0,0])
HH_Child_Incubator.specific_cycle_1(200,20,5,10)
HH_Child_Incubator.specific_cycle_2(200,15,5,15)
HH_Child_Incubator.specific_cycle_3(200,10,5,20)
HH_Child_Incubator.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HH_MRI = HH.Appliance(HH,1,18000,1,60,0.2,30)
HH_MRI.windows([480,1320],[0,0],0.0)

HH_Dental_Apparatus = HH.Appliance(HH,1,550,1,120,0.2,60, occasional_use=(4/7))
HH_Dental_Apparatus.windows([480,1200],[0,0],0.0)

