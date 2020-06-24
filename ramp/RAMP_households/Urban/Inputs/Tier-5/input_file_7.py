# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []

#Create new urban user classes
HIU = User("high income urban",100)
User_list.append(HIU)


#Create new appliances

#High-Income Urban
HIU_light_bulb = HIU.Appliance(HIU,4,20,2,120,0.2,10)
HIU_light_bulb.windows([1170,1440],[0,30],0.35)

HIU_CFL = HIU.Appliance(HIU,6,8,2,120,0.2,10)
HIU_CFL.windows([1170,1440],[0,30],0.35)

# HIU_Air_Conditioner = HIU.Appliance(HIU,1,1000,2,120,0.2,15)
# HIU_Air_Conditioner.windows([720,900],[1020,1260],0.35)

HIU_TV = HIU.Appliance(HIU,2,70,2,90,0.1,5)
HIU_TV.windows([720,900],[1170,1440],0.35)

HIU_DVD = HIU.Appliance(HIU,1,20,2,60,0.1,30)
HIU_DVD.windows([0,0],[1170,1440],0.35)

HIU_Speaker = HIU.Appliance(HIU,1,50,2,30,0.2,10)
HIU_Speaker.windows([720,900],[1170,1440],0.35)

HIU_Decoder = HIU.Appliance(HIU,1,15,2,90,0.1,5)
HIU_Decoder.windows([720,900],[1170,1440],0.35)

HIU_Electric_cooker = HIU.Appliance(HIU,1,800,3,30,0.1,10,thermal_P_var=0.4,occasional_use = 0.2)
HIU_Electric_cooker.windows([360,600],[720,840],0.1,[1140,1320])

HIU_Oven = HIU.Appliance(HIU,1,1500,2,60,0.1,10,thermal_P_var=0.4,occasional_use = 0.2)
HIU_Oven.windows([720,840],[1140,1320],0.1)

HIU_Kettle= HIU.Appliance(HIU,1,1000,3,10,0.1,1,occasional_use = 0.33)
HIU_Kettle.windows([360,600],[720,840],0.1,[1140,1320])

HIU_Microwave= HIU.Appliance(HIU,1,600,2,10,0.2,5,thermal_P_var=0.3,occasional_use = 0.33)
HIU_Microwave.windows([720,840],[1140,1320],0.1)

HIU_Dishwasher = HIU.Appliance(HIU,1,500,1,60,0.1,60,occasional_use = 0.33)
HIU_Dishwasher.windows([1140,1320],[0,0],0.1)

HIU_Fridge = HIU.Appliance(HIU,1,140,1,1440,0,30, 'yes',3)
HIU_Fridge.windows([0,1440],[0,0])
HIU_Fridge.specific_cycle_1(140,20,5,10)
HIU_Fridge.specific_cycle_2(140,15,5,15)
HIU_Fridge.specific_cycle_3(140,10,5,20)
HIU_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

HIU_Freezer = HIU.Appliance(HIU,1,100,1,1440,0,30, 'yes',3)
HIU_Freezer.windows([0,1440],[0,0])
HIU_Freezer.specific_cycle_1(150,20,5,10)
HIU_Freezer.specific_cycle_2(150,15,5,15)
HIU_Freezer.specific_cycle_3(150,10,5,20)
HIU_Freezer.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

HIU_PC = HIU.Appliance(HIU,1,65,2,180,0.1,10)
HIU_PC.windows([510,750],[810,1080],0.35)

HIU_Phone_charger = HIU.Appliance(HIU,3,7,2,240,0.2,10)
HIU_Phone_charger.windows([1110,1440],[0,30],0.35)

HIU_Washing_machine = HIU.Appliance(HIU,1,800,1,90,0.1,30,occasional_use = 0.33)
HIU_Washing_machine.windows([1140,1320],[0,0],0.1)

HIU_Iron = HIU.Appliance(HIU,1,1000,1,30,0.2,15,occasional_use = 0.2)
HIU_Iron.windows([1020,1320],[0,0],0.35)

HIU_water_heater = HIU.Appliance(HIU,1,500,3,60,0.2,15,thermal_P_var=0.3)
HIU_water_heater.windows([360,600],[720,840],0.35,[1140,1320])