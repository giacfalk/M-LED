# Cropland and irrigation water requirements

# cont_1 <- function(X, na.rm = na.rm){
#   ifelse((1 %in% X), 1, NA)
# }
# 
# cropland_extent <- raster::aggregate(cropland_extent, fact=33.33, fun=cont_1)

# cropland_extent <- projectRaster(cropland_extent, crs="+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs")
# clusters <- st_transform(clusters, 3395)

# Cropland in each cluster in hectares
clusters$cr_ha_count <- exactextractr::exact_extract(cropland_extent, clusters, fun="count")
clusters$cr_ha_count <- clusters$cr_ha_count * 900 * 0.0001

cr_ha_count_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=cr_ha_count))+
  scale_fill_viridis_c(trans="log", name="Cropland (ha)")

# Area of each cluster
clusters$area <- as.vector(st_area(clusters)) * 0.0001

# Share of cropland over total cluster area
clusters$crshare <- clusters$cr_ha_count / clusters$area

crshare_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=crshare))+
  scale_fill_viridis_c(trans="log")

#clusters <- st_transform(clusters, 4326)

# downscale SPAM rasters
ID_raster <- raster()
nrow(ID_raster) <- 2160
ncol(ID_raster) <- 4320
res(ID_raster) <- 0.083333
extent(ID_raster) <- ext  
values(ID_raster) <- 1:(2160*4320)
crs(ID_raster) <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

clusters$id_pix_ras_majority <- exactextractr::exact_extract(ID_raster, clusters, fun="majority")

clusters$id <- 1:nrow(clusters)

clusters <- group_by(clusters, id_pix_ras_majority) %>% mutate(total_crarea_underneath=sum(cr_ha_count, na.rm=T)) %>% ungroup()
clusters$crshare_sp =  clusters$cr_ha_count / clusters$total_crarea_underneath
clusters$crshare = ifelse(is.na(clusters$crshare_sp), 0, clusters$crshare_sp)

files = list.files(path = paste0(spam_folder, "spam2010v1r0_global_harv_area.geotiff") , pattern = 'r.tif')

for (X in files){
  a = paste0("A_" , as.character(substr(X, 36, 39)))
  clusters[a] <- exactextractr::exact_extract(raster(paste0(spam_folder, "spam2010v1r0_global_harv_area.geotiff/", X)), clusters, fun="sum")
  clusters <- clusters %>%  mutate(!!a := (!!as.name(a)) * crshare_sp) 
}

whea_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=A_whea))+
  scale_fill_viridis_c(trans="log")

whea_share_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=A_whea/cr_ha_count))+
  scale_fill_viridis_c(trans="log")

# Irrigation water requirements

clusters$clima_zone <- exactextractr::exact_extract(climatezones, clusters, fun="majority")

clima_zone_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=as.factor(clima_zone)))+
  scale_fill_discrete(name="Agro-ecological zone")

# List of months in the year
list_months = c("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")

# Import PET and extract monthly mean within each cluster
pet <- exactextractr::exact_extract(pet, clusters, fun="mean")

colnames(pet) <- gsub('.{3}$', '',paste0("PET_", gsub("mean.X2015.", "", colnames(pet))))

ppt <- exactextractr::exact_extract(ppt, clusters, fun="mean")

colnames(ppt) <- gsub("PET", "PPT", colnames(pet))

# soil <- exactextractr::exact_extract(soil, clusters, fun="mean")
# colnames(soil) <- gsub("PET", "MOI", colnames(pet))

clusters <- bind_cols(clusters, pet, ppt)

pet_plot <- ggplot(data=clusters %>% dplyr::select(starts_with("PET")) %>% gather(., key="key", value="value", 1:12))+
  geom_sf(aes(fill=value))+
  scale_fill_viridis_c(trans="log")+
  facet_wrap(vars(key))

ppt_plot <- ggplot(data=clusters %>% dplyr::select(starts_with("PPT")) %>% gather(., key="key", value="value", 1:12))+
  geom_sf(aes(fill=value))+
  scale_fill_viridis_c(trans="log", name="Monthly mean ppt")+
  facet_wrap(vars(key))

# Define crop factor for each day of the year based on sum of beginning of growing seasons and length of each growing period
for (i in 1:nrow(crops)){
print(crops$crop[i])
daily=data.frame("daily" = c(1:729))
daily$date = seq(as.Date("2019-01-01"), length.out = 729, by = "days")
daily$month = lubridate::month(daily$date)
daily$day = lubridate::day(daily$date)

pm1= as.Date(paste0(crops[i, 'pm_1'], "2019"), format= "%d%m%Y")
pm2= as.Date(paste0(crops[i, 'pm_2'], "2019"), format= "%d%m%Y")

# crop factor in each day of the year for growing period 1
daily['k_c'] = ifelse((daily$date>= pm1) & (daily$date < (pm1 + as.numeric(crops[i, 'nd_1']))), as.numeric(crops[i, 'cf_1']),ifelse((daily$date>= pm1 + as.numeric(crops[i, 'nd_1'])) & (daily$date < (pm1 + as.numeric(crops[i, 'nd_1']) + as.numeric(crops[i, 'nd_2']))), as.numeric((crops[i, 'cf_1'] + crops[i, 'cf_2'])/2), ifelse((daily$date>= pm1) & (daily$date < (pm1 + as.numeric(crops[i, 'nd_1']) + as.numeric(crops[i, 'nd_2']) + as.numeric(crops[i, 'nd_3']))), as.numeric((crops[i, 'cf_2'] + crops[i, 'cf_3'])/2), ifelse((daily$date>= pm1) & (daily$date < (pm1 + as.numeric(crops[i, 'nd_1']) + as.numeric(crops[i, 'nd_2']) + as.numeric(crops[i, 'nd_3'])+ as.numeric(crops[i, 'nd_4']))), as.numeric(crops[i, 'cf_3']), 0)))) 

# crop factor in each day of the year for growing period 2
daily['k_c2'] = ifelse((daily$date>= pm2) & (daily$date < (pm2 + as.numeric(crops[i, 'nd_1']))), as.numeric(crops[i, 'cf_1']),ifelse((daily$date>= pm2 + as.numeric(crops[i, 'nd_1'])) & (daily$date < (pm2 + as.numeric(crops[i, 'nd_1']) + as.numeric(crops[i, 'nd_2']))), as.numeric((crops[i, 'cf_1'] + crops[i, 'cf_2'])/2), ifelse((daily$date>= pm2) & (daily$date < (pm2 + as.numeric(crops[i, 'nd_1']) + as.numeric(crops[i, 'nd_2']) + as.numeric(crops[i, 'nd_3']))), as.numeric((crops[i, 'cf_2'] + crops[i, 'cf_3'])/2), ifelse((daily$date>= pm2) & (daily$date < (pm2 + as.numeric(crops[i, 'nd_1']) + as.numeric(crops[i, 'nd_2']) + as.numeric(crops[i, 'nd_3'])+ as.numeric(crops[i, 'nd_4']))), as.numeric(crops[i, 'cf_3']), 0)))) 

# crop factor in each day of the year for both growing periods
daily <- daily %>% mutate(k_c = pmax(k_c, k_c2), na.rm = T)
daily = daily %>% group_by(month, day) %>% summarise(k_c = max(k_c))

# daily potential evapotransperation
daily$date = seq(as.Date("2019-01-01"), length.out = 366, by = "days")

for (k in 1:365){

aa <- clusters[paste0('PET_' , as.character(ifelse(nchar(daily$month[k]==1), paste0("0", as.character(daily$month)), as.character(daily$month[k]))))]/30

aa$geometry=NULL
aa$geom=NULL

clusters[paste0("ET_",  as.character(crops[i,1]), "_" , as.character(daily[k,1]), "_" , as.character(daily[k,2]))] = daily$k_c[k] * aa

}}

# Summarise ETc by month by crop
for (i in 1:nrow(crops)){ 
  for (z in 1:12){  
    
aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters[paste0('monthly_ET_' , as.character(crops[i,1]) , "_" , as.character(z))] = as.vector(aa %>%  dplyr::select(starts_with(paste0('ET_' , as.character(crops[i,1]) , "_" , as.character(z) , '_')))) %>% rowSums(na.rm = T) %>% as.numeric()
  
aa <- clusters
aa$geometry=NULL
aa$geom=NULL

#Convert ET to total m3 per cluster per month per crop
clusters[paste0('monthly_ET_' , as.character(crops[i,1]) , "_" , as.character(z))] = as.vector(aa[paste0("A_" , as.character(crops[i,1]))] * aa[paste0('monthly_ET_' , as.character(crops[i,1]) , "_" , as.character(z))]* 10)

# Absorption efficiency (share of water that roots are able to extract from soil)
eta = 0.6

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

#Convert PPT to total m3 per cluster per month per crop 
clusters[paste0('monthly_PPT_' , as.character(crops[i,1]) , "_" , as.character(z))] = as.vector(aa[paste0('PPT_' , as.character(ifelse(nchar(as.character(z)) == 1, paste0("0" , as.character(z)), as.character(z))))] * eta * 10 * aa[paste0("A_" , as.character(crops[i,1]))])

#Calculate irrigation requirement per cluster per month per crop in m3 considering different irrigation efficiency per each crop 

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters[paste0('monthly_IRREQ_' , as.character(crops[i,1]) , "_" , as.character(z))] = (aa[paste0('monthly_ET_' , as.character(crops[i,1]) , "_" , as.character(z))] - aa[paste0('monthly_PPT_' , as.character(crops[i,1]) , "_" , as.character(z))]) / as.numeric(crops['eta_irr'][i,])

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters[paste0('monthly_IRREQ_' , as.character(crops[i,1]) , "_" , as.character(z))] = ifelse(aa[paste0('monthly_IRREQ_' , as.character(crops[i,1]) , "_" , as.character(z))]<0, 0, pull(aa[paste0('monthly_IRREQ_' , as.character(crops[i,1]) , "_" , as.character(z))]))
}}
  
# Obtain total yearly WG per cluster (in m3)

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

clusters['IRREQ_year'] =  as.numeric(aa %>%  dplyr::select(starts_with("monthly_IRREQ_")) %>% rowSums(na.rm = T))

aa <- clusters
aa$geometry=NULL
aa$geom=NULL

for (z in 1:12){  
  a = aa %>%  dplyr::select(starts_with("monthly_IRREQ_"))
a2 = a %>%  dplyr::select(ends_with(paste0("_", as.character(z))))
clusters[paste0('monthly_IRREQ' , "_" , as.character(z))] = as.numeric(rowSums(a2, na.rm = T))
}

monthly_irreq_plot <- ggplot(data=clusters %>% dplyr::select(starts_with("monthly_IRREQ_")) %>% gather(., key="key", value="value", 1:12))+
  geom_sf(aes(fill=value))+
  scale_fill_viridis_c(trans="log", name="Monthly irrig. wat. req. (m3)")+
  facet_wrap(vars(key))

monthly_irreq_dens_plot <- ggplot(data=clusters %>% dplyr::select(starts_with("monthly_IRREQ_")) %>% gather(., key="key", value="value", 1:12) %>% mutate(value=value/clusters$cr_ha_count))+
  geom_sf(aes(fill=value))+
  scale_fill_viridis_c(trans="log", name="Monthly irrig. wat. req. (m3/ha)")+
  facet_wrap(vars(key))
