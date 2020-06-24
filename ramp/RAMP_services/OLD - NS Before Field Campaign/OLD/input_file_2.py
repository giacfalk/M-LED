# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []


#Create new rural user classes

MC = User("Medical Clinic",1)
User_list.append(MC)

# Medical Clinic: Most private clinics in the community are run by nurses.

#Create new appliances

MC_light_bulb = MC.Appliance(MC,10,60,1,600,0.2,30)
MC_light_bulb.windows([0,1440],[0,0],0.35)

MC_Phone_charger = MC.Appliance(MC,6,5,1,120,0.2,30)
MC_Phone_charger.windows([480,1200],[0,0],0.35)

MC_VHF_Radio = MC.Appliance(MC,1,7,1,1440,0,1440, fixed='yes', flat='yes')
MC_VHF_Radio.windows([0,1440],[0,0],0.0)

MC_Vaccine_Refrigerator = MC.Appliance(MC,1,250,1,1440,0,30)
MC_Vaccine_Refrigerator.windows([0,1440],[0,0])
MC_Vaccine_Refrigerator.specific_cycle_1(200,20,5,10)
MC_Vaccine_Refrigerator.specific_cycle_2(200,15,5,15)
MC_Vaccine_Refrigerator.specific_cycle_3(200,10,5,20)
MC_Vaccine_Refrigerator.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

MC_Autoclave = MC.Appliance(MC,1,120,2,120,0.2,120, occasional_use=(2/7), thermal_P_var=0.4)
MC_Autoclave.windows([480,720],[900,1200],0.0)