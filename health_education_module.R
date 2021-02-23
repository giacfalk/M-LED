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
  assign(paste0('health1' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/Dispensary/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('health2' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/HealthCentre/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('health3' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('health4' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('health5' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/1.Health/SubCountyH/Outputs/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
}


for (i in 1:12){
  assign(paste0('edu' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_services/2.School/Output/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 

}

for (m in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters = mutate(clusters, !!paste0('er_hc_' , as.character(m) , "_" , as.character(i)) := pull(!!as.name(paste0('health1', "_" , as.character(m))))[i] * clusters$beds_1 + pull(!!as.name(paste0('health2', "_" , as.character(m))))[i]/45 * clusters$beds_2 + pull(!!as.name(paste0('health3', "_" , as.character(m))))[i]/150 * clusters$beds_3 + pull(!!as.name(paste0('health4', "_" , as.character(m))))[i] /450 * clusters$beds_4 + pull(!!as.name(paste0('health5', "_" , as.character(m))))[i]/2000 * clusters$beds_5)
            
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters = mutate(clusters, !!paste0('er_sch_' , as.character(m) , "_" , as.character(i)) := pull(!!as.name(paste0('edu', "_" , as.character(m))))[i] * clusters$pupils_1 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i]/45 * clusters$pupils_2 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i]/150 * clusters$pupils_3 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i] /450 * clusters$pupils_4 + pull(!!as.name(paste0('edu', "_" , as.character(m))))[i]/2000 * clusters$pupils_5)              

    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
# Schools and healthcare facilities are assumed to be already electrified in the total electricity access level in the cluster is > 0.75
clusters[paste0('er_hc_' , as.character(m) , "_" , as.character(i))] = ifelse(clusters$elrate > 0.75, 0,  pull(aa[paste0('er_hc_' , as.character(m) , "_" , as.character(i))]))

clusters[paste0('er_sch_' , as.character(m) , "_" , as.character(i))] = ifelse(clusters$elrate > 0.75, 0,  pull(aa[paste0('er_sch_' , as.character(m) , "_" , as.character(i))]))

}}

# Generate variable for total daily demand and variables as shares of the daily demand
idx = which(grepl("er_hc_", colnames(clusters))==TRUE)
clusters$er_hc_tt = rowSums(aa[idx])

for (m in 1:12){
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  idx = which(grepl(paste0("er_hc_", as.character(m)), colnames(clusters))==TRUE) 
  clusters[paste0('er_hc_tt' ,"_monthly_" , as.character(m))] = rowSums(aa[idx])
}

for (m in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters[paste0('er_hc_' , as.character(m) , "_" , as.character(i))] = pull(aa[paste0('er_hc_' , as.character(m) , "_" , as.character(i))]) / pull(aa[paste0('er_hc_tt' ,"_monthly_" , as.character(m))])
  }}

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

idx = which(grepl("er_sch_", colnames(clusters))==TRUE)
clusters$er_sch_tt = rowSums(aa[idx])

for (m in 1:12){
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  idx = which(grepl(paste0("er_sch_", as.character(m)), colnames(clusters))==TRUE) 
  clusters[paste0('er_sch_tt' ,"_monthly_" , as.character(m))] = rowSums(aa[idx])
}

for (m in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters[paste0('er_sch_' , as.character(m) , "_" , as.character(i))] = pull(aa[paste0('er_sch_' , as.character(m) , "_" , as.character(i))]) / pull(aa[paste0('er_sch_tt' ,"_monthly_" , as.character(m))])
  }}
