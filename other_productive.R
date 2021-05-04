#Crop processing machinery: energy demand

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

# sum all crops by months
for (z in 1:12){
  aa <- clusters
  aa$geometry=NULL
  aa$geom=NULL
  
  aa <- aa %>% select(starts_with('kwh_cp')) %>% select(ends_with(paste0('_' , as.character(z)))) %>% mutate(a=rowSums(., na.rm = T))
  
  clusters = clusters %>% mutate(!!as.name(paste0('monthly_kwh_cropproc', "_" , as.character(z))) := as.vector(aa$a))
  
}

# simulate daily profile

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


####

# calculate paved road density in each cluster 

ints = st_intersection(roads, clusters)
roadslenght = tapply(st_length(ints), ints$id,sum)
clusters$roadslenght = rep(0,nrow(clusters))
clusters$roadslenght[match(names(roadslenght),clusters$id)] = roadslenght

# calculate travel time to 50 k in each cluster

clusters$traveltime = exact_extract(traveltime, clusters, 'mean')

# calculate employment rate in each cluster
clusters$fid=NULL

clusters2 <- dplyr::select(clusters, id)

result <- qgis_run_algorithm(
  "native:joinbynearest",
  INPUT = clusters2,
  INPUT_2 = empl_wealth,
  NEIGHBORS = 1
)

clusters2 <- sf::read_sf(qgis_output(result, "OUTPUT"))

gdata::keep(clusters, clusters2, gadm0, home_repo_folder, input_folder, processed_folder, spam_folder, sure = T)
save.image(file="bk1_1.Rdata")

# bind...
clusters2$geom<- NULL
clusters2$geometry<- NULL
clusters2 <- clusters2[!duplicated(clusters2[,c('id')]),]
clusters2 <- dplyr::select(clusters2, -id) 
clusters <- dplyr::select(clusters, -starts_with("HCW")) 
clusters2 <- bind_cols(clusters, clusters2)

# run PCA
clusters2$geometry<-NULL
clusters2$geom<-NULL

clusters2$popdens=clusters2$pop/clusters2$area
clusters2$employment = (clusters2$EMEMPLMEMC + clusters2$EMEMPLWEMC)/2

data_pca = dplyr::select(clusters2, HCWIXQPHGH, employment, popdens, traveltime)
data_pca$geometry=NULL
data_pca$geom=NULL

data_pca[] <- lapply(data_pca, function(x) { 
x[is.na(x)] <- mean(x, na.rm = TRUE)
x
})

data_pca <- lapply(data_pca, function(x) round((x-min(x, na.rm=T))/(max(x, na.rm=T)-min(x, na.rm=T)), 2)) %>% bind_cols()

data_pca_bk <- data_pca

data_pca <- prcomp(data_pca)

PCs <- as.data.frame(data_pca$x)
PCs$PCav <- PCs$PC1

# rescale PCA to 0.3  - 0.6 range

PCs$PCav <- rescale(PCs$PCav, to = c(0.6, 0.3))

# hist of variables

hist <- data.frame(data_pca_bk, PCs$PCav)

hist$PCs.PCav <- rescale(hist$PCs.PCav, to = c(0, 1))

colnames(hist) <- c("Highest wealth share", "Employment rate", "Population density", "City accessibility", "PCA")

hist <- tidyr::gather(hist, key="var", value="value", 1:5)

# a <- ggplot(hist)+
#   geom_histogram(aes(x=value, fill=var), colour="black", lwd=0.01, binwidth = 0.1)+
#   facet_wrap(vars(var))+
#   xlab("Normalised values")+
#   ylab("Count")+
#   theme(legend.position = "none")
# 
# ggsave("pca.png", a, device = "png")
# 

clusters_prod <- cbind(clusters, PCs$PCav)

#ggplot(clusters)+
#geom_clusters(aes(fill=PCs.PCav))

# import load monthly curves of residential

clusters_residential = dplyr::select(clusters_prod, id, starts_with("PerHHD_")) %>% as.data.frame()
clusters_residential$geometry= NULL
clusters_residential$geom= NULL
clusters_residential$PerHHD_tt = NULL

clusters_residential$PerHHD_tt_monthly_1 = as.numeric(clusters_residential$PerHHD_tt_monthly_1) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_2 = as.numeric(clusters_residential$PerHHD_tt_monthly_2) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_3 = as.numeric(clusters_residential$PerHHD_tt_monthly_3) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_4 = as.numeric(clusters_residential$PerHHD_tt_monthly_4) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_5 = as.numeric(clusters_residential$PerHHD_tt_monthly_5) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_6 = as.numeric(clusters_residential$PerHHD_tt_monthly_6) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_7 = as.numeric(clusters_residential$PerHHD_tt_monthly_7) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_8 = as.numeric(clusters_residential$PerHHD_tt_monthly_8) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_9 = as.numeric(clusters_residential$PerHHD_tt_monthly_9) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_10 = as.numeric(clusters_residential$PerHHD_tt_monthly_10) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_11 = as.numeric(clusters_residential$PerHHD_tt_monthly_11) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
clusters_residential$PerHHD_tt_monthly_12 = as.numeric(clusters_residential$PerHHD_tt_monthly_12) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)

clusters_residential_tt = tidyr::gather(clusters_residential %>% dplyr::select(290:301, 1), "date_tt", "value_tt", 1:12)

clusters_residential_tt$month = as.numeric((sub('.*\\_', "", gsub("PerHHD_tt_monthly_", "", clusters_residential_tt$date_tt))))

clusters_residential = tidyr::gather(clusters_residential %>% dplyr::select(2:289, 1), "date", "value", 1:288)
clusters_residential$hour = as.numeric((sub('.*\\_', "", gsub("PerHHD_", "", clusters_residential$date))))
clusters_residential$month = as.numeric((sub('\\_.*', "", gsub("PerHHD_", "", clusters_residential$date))))

clusters_residential <- as.data.table(clusters_residential)
clusters_residential_tt <- as.data.table(clusters_residential_tt)

clusters_residential = merge(clusters_residential,clusters_residential_tt, by=c("id", "month"))

clusters_residential$value = as.numeric(clusters_residential$value_tt)*as.numeric(clusters_residential$value)

clusters_residential = dplyr::select(clusters_residential, hour, value, month) %>% group_by(hour, month) %>% dplyr::summarise(value=sum(value, na.rm=T)) %>% ungroup()

clusters_residential$hour = as.numeric(clusters_residential$hour)

# calculate monthly markup at each hour, i.e. ratio with mean

clusters_residential_2 = group_by(clusters_residential, hour) %>% mutate(media = mean(value, na.rm=T)) %>% ungroup() %>% group_by(month) %>% mutate(value = value/media)

# use calculated ratios to rescale load curve of productive activities for each monthly

load_curve_prod_act <- merge(clusters_residential_2, load_curve_prod_act,  by.x="hour", by.y="ï..Hour", all.x=T)

load_curve_prod_act$load_curve <- load_curve_prod_act$value * load_curve_prod_act$Share

# multiply daily total residential consumption of each month by the monthly load curves for productive

for (m in c(1:12)){
for (h in c(1:24)){

  clusters_prod <- mutate(clusters_prod, !!paste0("residual_productive_", m, "_", h) := as.numeric(load_curve_prod_act$load_curve[load_curve_prod_act$hour == h & load_curve_prod_act$month == m]))
}}

for (m in c(1:12)){

  a<-dplyr::select(clusters_prod, starts_with("PerHHD_tt_monthly"))[,m] %>% as.data.frame() %>% mutate(geometry=NULL, geom=NULL) %>% mutate_all(., .funs = as.numeric) *  clusters_prod$PCs.PCav

clusters_prod <- mutate(clusters_prod, !!paste0("residual_productive_tt_", m) := a[,1])
}

clusters <- clusters_prod

gdata::keep(clusters, gadm0, sure = T)
source("manual_parameters.R", echo = F)