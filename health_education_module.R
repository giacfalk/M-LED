for (f in c("pupils_1","pupils_2","pupils_3","pupils_4","pupils_5")){
  
  r <- fasterize::fasterize(primaryschools %>% st_transform(3395) %>% st_buffer(500) %>% st_transform(4326), ID_raster, field = f)
  clusters[f] <- exact_extract(r, clusters, fun="sum") 
  }

for (f in c("beds_1", "beds_2","beds_3","beds_4","beds_5")){
  
  r <- fasterize::fasterize(healthcarefacilities %>% st_transform(3395) %>% st_buffer(500) %>% st_transform(4326), ID_raster, field = f)
  clusters[f] <- exact_extract(r, clusters, fun="sum") 
}

# Estimate the yearly electric demand from healthcare and education facilities
# define consumption of facility types (kWh/facility/year)
for (i in 1:12){
  assign(paste0('health1' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/Dispensary/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000)) 
  
  assign(paste0('health2' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/HealthCentre/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000)) 
  
  assign(paste0('health3' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000)) 
  
  assign(paste0('health4' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)*1.3/1000)) 
  
  assign(paste0('health5' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)*1.6/1000)) 
  
}


for (i in 1:12){
  assign(paste0('edu' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/2.School/Output/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000)) #/10 schools simulated 

}

for (m in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters = mutate(clusters, !!paste0('er_hc_' , as.character(m) , "_" , as.character(i)) := pull(!!as.name(paste0('health1', "_" , as.character(m))))[i] * clusters$beds_1 + pull(!!as.name(paste0('health2', "_" , as.character(m))))[i] * clusters$beds_2 + pull(!!as.name(paste0('health3', "_" , as.character(m))))[i] * clusters$beds_3 + pull(!!as.name(paste0('health4', "_" , as.character(m))))[i] * clusters$beds_4 + pull(!!as.name(paste0('health5', "_" , as.character(m))))[i] * clusters$beds_5)
            
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters = mutate(clusters, !!paste0('er_sch_' , as.character(m) , "_" , as.character(i)) := pull(!!as.name(paste0('edu', "_" , as.character(m))))[i] /700 * clusters$pupils_1 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i] /700 * clusters$pupils_2 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i] /700 * clusters$pupils_3 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i] /700 * clusters$pupils_4 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i] /700 * clusters$pupils_5)              

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

# Schools and healthcare facilities are assumed to be already electrified in the total electricity access level in the cluster is > 0.75
clusters[paste0('er_hc_' , as.character(m) , "_" , as.character(i))] = ifelse(clusters$elrate > 0.75, 0,  pull(aa[paste0('er_hc_' , as.character(m) , "_" , as.character(i))]))

clusters[paste0('er_sch_' , as.character(m) , "_" , as.character(i))] = ifelse(clusters$elrate > 0.75, 0,  pull(aa[paste0('er_sch_' , as.character(m) , "_" , as.character(i))]))

}}

for (m in 1:12){
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  out = aa %>% dplyr::select(starts_with(paste0("er_hc_", as.character(m), "_"))) %>% rowSums(.)
  clusters[paste0('er_hc_tt' ,"_monthly_" , as.character(m))] = out

}

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

# Generate variable for total daily demand and variables as shares of the daily demand
out = aa %>% dplyr::select(starts_with("er_hc_tt_monthly_")) %>% rowSums(.)
clusters$er_hc_tt = out

for (m in 1:12){
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  out = aa %>% dplyr::select(starts_with(paste0("er_sch_", as.character(m), "_"))) %>% rowSums(.)
  clusters[paste0('er_sch_tt' ,"_monthly_" , as.character(m))] = out
  
}


aa <- clusters
aa$geometry=NULL
aa$geom=NULL

out = aa %>% dplyr::select(starts_with("er_sch_tt_monthly_")) %>% rowSums(.)
clusters$er_sch_tt = out

sch_monthly_demand <- ggplot(data=clusters %>% dplyr::select(starts_with('er_sch_tt_monthly_')) %>% gather(., key="key", value="value", 1:12))+
  geom_sf(aes(fill=value/1e6))+
  scale_fill_viridis_c(trans="log", name="GWh")+
  facet_wrap(vars(key))

hc_monthly_demand <- ggplot(data=clusters %>% dplyr::select(starts_with('er_hc_tt_monthly_')) %>% gather(., key="key", value="value", 1:12))+
  geom_sf(aes(fill=value/1e6))+
  scale_fill_viridis_c(trans="log", name="GWh")+
  facet_wrap(vars(key))
