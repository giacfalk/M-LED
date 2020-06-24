# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

HC = User("Health Centre",1)
User_list.append(HC)

# All government health centres have a clinical officer as the in-charge and provide comprehensive primary care. 

#Create new appliances

HC_light_bulb = HC.Appliance(HC,30,60,1,720,0.2,60)
HC_light_bulb.windows([0,1440],[0,0],0.35)

HC_Phone_charger = HC.Appliance(HC,6,5,1,240,0.2,30)
HC_Phone_charger.windows([480,1200],[0,0],0.35)

HC_VHF_Radio = HC.Appliance(HC,2,7,1,1440,0,1440, fixed='yes', flat='yes')
HC_VHF_Radio.windows([0,1440],[0,0],0.0)

HC_Electric_Fans = HC.Appliance(HC,3,60,1,480,0.2,30)
HC_Electric_Fans.windows([480,1200],[0,0],0.2)

HC_Computer = HC.Appliance(HC,3,70,1,600,0.15,300)
HC_Computer.windows([480,1200],[0,0],0.2)

HC_Surgery_Light_Pro = HC.Appliance(HC,2,70,2,120,0.3,30, occasional_use=(4/7))
HC_Surgery_Light_Pro.windows([480,720],[900,1200],0.2)

HC_Vaccine_Refrigerator = HC.Appliance(HC,2,250,1,1440,0,30)
HC_Vaccine_Refrigerator.windows([0,1440],[0,0])
HC_Vaccine_Refrigerator.specific_cycle_1(200,20,5,10)
HC_Vaccine_Refrigerator.specific_cycle_2(200,15,5,15)
HC_Vaccine_Refrigerator.specific_cycle_3(200,10,5,20)
HC_Vaccine_Refrigerator.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HH_Child_Incubator = HH.Appliance(HH,3,300,1,1440,0.2,30) # for now it behaves like a fridge
HH_Child_Incubator.windows([0,1440],[0,0])
HH_Child_Incubator.specific_cycle_1(200,20,5,10)
HH_Child_Incubator.specific_cycle_2(200,15,5,15)
HH_Child_Incubator.specific_cycle_3(200,10,5,20)
HH_Child_Incubator.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HC_Autoclave = HC.Appliance(HC,2,120,2,120,0.2,120, thermal_P_var=0.4)
HC_Autoclave.windows([480,720],[900,1200],0.0)

HC_Microscope = HC.Appliance(HC,4,30,1,120,0.2,10,occasional_use=(5/7))
HC_Microscope.windows([480,1320],[0,0],0.0)

HC_Blood_Incubator = HC.Appliance(HC,1,450,1,120,0.2,5,occasional_use=(5/7))
HC_Blood_Incubator.windows([480,1320],[0,0],0.0)

HC_Ecography = HC.Appliance(HC,1,30,1,15,0.2,5)
HC_Ecography.windows([480,1200],[0,0],0.0)

HC_Xray = HC.Appliance(HC,1,32000,1,5,0.2,1)
HC_Xray.windows([480,1200],[0,0],0.0)