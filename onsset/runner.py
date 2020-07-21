import os
from onsset import *
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import load_workbook

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

specs_path = specs_path = home_repo_folder + 'onsset/specs_KEN.xlsx'

# RUN_PARAM: Insert the name of the country you are working on. More countries should be separated using comma e.g. ["Malawi", "Ghana"]
countries = ['KEN']
# countries = str(input('countries: ')).split()
# countries = specs.index.tolist() if 'all' in countries else countries

choice = int(input(
	'Enter 1 to split (if multiple country run is needed), 2 to prepare/calibrate the GIS input file, 3 to run scenario(s): '))

# TODO Do we actually need option 1 anymore? I suggest removing it and readjust the options
if choice == 1:
	messagebox.showinfo('OnSSET', 'Open the csv file with GIS data')
	settlements_csv = filedialog.askopenfilename()
	messagebox.showinfo('OnSSET', 'Select the folder to save split countries')
	base_dir = filedialog.asksaveasfilename()

	print('\n --- Splitting --- \n')

	df = pd.read_csv(settlements_csv)

	for country in countries:
		print(country)
		df.loc[df[SET_COUNTRY] == country].to_csv(base_dir + '.csv', index=False)

elif choice == 2:
	SpecsData = pd.read_excel(specs_path, sheet_name='SpecsData')
	#messagebox.showinfo('OnSSET', 'Open the file containing separated countries')
	base_dir = home_repo_folder + 'onsset/input/Assist/KEN.csv'
	#messagebox.showinfo('OnSSET', 'Browse to result folder and name the calibrated file')
	output_dir = home_repo_folder + 'onsset/cali_KEN'

	print('\n --- Prepping --- \n')

	for country in countries:
		print(country)
		settlements_in_csv = base_dir
		settlements_out_csv = output_dir + '.csv'

		sett = pd.read_csv(base_dir)
        
		sett['PerCapitaDemand'] = sett['PerHHD']

		sett.to_csv(base_dir)

		onsseter = SettlementProcessor(settlements_in_csv)

		start_year = int(SpecsData.loc[0, SPE_START_YEAR])
		end_year = int(SpecsData.loc[0, SPE_END_YEAR])
		project_life = end_year - start_year
		
		pop_future_high = int(SpecsData.loc[0, 'PopEndYearHigh'])
		pop_future_low = int(SpecsData.loc[0, 'PopEndYearLow'])
		pop_actual = int(SpecsData.loc[0, SPE_POP])
		
		urban_growth_high = pop_future_high / pop_actual
		rural_growth_high = pop_future_high / pop_actual

		yearly_urban_growth_rate_high = urban_growth_high ** (1 / project_life)
		yearly_rural_growth_rate_high = rural_growth_high ** (1 / project_life)

		urban_growth_low = pop_future_low / pop_actual
		rural_growth_low = pop_future_low / pop_actual

		yearly_urban_growth_rate_low = urban_growth_low ** (1 / project_life)
		yearly_rural_growth_rate_low = rural_growth_low ** (1 / project_life)

		onsseter.condition_df()
		onsseter.grid_penalties()
		onsseter.calc_wind_cfs()

		pop_actual = SpecsData.loc[0, SPE_POP]
		pop_future_high = SpecsData.loc[0, SPE_POP_FUTURE + 'High']
		pop_future_low = SpecsData.loc[0, SPE_POP_FUTURE + 'Low']
		urban_current = SpecsData.loc[0, SPE_URBAN]
		urban_future = SpecsData.loc[0, SPE_URBAN_FUTURE]
		start_year = int(SpecsData.loc[0, SPE_START_YEAR])
		end_year = int(SpecsData.loc[0, SPE_END_YEAR])

		elec_actual = SpecsData.loc[0, SPE_ELEC]
		elec_actual_urban = SpecsData.loc[0, SPE_ELEC_URBAN]
		elec_actual_rural = SpecsData.loc[0, SPE_ELEC_RURAL]
		pop_tot = SpecsData.loc[0, SPE_POP]

		num_people_per_hh_rural = float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_RURAL])
		num_people_per_hh_urban = float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_URBAN])

		# In case there are limitations in the way grid expansion is moving in a country, this can be reflected through gridspeed.

		# In this case the parameter is set to a very high value therefore is not taken into account.
		urban_modelled = SpecsData.loc[0, SPE_URBAN_MODELLED]
		elec_modelled = SpecsData.loc[0, SPE_ELEC_MODELLED] 
		rural_elec_ratio = SpecsData.loc[0, 'rural_elec_ratio_modelled']
		urban_elec_ratio = SpecsData.loc[0, 'urban_elec_ratio_modelled'] 

		book = load_workbook(specs_path)
		writer = pd.ExcelWriter(specs_path, engine='openpyxl')
		writer.book = book
		# RUN_PARAM: Here the calibrated "specs" data are copied to a new tab called "SpecsDataCalib". This is what will later on be used to feed the model
		SpecsData.to_excel(writer, sheet_name='SpecsDataCalib', index=False)
		writer.save()
		writer.close()

		logging.info('Calibration finished. Results are transferred to the csv file')
		onsseter.df.to_csv(settlements_out_csv, index=False)

elif choice == 3:

	diesel_high = True
	diesel_tag = 'high' if diesel_high else 'low'

	#messagebox.showinfo('OnSSET', 'Open the csv file with calibrated GIS data')
	base_dir = home_repo_folder + 'onsset/cali_KEN.csv'
	#messagebox.showinfo('OnSSET', 'Browse to RESULTS folder to save outputs')
	# output_dir = filedialog.asksaveasfilename()
	output_dir = home_repo_folder + 'onsset/results'
	#messagebox.showinfo('OnSSET', 'Browse to SUMMARIES folder and name the scenario to save outputs')
	# output_dir_summaries = filedialog.asksaveasfilename()
	output_dir_summaries = home_repo_folder + 'onsset/results'

	print('\n --- Running scenario --- \n')

	ScenarioInfo = pd.read_excel(specs_path, sheet_name='ScenarioInfo')
	Scenarios = ScenarioInfo['Scenario']
	ScenarioParameters = pd.read_excel(specs_path, sheet_name='ScenarioParameters')
	SpecsData = pd.read_excel(specs_path, sheet_name='SpecsDataCalib')

	for scenario in Scenarios:
		print('Scenario: ' + str(scenario + 1))
		countryID = SpecsData.iloc[0]['CountryCode']

		popIndex = ScenarioInfo.iloc[scenario]['Population_Growth']
		tierIndex = ScenarioInfo.iloc[scenario]['Target_electricity_consumption_level']
		fiveyearIndex = ScenarioInfo.iloc[scenario]['Electrification_target_5_years']
		gridIndex = ScenarioInfo.iloc[scenario]['Grid_electricity_generation_cost']
		pvIndex = ScenarioInfo.iloc[scenario]['PV_cost_adjust']
		dieselIndex = ScenarioInfo.iloc[scenario]['Diesel_price']
		productiveIndex = ScenarioInfo.iloc[scenario]['Productive_uses_demand']
		prioIndex = ScenarioInfo.iloc[scenario]['Prioritization_algorithm']

		end_year_pop = ScenarioParameters.iloc[popIndex]['PopEndYear']
		rural_tier = ScenarioParameters.iloc[tierIndex]['RuralTargetTier']
		urban_tier = ScenarioParameters.iloc[tierIndex]['UrbanTargetTier']
		five_year_target = ScenarioParameters.iloc[fiveyearIndex]['5YearTarget']
		annual_new_grid_connections_limit = ScenarioParameters.iloc[fiveyearIndex][
												'GridConnectionsLimitThousands'] * 1000
		grid_price = ScenarioParameters.iloc[gridIndex]['GridGenerationCost']
		pv_capital_cost_adjust = ScenarioParameters.iloc[pvIndex]['PV_Cost_adjust']
		diesel_price = ScenarioParameters.iloc[dieselIndex]['DieselPrice']
		productive_demand = ScenarioParameters.iloc[productiveIndex]['ProductiveDemand']
		prioritization = ScenarioParameters.iloc[prioIndex]['PrioritizationAlgorithm']
		auto_intensification = ScenarioParameters.iloc[prioIndex]['AutoIntensificationKM']

		settlements_in_csv = base_dir
		settlements_out_csv = os.path.join(output_dir,
										   '{}-1-{}_{}_{}_{}_{}_{}.csv'.format(countryID, popIndex, tierIndex,
																					 fiveyearIndex, gridIndex, pvIndex,
																					 prioIndex))
		summary_csv = os.path.join(output_dir_summaries,
								   '{}-1-{}_{}_{}_{}_{}_{}_summary.csv'.format(countryID, popIndex, tierIndex,
																					 fiveyearIndex, gridIndex, pvIndex,
																					 prioIndex))

		onsseter = SettlementProcessor(settlements_in_csv)

		start_year = SpecsData.iloc[0][SPE_START_YEAR]
		end_year = SpecsData.iloc[0][SPE_END_YEAR]

		existing_grid_cost_ratio = SpecsData.iloc[0][SPE_EXISTING_GRID_COST_RATIO]
		num_people_per_hh_rural =float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_RURAL])
		num_people_per_hh_urban =float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_URBAN])
		max_grid_extension_dist = float(SpecsData.iloc[0][SPE_MAX_GRID_EXTENSION_DIST])
		urban_elec_ratio = float(SpecsData.iloc[0]['rural_elec_ratio_modelled'])
		rural_elec_ratio = float(SpecsData.iloc[0]['urban_elec_ratio_modelled'])
		annual_grid_cap_gen_limit = SpecsData.loc[0, 'NewGridGenerationCapacityAnnualLimitMW'] * 1000
		# annual_new_grid_connections_limit = SpecsData.loc[0, 'NewGridConnectionsAnnualLimitThousands']*1000
		pv_no = 1
		diesel_no = 1

		# RUN_PARAM: Fill in general and technology specific parameters (e.g. discount rate, losses etc.)
		Technology.set_default_values(base_year=start_year,
									  start_year=start_year,
									  end_year=end_year,
									  discount_rate=0.15)

		grid_calc = Technology(om_of_td_lines=0.02,
							   distribution_losses=float(SpecsData.iloc[0][SPE_GRID_LOSSES]),
							   connection_cost_per_hh=140,
							   base_to_peak_load_ratio=float(SpecsData.iloc[0][SPE_BASE_TO_PEAK]),
							   capacity_factor=0.65,
							   tech_life=30,
							   grid_capacity_investment=float(SpecsData.iloc[0][SPE_GRID_CAPACITY_INVESTMENT]),
							   grid_penalty_ratio=1,
							   grid_price=grid_price)

		mg_hydro_calc = Technology(om_of_td_lines=0.02,
								   distribution_losses=0.05,
								   connection_cost_per_hh=25,
								   base_to_peak_load_ratio=0.85,
								   capacity_factor=0.5,
								   tech_life=30,
								   capital_cost=4500,
								   om_costs=0.02)

		mg_wind_calc = Technology(om_of_td_lines=0.02,
								  distribution_losses=0.05,
								  connection_cost_per_hh=25,
								  base_to_peak_load_ratio=0.85,
								  capital_cost=3500,
								  om_costs=0.02,
								  tech_life=20)

		mg_pv_calc = Technology(om_of_td_lines=0.02,
								distribution_losses=0.05,
								connection_cost_per_hh=25,
								base_to_peak_load_ratio=0.85,
								tech_life=20,
								om_costs=0.015,
								capital_cost=4000 * pv_capital_cost_adjust)

		sa_pv_calc = Technology(base_to_peak_load_ratio=0.9,
								tech_life=15,
								om_costs=0.02,
								capital_cost={0.020: 6500 * pv_capital_cost_adjust,
											  0.050: 6000 * pv_capital_cost_adjust,
											  0.100: 5500 * pv_capital_cost_adjust,
											  1: 5000 * pv_capital_cost_adjust,
											  5: 4250 * pv_capital_cost_adjust},
								standalone=True)

		mg_diesel_calc = Technology(om_of_td_lines=0.02,
									distribution_losses=0.05,
									connection_cost_per_hh=25,
									base_to_peak_load_ratio=0.85,
									capacity_factor=0.7,
									tech_life=15,
									om_costs=0.1,
									efficiency=0.33,
									capital_cost=721,
									diesel_price=diesel_price,
									diesel_truck_consumption=33.7,
									diesel_truck_volume=15000)

		sa_diesel_calc = Technology(base_to_peak_load_ratio=0.5,
									capacity_factor=0.5,
									tech_life=10,
									om_costs=0.1,
									capital_cost=938,
									diesel_price=diesel_price,
									standalone=True,
									efficiency=0.28,
									diesel_truck_consumption=14,
									diesel_truck_volume=300)

		pv_diesel_hyb = Technology(om_of_td_lines=0.03,
								   distribution_losses=0.05,
								   connection_cost_per_hh=100,
								   base_to_peak_load_ratio=0.5,
								   tech_life=15,
								   diesel_price=diesel_price,
								   diesel_truck_consumption=33.7,
								   diesel_truck_volume=15000)

		# RUN_PARAM: Activating (un-commenting) lines 254-294 will run the analysis without time step and help identify differences in the two modelling approaches
		### RUN - NO TIMESTEP

		# # RUN_PARAM: Fill in the next 3 parameters accordingly. Remember this specifies a run with no intermediate step
		# time_step = end_year - start_year	 # Years between final and start year
		# year = end_year  # Final year
		# eleclimits = {end_year: 1}  # Access goal in the final year
		#
		# grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit
		# grid_connect_limit = time_step * annual_new_grid_connections_limit
		#
		# eleclimit = eleclimits[year]
		#
		# hybrid_1 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
		#											max(onsseter.df[SET_TRAVEL_HOURS]), 1, start_year, end_year,
		#											pv_no=pv_no, diesel_no=diesel_no)
		# hybrid_2 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
		#											max(onsseter.df[SET_TRAVEL_HOURS]), 2, start_year, end_year,
		#											pv_no=pv_no, diesel_no=diesel_no)
		# hybrid_3 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
		#											max(onsseter.df[SET_TRAVEL_HOURS]), 3, start_year, end_year,
		#											pv_no=pv_no, diesel_no=diesel_no)
		# hybrid_4 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
		#											max(onsseter.df[SET_TRAVEL_HOURS]), 4, start_year, end_year,
		#											pv_no=pv_no, diesel_no=diesel_no)
		# hybrid_5 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
		#											max(onsseter.df[SET_TRAVEL_HOURS]), 5, start_year, end_year,
		#											pv_no=pv_no, diesel_no=diesel_no)
		#
		# onsseter.set_scenario_variables(year, num_people_per_hh_rural, num_people_per_hh_urban, time_step, start_year,
		#								  urban_elec_ratio, rural_elec_ratio, urban_tier, rural_tier, end_year_pop,
		#								  productive_demand)
		#
		# onsseter.calculate_off_grid_lcoes(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
		#									sa_diesel_calc, hybrid_1, hybrid_2, hybrid_3, hybrid_4,
		#									hybrid_5, year, start_year, end_year, time_step)
		#
		# if year - time_step == start_year:
		#	  onsseter.current_mv_line_dist()
		#
		# onsseter.pre_electrification(grid_calc, grid_price, year, time_step, start_year)
		#
		# onsseter.run_elec(grid_calc, max_grid_extension_dist, year, start_year, end_year, time_step, grid_cap_gen_limit,
		#					grid_connect_limit, auto_intensification, prioritization)
		#
		# onsseter.results_columns(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc, sa_diesel_calc,
		#						   hybrid_1, hybrid_2, hybrid_3, hybrid_4, hybrid_5, grid_calc, year)
		#
		# onsseter.calculate_investments(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
		#								 sa_diesel_calc, grid_calc, hybrid_1, hybrid_2, hybrid_3, hybrid_4,
		#								 hybrid_5, year, end_year, time_step)
		#
		# onsseter.apply_limitations(eleclimit, year, time_step, prioritization, auto_intensification)
		#
		# onsseter.final_decision(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc, sa_diesel_calc,
		#						  grid_calc, hybrid_1, hybrid_2, hybrid_3, hybrid_4, hybrid_5, year,
		#						  end_year, time_step)
		#
		# onsseter.delete_redundant_columns(year)

		### END OF FIRST RUN

		### HERE STARTS THE ACTUAL ANALYSIS WITH THE INCLUSION OF TIME STEPS

		# RUN_PARAM: One shall define here the years of analysis (excluding start year) together with access targets per interval and timestep duration
		yearsofanalysis = [2025, 2030]
		eleclimits = {2025: five_year_target, 2030: 1}
		time_steps = {2025: 7, 2030: 5}

		elements = ["1.Population", "2.New_Connections", "3.Capacity", "4.Investment"]
		techs = ["Grid", "SA_Diesel", "SA_PV", "MG_Diesel", "MG_PV", "MG_Wind", "MG_Hydro", "MG_Hybrid"]

		sumtechs = []

		for element in elements:
			for tech in techs:
				sumtechs.append(element + "_" + tech)

		sumtechs.append('Min_cluster_pop_2030')
		sumtechs.append('Max_cluster_pop_2030')
		sumtechs.append('Min_cluster_area')
		sumtechs.append('Max_cluster_area')
		sumtechs.append('Min_existing_grid_dist')
		sumtechs.append('Max_existing_grid_dist')
		sumtechs.append('Min_road_dist')
		sumtechs.append('Max_road_dist')
		sumtechs.append('Min_investment_capita_cost')
		sumtechs.append('Max_investment_capita_cost')

		total_rows = len(sumtechs)

		df_summary = pd.DataFrame(columns=yearsofanalysis)

		for row in range(0, total_rows):
			df_summary.loc[sumtechs[row]] = "Nan"

		onsseter.current_mv_line_dist()

		for year in yearsofanalysis:
			eleclimit = eleclimits[year]
			time_step = time_steps[year]

			if year - time_step == start_year:
				grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit
				grid_connect_limit = time_step * annual_new_grid_connections_limit
			else:
				grid_cap_gen_limit = 9999999999
				grid_connect_limit = 9999999999

			hybrid_1 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
													  max(onsseter.df[SET_TRAVEL_HOURS]), 1, year - time_step, end_year,
													  pv_no=pv_no, diesel_no=diesel_no)
			hybrid_2 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
													  max(onsseter.df[SET_TRAVEL_HOURS]), 2, year - time_step, end_year,
													  pv_no=pv_no, diesel_no=diesel_no)
			hybrid_3 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
													  max(onsseter.df[SET_TRAVEL_HOURS]), 3, year - time_step, end_year,
													  pv_no=pv_no, diesel_no=diesel_no)
			hybrid_4 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
													  max(onsseter.df[SET_TRAVEL_HOURS]), 4, year - time_step, end_year,
													  pv_no=pv_no, diesel_no=diesel_no)
			hybrid_5 = pv_diesel_hyb.pv_diesel_hybrid(1, max(onsseter.df[SET_GHI]),
													  max(onsseter.df[SET_TRAVEL_HOURS]), 5, year - time_step, end_year,
													  pv_no=pv_no, diesel_no=diesel_no)

			onsseter.set_scenario_variables(year, num_people_per_hh_rural, num_people_per_hh_urban, time_step,
											start_year, urban_elec_ratio, rural_elec_ratio, urban_tier, rural_tier,
											end_year_pop, productive_demand)

			onsseter.calculate_off_grid_lcoes(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
											  sa_diesel_calc, hybrid_1, hybrid_2, hybrid_3, hybrid_4,
											  hybrid_5, year, start_year, end_year, time_step)

			onsseter.pre_electrification(grid_calc, grid_price, year, time_step, start_year)

			onsseter.run_elec(grid_calc, max_grid_extension_dist, year, start_year, end_year, time_step,
							  grid_cap_gen_limit, grid_connect_limit, auto_intensification, prioritization)

			onsseter.results_columns(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
									 sa_diesel_calc, grid_calc, hybrid_1, hybrid_2, hybrid_3, hybrid_4,
									 hybrid_5, year)

			onsseter.calculate_investments(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
										   sa_diesel_calc, grid_calc, hybrid_1, hybrid_2, hybrid_3,
										   hybrid_4, hybrid_5, year, end_year, time_step)

			onsseter.apply_limitations(eleclimit, year, time_step, prioritization, auto_intensification)

			onsseter.final_decision(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc, sa_diesel_calc,
									grid_calc, hybrid_1, hybrid_2, hybrid_3, hybrid_4, hybrid_5, year,
									end_year, time_step)

			onsseter.calc_summaries(df_summary, sumtechs, year)

		onsseter.df['FinalElecCode' + str(year)] = onsseter.df['FinalElecCode' + str(year)].astype(int)

		for i in range(len(onsseter.df.columns)):
			if onsseter.df.iloc[:, i].dtype == 'float64':
				onsseter.df.iloc[:, i] = pd.to_numeric(onsseter.df.iloc[:, i], downcast='float')
			elif onsseter.df.iloc[:, i].dtype == 'int64':
				onsseter.df.iloc[:, i] = pd.to_numeric(onsseter.df.iloc[:, i], downcast='signed')

		df_summary.to_csv(summary_csv, index=sumtechs)
		onsseter.df.to_csv(settlements_out_csv, index=False)
