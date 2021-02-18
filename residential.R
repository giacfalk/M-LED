for (i in 1:12){
  assign(paste0('rur1' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Rural/Outputs/Tier-1/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('rur2' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Rural/Outputs/Tier-2/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('rur3' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Rural/Outputs/Tier-3/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('rur4' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Rural/Outputs/Tier-4/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('rur5' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Rural/Outputs/Tier-5/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 

}

for (i in 1:12){
  assign(paste0('urb1' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Urban/Outputs/Tier-1/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('urb2' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Urban/Outputs/Tier-2/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('urb3' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Urban/Outputs/Tier-3/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('urb4' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Urban/Outputs/Tier-4/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
  assign(paste0('urb5' , "_" , as.character(i)), read.csv(paste0(home_repo_folder , 'ramp/RAMP_households/Urban/Outputs/Tier-5/output_file_' , as.character(i) , '.csv')) %>% rename(values = X0, minutes = X) %>% mutate(hour=minutes%/%60%%24) %>% group_by(hour) %>% summarise(values=mean(values)/1000/100)) 
  
}

# Energy efficiency improvements. For now, we will assume that efficiency improvements are stronger by 5% for each tier higher
# rur1= rur1- eff_impr_rur1*rur1
# rur2= rur2- eff_impr_rur2*rur2
# rur3= rur3- eff_impr_rur3*rur3
# rur4= rur4- eff_impr_rur4*rur4
# rur5= rur5- eff_impr_rur5*rur5
# 
# urb1= urb1- eff_impr_urb1*urb1
# urb2= urb2- eff_impr_urb2*urb2
# urb3= urb3- eff_impr_urb3*urb3
# urb4= urb4- eff_impr_urb4*urb4
# urb5= urb5- eff_impr_urb5*urb5

# define if clsuter is prevalently urban or rural
clusters$isurban <- exact_extract(urbrur, clusters, fun="majority")

####
# Calculate the number of people in each tier in each cluster
raster_tiers <- crop(raster_tiers, ext)

population <- population250
population <- projectRaster(population, raster_tiers)

r1 <- raster_tiers
values(r1) <- ifelse(values(raster_tiers)==1, values(population), 0)

r2 <- raster_tiers
values(r2) <- ifelse(values(raster_tiers)==2, values(population), 0)

r3 <- raster_tiers
values(r3) <- ifelse(values(raster_tiers)==3, values(population), 0)

r4 <- raster_tiers
values(r4) <- ifelse(values(raster_tiers)==4, values(population), 0)

raster_tiers <- stack(r1, r2, r3, r4)

accpop <- exact_extract(raster_tiers, clusters, fun="sum")
accpop <- as.data.frame(accpop)
colnames(accpop) <- c("acc_pop_t1", "acc_pop_t2", "acc_pop_t3", "acc_pop_t4")

clusters$popdens <- clusters$pop / clusters$area

aa <- accpop

clusters['acc_pop_share_t1'] = accpop['acc_pop_t1'] / (accpop['acc_pop_t1'] + accpop['acc_pop_t2'] + accpop['acc_pop_t3'] + accpop['acc_pop_t4'])
clusters['acc_pop_share_t2'] = accpop['acc_pop_t2'] / (accpop['acc_pop_t1'] + accpop['acc_pop_t2'] + accpop['acc_pop_t3'] + accpop['acc_pop_t4'])
clusters['acc_pop_share_t3'] = accpop['acc_pop_t3'] / (accpop['acc_pop_t1'] + accpop['acc_pop_t2'] + accpop['acc_pop_t3'] + accpop['acc_pop_t4'])
clusters['acc_pop_share_t4'] = accpop['acc_pop_t4'] / (accpop['acc_pop_t1'] + accpop['acc_pop_t2'] + accpop['acc_pop_t3'] + accpop['acc_pop_t4'])

clusters$acc_pop_share_t1[is.nan(clusters$acc_pop_share_t1)]<-0
clusters$acc_pop_share_t2[is.nan(clusters$acc_pop_share_t2)]<-0
clusters$acc_pop_share_t3[is.nan(clusters$acc_pop_share_t3)]<-0
clusters$acc_pop_share_t4[is.nan(clusters$acc_pop_share_t4)]<-0

clusters <- bind_cols(clusters, accpop)

# Spatial join between income quintiles DHS and clusters

dhs <- filter(dhs, ISO=="KE")

clusters <- st_transform(clusters, 3395)
dhs <- st_transform(dhs, 3395)

clusters <- st_join(clusters, dhs, join = nngeo::st_nn, maxdist = 50000, k = 1) 

clusters <- st_transform(clusters, 4326)


clusters$ISO = as.factor("KE")

# aa = clusters %>% dplyr::select('acc_pop_share_t1', 'acc_pop_share_t2', 'acc_pop_share_t3', 'acc_pop_share_t4', 'HCWIXQPLOW', 'HCWIXQP2ND', 'HCWIXQPMID', 'HCWIXQP4TH', 'HCWIXQPHGH', 'popdens', 'isurban', 'ISO') %>% as.data.frame()
# 
# aa$geom=NULL
# aa$geometry=NULL
# 
# # Partition data
# splitSample <- sample(1:2, size=nrow(aa), prob=c(0.8,0.2), replace = TRUE)
# train.hex <- aa[splitSample==1,]
# test.hex <- aa[splitSample==2,]
# 
# pr = rfsrc(Multivar(acc_pop_share_t1, acc_pop_share_t2, acc_pop_share_t3, acc_pop_share_t4)~.,data = train.hex, importance=T)
# 
# print(pr)
# 
# prediction <- predict.rfsrc(pr, test.hex)
# 
# # Calculate the number of people in each tier in each cluster
# 
# clusters_ng <- clusters
# clusters_ng$geometry=NULL
# 
# prediction <- predict.rfsrc(pr, clusters_ng)
# clusters$acc_pop_share_t1_new = prediction$regrOutput$acc_pop_share_t1$predicted
# clusters$acc_pop_share_t2_new = prediction$regrOutput$acc_pop_share_t2$predicted
# clusters$acc_pop_share_t3_new = prediction$regrOutput$acc_pop_share_t3$predicted
# clusters$acc_pop_share_t4_new = prediction$regrOutput$acc_pop_share_t4$predicted
# 
# clusters$acc_pop_t1_new =  clusters$acc_pop_share_t1_new * clusters$noacc
# clusters$acc_pop_t2_new =  clusters$acc_pop_share_t2_new * clusters$noacc
# clusters$acc_pop_t3_new =  clusters$acc_pop_share_t3_new * clusters$noacc
# clusters$acc_pop_t4_new =  clusters$acc_pop_share_t4_new * clusters$noacc

clusters$acc_pop_t1_new =  clusters$acc_pop_share_t1 * clusters$noacc
clusters$acc_pop_t2_new =  clusters$acc_pop_share_t2 * clusters$noacc
clusters$acc_pop_t3_new =  clusters$acc_pop_share_t3 * clusters$noacc
clusters$acc_pop_t4_new =  clusters$acc_pop_share_t4 * clusters$noacc

# Calculate number of households in each cluster
clusters$HHs = ifelse(clusters$isurban>=12, clusters$pop/3.5, clusters$pop/4.5)

for (m in 1:12){
  for (i in 1:24){

    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters = mutate(clusters, !!paste0('PerHHD_' , as.character(m) , "_" , as.character(i)) := ifelse(aa$isurban>=12,  pull(!!as.name(paste0('urb1', "_" , as.character(m))))[i] * aa$acc_pop_t1_new +  pull(!!as.name(paste0('urb2', "_" , as.character(m))))[i] * aa$acc_pop_t2_new +  pull(!!as.name(paste0('urb3', "_" , as.character(m))))[i] * aa$acc_pop_t3_new +  pull(!!as.name(paste0('urb4', "_" , as.character(m))))[i] * aa$acc_pop_t4_new * 0.75 +  pull(!!as.name(paste0('urb5', "_" , as.character(m))))[i] * aa$acc_pop_t4_new * 0.25, ifelse(aa$isurban < 12,  pull(!!as.name(paste0('rur1', "_" , as.character(m))))[i] * aa$acc_pop_t1_new +  pull(!!as.name(paste0('rur2', "_" , as.character(m))))[i] * aa$acc_pop_t2_new +  pull(!!as.name(paste0('rur3', "_" , as.character(m))))[i] * aa$acc_pop_t3_new +  pull(!!as.name(paste0('rur4', "_" , as.character(m))))[i] * aa$acc_pop_t4_new * 0.75 +  pull(!!as.name(paste0('rur5', "_" , as.character(m))))[i] * aa$acc_pop_t4_new * 0.25 , 0)))
  }}

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

idx = which(grepl("PerHHD_", colnames(aa))==TRUE)
clusters$PerHHD_tt = rowSums(aa[idx])

for (m in 1:12){
  
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
    idx = which(grepl(paste0("PerHHD_", as.character(m)), colnames(clusters))==TRUE) 
    clusters[paste0('PerHHD_tt' ,"_monthly_" , as.character(m))] = rowSums(aa[idx])
}

for (m in 1:12){
  for (i in 1:24){
    
    aa <- clusters
    aa$geometry=NULL
    aa$geom=NULL
    
    clusters[paste0('PerHHD_' , as.character(m) , "_" , as.character(i))] = pull(aa[paste0('PerHHD_' , as.character(m) , "_" , as.character(i))]) / pull(aa[paste0('PerHHD_tt' ,"_monthly_" , as.character(m))])
}}