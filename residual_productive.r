## residual productive demand
library(sf)
library(tidyverse)
library(raster)
library(rgeos)
sf <- read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_16.gpkg') 

a <- read.csv("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_8.csv") %>% dplyr::select(starts_with("kwh_cropproc_tt"), id)

b<- read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_16.csv')

a$X=NULL
b$X=NULL

sf = merge(sf, a, by="id")
sf = merge(sf, b, by="id")

# calculate paved road density in each cluster 
roads<-read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/onsset/input/Roads/RoadsKEN.shp')

ints = st_intersection(roads, sf)
roadslenght = tapply(st_length(ints), ints$id,sum)
sf$roadslenght = rep(0,nrow(sf))
sf$roadslenght[match(names(roadslenght),sf$id)] = roadslenght

# calculate travel time to 50 k in each cluster
traveltime <- raster('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/input_folder/travel.tif')

library(exactextractr)

sf$traveltime = exact_extract(traveltime, sf, 'mean')

# calculate employment rate in each cluster
empl_wealth<-read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/jrc/wealth_employment/shps/sdr_subnational_data_dhs_2014.shp')

sf2 = st_join(sf, empl_wealth, join = st_nn, largest=T, left=T)

# run PCA
library(FactoMineR)
library(factoextra)

sf2$popdens=sf2$popsum/sf2$Area
sf2$employment = (sf2$EMEMPLMEMC + sf2$EMEMPLWEMC)/2

data_pca = dplyr::select(sf2, HCWIXQPHGH.y, employment, popdens, traveltime)
data_pca$geometry=NULL

data_pca[] <- lapply(data_pca, function(x) { 
  x[is.na(x)] <- mean(x, na.rm = TRUE)
  x
})

data_pca <- lapply(data_pca, function(x) round((x-min(x))/(max(x)-min(x)), 2)) %>% bind_cols()

data_pca_bk <- data_pca

data_pca <- prcomp(data_pca)

PCs <- as.data.frame(data_pca$x)
PCs$PCav <- PCs$PC1

# rescale PCA to 0.3  - 0.6 range

library(scales)
PCs$PCav <- rescale(PCs$PCav, to = c(0.6, 0.3))

# hist of variables

hist <- data.frame(data_pca_bk, PCs$PCav)

hist$PCs.PCav <- rescale(hist$PCs.PCav, to = c(0, 1))

colnames(hist) <- c("Highest wealth share", "Employment rate", "Population density", "City accessibility", "PCA")

hist <- tidyr::gather(hist, key="var", value="value", 1:5)

a <- ggplot(hist)+
  geom_histogram(aes(x=value, fill=var), colour="black", lwd=0.01, binwidth = 0.1)+
  facet_wrap(vars(var))+
  xlab("Normalised values")+
  ylab("Count")+
  theme(legend.position = "none")

ggsave("pca.png", a, device = "png")

                  
sf_prod <- cbind(sf, PCs$PCav)

library(ggplot2)
#ggplot(sf)+
  #geom_sf(aes(fill=PCs.PCav))


# import load curve of productive activities

load_curve_prod_act <- read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/input_folder/productive profile.csv')

# import load monthly curves of residential

sf_residential = dplyr::select(sf_prod, id, starts_with("PerHHD_")) %>% as.data.frame()
sf_residential$geometry = NULL
sf_residential$PerHHD_tt = NULL

sf_residential$PerHHD_tt_monthly_1 = as.numeric(sf_residential$PerHHD_tt_monthly_1) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_2 = as.numeric(sf_residential$PerHHD_tt_monthly_2) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_3 = as.numeric(sf_residential$PerHHD_tt_monthly_3) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_4 = as.numeric(sf_residential$PerHHD_tt_monthly_4) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_5 = as.numeric(sf_residential$PerHHD_tt_monthly_5) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_6 = as.numeric(sf_residential$PerHHD_tt_monthly_6) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_7 = as.numeric(sf_residential$PerHHD_tt_monthly_7) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_8 = as.numeric(sf_residential$PerHHD_tt_monthly_8) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_9 = as.numeric(sf_residential$PerHHD_tt_monthly_9) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_10 = as.numeric(sf_residential$PerHHD_tt_monthly_10) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_11 = as.numeric(sf_residential$PerHHD_tt_monthly_11) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residential$PerHHD_tt_monthly_12 = as.numeric(sf_residential$PerHHD_tt_monthly_12) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)

sf_residential_tt = tidyr::gather(sf_residential %>% dplyr::select(290:301, 1), "date_tt", "value_tt", 1:12)

sf_residential_tt$month = as.numeric((sub('.*\\_', "", gsub("PerHHD_tt_monthly_", "", sf_residential_tt$date_tt))))

sf_residential = tidyr::gather(sf_residential %>% dplyr::select(2:289, 1), "date", "value", 1:288)
sf_residential$hour = as.numeric((sub('.*\\_', "", gsub("PerHHD_", "", sf_residential$date))))
sf_residential$month = as.numeric((sub('\\_.*', "", gsub("PerHHD_", "", sf_residential$date))))

sf_residential = merge(sf_residential,sf_residential_tt, by=c("id", "month"))

sf_residential$value = as.numeric(sf_residential$value_tt)*as.numeric(sf_residential$value)

sf_residential = dplyr::select(sf_residential, hour, value, month) %>% group_by(hour, month) %>% dplyr::summarise(value=sum(value, na.rm=T)) %>% ungroup()

sf_residential$hour = as.numeric(sf_residential$hour)

# calculate monthly markup at each hour, i.e. ratio with mean

sf_residential_2 = group_by(sf_residential, hour) %>% mutate(media = mean(value, na.rm=T)) %>% ungroup() %>% group_by(month) %>% mutate(value = value/media)

# use calculated ratios to rescale load curve of productive activities for each monthly

load_curve_prod_act <- merge(sf_residential_2, load_curve_prod_act,  by.y="ï..Hour", by.x="hour", all.x=T)
  
load_curve_prod_act$load_curve <- load_curve_prod_act$value * load_curve_prod_act$Share

# multiply daily total residential consumption of each month by the monthly load curves for productive

for (m in c(1:12)){
  for (h in c(0:23)){
    sf_prod <- mutate(sf_prod, !!paste0("residual_productive_", m, "_", h) := as.numeric(load_curve_prod_act$load_curve[load_curve_prod_act$hour == h & load_curve_prod_act$month == m]))
  }}

for (m in c(1:12)){
  a<-dplyr::select(sf_prod, starts_with("PerHHD_tt_monthly"))[,m] %>% as.data.frame() %>% mutate(geometry=NULL) %>% mutate_all(., .funs = as.numeric) *  sf_prod$PCs.PCav
  sf_prod <- mutate(sf_prod, !!paste0("residual_productive_tt_", m) := a[,1])
  }

sf <- sf_prod

###

