#Crop processing machinery: energy demand
# Import csv of energy consumption by crop 
energy_crops = read.csv(paste0(input_folder,'crop_processing.csv'))

# Extract yield 
# Import all Yield (kg/ha) cropland layers (Default datasets used: MapSPAM)
# NB: when using MapSPAM use harvested area, which accounts for multiple growing seasons per year)
files = list.files(path = paste0(spam_folder, "spam2010v1r0_global_yield.geotiff") , pattern = 'r.tif')

for (X in files){
  a = paste0("Y_" , gsub("_r.tif", "", gsub("spam2010v1r0_global_yield_", "", X)))
  clusters[a] <- exactextractr::exact_extract(raster(paste0(spam_folder, "spam2010v1r0_global_yield.geotiff/", X)), clusters, fun="mean")
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters <- clusters %>%  mutate(!!paste0("yield_", gsub("_r.tif", "", gsub("spam2010v1r0_global_yield_", "", X)), "_tot") := (!!as.name(a)) * pull(!!aa[paste0("A_", gsub("_r.tif", "", gsub("spam2010v1r0_global_yield_", "", X)))])) 
}

# Multiply yearly yield of each crop by unit processing energy requirement to estimate yearly demand in each cluster as the sum of each crop processing energy demand
for (X in energy_crops$ï..Crop){
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0("kwh_" , X , "_tot")] = pull(aa[paste0("yield_", X, "_tot")]) * energy_crops$kwh_kg[energy_crops$ï..Crop == X] 
}

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters['kwh_cp_tt'] = as.vector(aa %>%  select(starts_with('kwh')) %>% rowSums(na.rm = T) %>% as.numeric())

crops = read_xlsx(paste0(input_folder ,'crops_cfs_ndays_months.xlsx'))

# processing to take place in post-harvesting months: for each crop 1) take harvesting date 2) take plantation months. for those months between 1 and 2 equally allocate crop processing

crops <-  crops[crops$crop %in% energy_crops$ï..Crop, ]

for (i in 1:nrow(crops)){
  for (m in 1:12){
  daily=data.frame("daily" = c(1:729))
  daily$date = seq(as.Date("2019-01-01"), length.out = 729, by = "days")
  daily$month = lubridate::month(daily$date)
  daily$day = lubridate::day(daily$date)
  
  pm1= as.Date(paste0(crops[i, 'pm_1'], "2019"), format= "%d%m%Y")
  pm2= as.Date(paste0(crops[i, 'pm_2'], "2019"), format= "%d%m%Y")
  
  a =  filter(daily, date>= pm1 + as.numeric(crops[i, 'nd_1']) + as.numeric(crops[i, 'nd_2']) + as.numeric(crops[i, 'nd_3']) + as.numeric(crops[i, 'nd_4']))
  a =  filter(a, date < as.Date("2020-03-15", format="%Y-%m-%d"))
  a =  filter(a, lubridate::month(month) == m)
  a = nrow(a)
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
clusters[paste0("kwh_cp" , as.character(crops$crop[i]) , "_" , as.character(m))] = aa[paste0("kwh_" , as.character(crops$crop[i]) , "_tot")] / a

}}

#### continue from here #####

# sum all crops by months
for (z in 1:12){
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  aa <- aa %>% select(starts_with('kwh_cp')) %>% select(ends_with(paste0('_' , as.character(z)))) %>% mutate(a=rowSums(., na.rm = T))
  
  clusters = clusters %>% mutate(!!as.name(paste0('monthly_kwh_cropproc', "_" , as.character(z))) := aa$a)

}

# simulate daily profile
load_curve_cp = c(0, 0, 0, 0, 0, 0, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0, 0, 0, 0, 0, 0)

for (k in 1:12){
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  clusters[paste0('kwh_cropproc_tt_', as.character(k))] = pull(aa[paste0('monthly_kwh_cropproc' , "_" , as.character(k))])/30
  
}

for (k in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
  clusters[paste0('kwh_cropproc' , as.character(k) , "_" ,  as.character(i))] = pull(aa[paste0('kwh_cropproc_tt_' , as.character(k))])*load_curve_cp[i]
  
  }}

for (k in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
  clusters[paste0('kwh_cropproc' , as.character(k) , "_" ,  as.character(i))] = pull(aa[paste0('kwh_cropproc' , as.character(k) , "_" ,  as.character(i))])/pull(aa[paste0('kwh_cropproc_tt_' , as.character(k))])
  
  }}

