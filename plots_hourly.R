library(sf)
library(cowplot)
library(raster)
library(ggplot2)
library(scales)
library(tidyr)
library(tidyverse)
library(sf)

setwd('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/results_figures')

geogeo <- sf$geometry

sf$geometry=NULL
#sf$geom=NULL

### Irrigation ###
sf_irrig = dplyr::select(sf,starts_with("er_kwh_tt"))
  
sf_irrig$id = 1:nrow(sf)

sf_irrig = tidyr::gather(sf_irrig, "month_tt", "value_tt", 1:12)

sf_irrig$month_tt = as.numeric(gsub("er_kwh_tt", "", sf_irrig$month_tt))

sf_irrig$value_tt = as.numeric(sf_irrig$value_tt)

load_curve_irrig = c(0, 0, 0, 0, 0, 0.166, 0.166, 0.166, 0.166, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.166, 0.166)

for (i in c(0:23)){
  sf_irrig = mutate(sf_irrig, !!paste0("value", i) := load_curve_irrig[i+1]*value_tt)
}

sf_irrig = tidyr::gather(sf_irrig, "hour", "value", 4:27)

sf_irrig$value=as.numeric(sf_irrig$value)

sf_irrig$hour = as.numeric(gsub("value", "", sf_irrig$hour ))

###

sf_irrig = dplyr::select(sf_irrig, hour, value ,month_tt) %>% group_by(hour, month_tt) %>% summarise(value_irrigation=sum(value, na.rm=T)) %>% ungroup()

sf_irrig$hour = as.numeric(sf_irrig$hour)
sf_irrig$month_tt = as.numeric(sf_irrig$month_tt)

irrigation <- ggplot(sf_irrig, aes(x=as.numeric(hour), y=value_irrigation/1000, group=as.factor(month_tt), colour=as.factor(month_tt)))+
  geom_line(aes(group=as.factor(month_tt), colour=as.factor(month_tt)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed")+
  ggtitle("Irrigation")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

### Crop processing ###
sf_croppro = dplyr::select(sf,starts_with("kwh_cropproc_tt"))

sf_croppro$id = 1:nrow(sf)

sf_croppro = tidyr::gather(sf_croppro, "month_tt", "value_tt", 1:12)

sf_croppro$month_tt = as.numeric(gsub("kwh_cropproc_tt_", "", sf_croppro$month_tt))

sf_croppro$value_tt = as.numeric(sf_croppro$value_tt)

load_curve_cp = c(0, 0, 0, 0, 0, 0, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0, 0, 0, 0, 0, 0)

for (i in c(0:23)){
  sf_croppro = mutate(sf_croppro, !!paste0("value", i) := load_curve_cp[i+1]*value_tt)
}

sf_croppro = tidyr::gather(sf_croppro, "hour", "value", 4:27)

sf_croppro$value=as.numeric(sf_croppro$value)

sf_croppro$hour = as.numeric(gsub("value", "", sf_croppro$hour ))

###

sf_croppro = dplyr::select(sf_croppro, hour, value ,month_tt) %>% group_by(hour, month_tt) %>% summarise(value_cropproation=sum(value, na.rm=T)) %>% ungroup()

sf_croppro$hour = as.numeric(sf_croppro$hour)
sf_croppro$month_tt = as.numeric(sf_croppro$month_tt)

crop_pro <- ggplot(sf_croppro, aes(x=as.numeric(hour), y=value_cropproation/1000, group=as.factor(month_tt), colour=as.factor(month_tt)))+
  geom_line(aes(group=as.factor(month_tt), colour=as.factor(month_tt)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed")+
  ggtitle("Crop processing")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

## Health ##
sf_health = dplyr::select(sf, id, starts_with("er_hc_"))
sf_health$er_hc_tt = NULL

sf_health$er_hc_tt_monthly_1 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_1 )
sf_health$er_hc_tt_monthly_2 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_2 )
sf_health$er_hc_tt_monthly_3 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_3 )
sf_health$er_hc_tt_monthly_4 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_4 )
sf_health$er_hc_tt_monthly_5 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_5 )
sf_health$er_hc_tt_monthly_6 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_6 )
sf_health$er_hc_tt_monthly_7 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_7 )
sf_health$er_hc_tt_monthly_8 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_8 )
sf_health$er_hc_tt_monthly_9 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_9 )
sf_health$er_hc_tt_monthly_10 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_10 )
sf_health$er_hc_tt_monthly_11 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_11 )
sf_health$er_hc_tt_monthly_12 = ifelse(sf$elrate>0.75, 0, sf_health$er_hc_tt_monthly_12 )

sf_health_tt = tidyr::gather(sf_health %>% dplyr::select(290:301, 1), "date_tt", "value_tt", 1:12)
sf_health_tt$month = as.numeric((sub('.*\\_', "", gsub("er_hc_tt_monthly_", "", sf_health_tt$date_tt))))

sf_health = tidyr::gather(sf_health %>% dplyr::select(2:289, 1), "date", "value", 1:288)
sf_health$hour = as.numeric((sub('.*\\_', "", gsub("er_hc_", "", sf_health$date))))
sf_health$month = as.numeric((sub('\\_.*', "", gsub("er_hc_", "", sf_health$date))))


sf_health = merge(sf_health,sf_health_tt, by=c("id", "month"))

sf_health$value = as.numeric(sf_health$value_tt)*as.numeric(sf_health$value)

sf_health = dplyr::select(sf_health, hour, value, month) %>% group_by(hour, month) %>% summarise(value=sum(value, na.rm=T)) %>% ungroup()

sf_health$hour = as.numeric(sf_health$hour)


health<-ggplot(sf_health, aes(x=as.numeric(hour), y=value/1000))+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed")+
  ggtitle("Healthcare")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

## Edu ##
sf_edu = dplyr::select(sf, id, starts_with("er_sch_"))
sf_edu$er_sch_tt = NULL

sf_edu$er_sch_tt_monthly_1 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_1 )
sf_edu$er_sch_tt_monthly_2 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_2 )
sf_edu$er_sch_tt_monthly_3 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_3 )
sf_edu$er_sch_tt_monthly_4 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_4 )
sf_edu$er_sch_tt_monthly_5 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_5 )
sf_edu$er_sch_tt_monthly_6 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_6 )
sf_edu$er_sch_tt_monthly_7 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_7 )
sf_edu$er_sch_tt_monthly_8 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_8 )
sf_edu$er_sch_tt_monthly_9 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_9 )
sf_edu$er_sch_tt_monthly_10 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_10 )
sf_edu$er_sch_tt_monthly_11 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_11 )
sf_edu$er_sch_tt_monthly_12 = ifelse(sf$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_12 )

sf_edu_tt = tidyr::gather(sf_edu %>% dplyr::select(290:301, 1), "date_tt", "value_tt", 1:12)
sf_edu_tt$month = as.numeric((sub('.*\\_', "", gsub("er_sch_tt_monthly_", "", sf_edu_tt$date_tt))))

sf_edu = tidyr::gather(sf_edu %>% dplyr::select(2:289, 1), "date", "value", 1:288)
sf_edu$hour = as.numeric((sub('.*\\_', "", gsub("er_sch_", "", sf_edu$date))))
sf_edu$month = as.numeric((sub('\\_.*', "", gsub("er_sch_", "", sf_edu$date))))


sf_edu = merge(sf_edu,sf_edu_tt, by=c("id", "month"))

sf_edu$value = as.numeric(sf_edu$value_tt)*as.numeric(sf_edu$value)

sf_edu = dplyr::select(sf_edu, hour, value, month) %>% group_by(hour, month) %>% summarise(value=sum(value, na.rm=T)) %>% ungroup()

sf_edu$hour = as.numeric(sf_edu$hour)

edu<-ggplot(sf_edu, aes(x=as.numeric(hour), y=value/1000))+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed")+
  ggtitle("Education")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

## Residential

sf_residential = dplyr::select(sf, id, starts_with("PerHHD_")) %>% as.data.frame()
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

sf_residential = dplyr::select(sf_residential, hour, value, month) %>% group_by(hour, month) %>% summarise(value=sum(value, na.rm=T)) %>% ungroup()

sf_residential$hour = as.numeric(sf_residential$hour)

residential <-ggplot(sf_residential, aes(x=as.numeric(hour), y=value/1000))+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed")+
  ggtitle("Residential")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

######
# residual productive
## residual_productive

sf_residual_productive = dplyr::select(sf, id, starts_with("residual_productive_")) %>% as.data.frame()

sf_residual_productive$residual_productive_tt_1 = as.numeric(sf_residual_productive$residual_productive_tt_1) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_2 = as.numeric(sf_residual_productive$residual_productive_tt_2) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_3 = as.numeric(sf_residual_productive$residual_productive_tt_3) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_4 = as.numeric(sf_residual_productive$residual_productive_tt_4) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_5 = as.numeric(sf_residual_productive$residual_productive_tt_5) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_6 = as.numeric(sf_residual_productive$residual_productive_tt_6) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_7 = as.numeric(sf_residual_productive$residual_productive_tt_7) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_8 = as.numeric(sf_residual_productive$residual_productive_tt_8) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_9 = as.numeric(sf_residual_productive$residual_productive_tt_9) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_10 = as.numeric(sf_residual_productive$residual_productive_tt_10) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_11 = as.numeric(sf_residual_productive$residual_productive_tt_11) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)
sf_residual_productive$residual_productive_tt_12 = as.numeric(sf_residual_productive$residual_productive_tt_12) * as.numeric(sf$HHs) * (sf$noaccsum/sf$popsum)

sf_residual_productive_tt = tidyr::gather(sf_residual_productive %>% dplyr::select(290:301, 1), "date_tt", "value_tt", 1:12)

sf_residual_productive_tt$month = as.numeric((sub('.*\\_', "", gsub("residual_productive_tt_", "", sf_residual_productive_tt$date_tt))))

sf_residual_productive = tidyr::gather(sf_residual_productive %>% dplyr::select(2:289, 1), "date", "value", 1:288)
sf_residual_productive$hour = as.numeric((sub('.*\\_', "", gsub("residual_productive_", "", sf_residual_productive$date))))
sf_residual_productive$month = as.numeric((sub('\\_.*', "", gsub("residual_productive_", "", sf_residual_productive$date))))

sf_residual_productive = merge(sf_residual_productive,sf_residual_productive_tt, by=c("id", "month"))

sf_residual_productive$value = as.numeric(sf_residual_productive$value_tt)*as.numeric(sf_residual_productive$value)

sf_residual_productive = dplyr::select(sf_residual_productive, hour, value, month) %>% group_by(hour, month) %>% summarise(value=sum(value, na.rm=T)) %>% ungroup()

sf_residual_productive$hour = as.numeric(sf_residual_productive$hour)

residual_productive <-ggplot(sf_residual_productive, aes(x=as.numeric(hour), y=value/1000))+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed")+
  ggtitle("Commercial & prod.")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

#####

### okay, just fix magnitude of commercial (somehow wrong multiplication)
all_sectors <- cowplot::plot_grid(residential + theme(legend.position = "none"), edu + theme(legend.position = "none"), health + theme(legend.position = "none"), irrigation + theme(legend.position = "none"), crop_pro + theme(legend.position = "none"), residual_productive + theme(legend.position = "none"))


all_sectors <- cowplot::plot_grid(all_sectors, get_legend(crop_pro), ncol = 1, rel_heights = c(1, 0.15))

ggsave("all.png", all_sectors, device = "png", scale=1.7)

Residential<-sum(residential$data$value)*30
Education<-sum(edu$data$value)*30
Healthcare<-sum(health$data$value)*30
Irrigation<-sum(irrigation$data$value_irrigation)*30
Crop_processing<-sum(crop_pro$data$value_cropproation)*30
Comm_prod <- sum(residual_productive$data$value)*30

print("Latent demand (estimated) TWh")
sum(Residential, Education, Healthcare, Irrigation, Crop_processing, Comm_prod)/1000000000  

print("Total power demand: 7.86 TWh")

sum(Residential, Education, Healthcare, Irrigation, Crop_processing, Comm_prod)/1000000000/7.86

df <- as.data.frame(rbind(Residential, Education, Healthcare, Irrigation, Crop_processing, Comm_prod))
df$sector<-rownames(df)

barplot <- ggplot(df, aes(x=sector, y=V1/1000000000))+
  geom_col(aes(fill=sector))+
  scale_y_continuous(name="Yearly unmet electricity demand (TWh)")+
  xlab("Sector")+
  scale_fill_discrete(name="Sector")+
  theme(legend.position = "bottom", legend.direction = "horizontal")
  

ggsave("barplot_sectors.png", barplot, device = "png", scale=1, width = 7, height = 5)

############

fmt_dcimals <- function(decimals=0){
  # return a function responpsible for formatting the 
  # axis labels with a given number of decimals 
  function(x) as.character(round(x,decimals))
}

sf$geometry <- geogeo

sf <- st_as_sf(sf)

sf$residential_demand <- cut((as.numeric(sf$PerHHD_tt) * (as.numeric(sf$noaccsum) / as.numeric(sf$popsum)) * as.numeric(sf$HHs))/1000, breaks = c(-Inf, 1, 5, 15, 30, 50, Inf), 
                       labels = c("<1", "1-5", "5-15", "15-30", "30-50", ">50"), right = FALSE)

library(viridis)
a<- ggplot(sf)+
  geom_sf(aes(fill=residential_demand), color = NA)+
  ggtitle("Residential")+
  scale_fill_viridis(name="MWh", discrete = T)+
  theme(legend.position = "none")

sf = mutate(sf, er_kwh_tt = as.numeric(er_kwh_tt1) + as.numeric(er_kwh_tt2) + as.numeric(er_kwh_tt3) + as.numeric(er_kwh_tt4) + as.numeric(er_kwh_tt5) + as.numeric(er_kwh_tt6) + as.numeric(er_kwh_tt7) + as.numeric(er_kwh_tt8) + as.numeric(er_kwh_tt9) + as.numeric(er_kwh_tt10) + as.numeric(er_kwh_tt11) + as.numeric(er_kwh_tt12))

sf$irrigation_demand <- cut(as.numeric(sf$er_kwh_tt)/1000, breaks = c(-Inf, 1, 5, 15, 30, 50, Inf), labels = c("<1", "1-5", "5-15", "15-30", "30-50", ">50"), right = FALSE)

b<- ggplot(sf)+
  geom_sf(aes(fill=irrigation_demand), color = NA)+
  ggtitle("Irrigation water pumping")+
  scale_fill_viridis(name="MWh", discrete = T)+
  theme(legend.position = "none")



sf = mutate(sf, kwh_cropproc_tt_ = as.numeric(kwh_cropproc_tt_1) + as.numeric(kwh_cropproc_tt_2) + as.numeric(kwh_cropproc_tt_3) + as.numeric(kwh_cropproc_tt_4) + as.numeric(kwh_cropproc_tt_5) + as.numeric(kwh_cropproc_tt_6) + as.numeric(kwh_cropproc_tt_7) + as.numeric(kwh_cropproc_tt_8) + as.numeric(kwh_cropproc_tt_9) + as.numeric(kwh_cropproc_tt_10) + as.numeric(kwh_cropproc_tt_11) + as.numeric(kwh_cropproc_tt_12))


sf$cropproc_demand <- cut(as.numeric(sf$kwh_cropproc_tt_)/1000, breaks = c(-Inf, 1, 5, 15, 30, 50, Inf), labels = c("<1", "1-5", "5-15", "15-30", "30-50", ">50"), right = FALSE)

c<- ggplot(sf)+
  geom_sf(aes(fill=cropproc_demand), color = NA)+
  ggtitle("Crop processing")+
  scale_fill_viridis(name="MWh", discrete = T)+
  theme(legend.position = "none")


sf$health_demand <- cut((as.numeric(sf$er_hc_tt))/1000, breaks = c(-Inf, 1, 5, 15, 30, 50, Inf), labels = c("<1", "1-5", "5-15", "15-30", "30-50", ">50"), right = FALSE)

sf$school_demand <- cut((as.numeric(sf$er_sch_tt))/1000, breaks = c(-Inf, 1, 5, 15, 30, 50, Inf), labels = c("<1", "1-5", "5-15", "15-30", "30-50", ">50"), right = FALSE)


d<- ggplot(sf)+
  geom_sf(aes(fill=health_demand), color = NA)+
  ggtitle("Healthcare facilities")+
  scale_fill_viridis(name="MWh", discrete = T)+
  theme(legend.position = "none")

e<- ggplot(sf)+
  geom_sf(aes(fill=school_demand), color = NA)+
  ggtitle("Education")+
  scale_fill_viridis(name="MWh", discrete = T)+
  theme(legend.position = "bottom", legend.direction = "horizontal")

sf = mutate(sf, residual_productive = as.numeric(residual_productive_tt_1) + as.numeric(residual_productive_tt_2) + as.numeric(residual_productive_tt_3) + as.numeric(residual_productive_tt_4) + as.numeric(residual_productive_tt_5) + as.numeric(residual_productive_tt_6) + as.numeric(residual_productive_tt_7) + as.numeric(residual_productive_tt_8) + as.numeric(residual_productive_tt_9) + as.numeric(residual_productive_tt_10) + as.numeric(residual_productive_tt_11) + as.numeric(residual_productive_tt_12))

sf$residual_productive <- cut((as.numeric(sf$residual_productive) * (as.numeric(sf$noaccsum) / as.numeric(sf$popsum)) * as.numeric(sf$HHs))/1000, breaks = c(-Inf, 1, 5, 15, 30, 50, Inf), 
                             labels = c("<1", "1-5", "5-15", "15-30", "30-50", ">50"), right = FALSE)

f<- ggplot(sf)+
  geom_sf(aes(fill=residual_productive), color = NA)+
  ggtitle("Commercial and productive")+
  scale_fill_viridis(name="MWh", discrete = T)+
  theme(legend.position = "none")

ggsave(plot_grid(plot_grid(a, b, c, d,  e + theme(legend.position = "none"), f, ncol = 3), get_legend(e), ncol = 1, rel_heights = c(1, 0.15)), filename = "sectoral_loads.png", device="png", scale=2, height = 4, width = 4)

###

sf <- read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_16.gpkg') 

a <- read.csv("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_8.csv") %>% dplyr::select(starts_with("kwh_cropproc_tt"), id)

b<- read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_16.csv')

a$X=NULL
b$X=NULL

sf = merge(sf, a, by="id")
sf = merge(sf, b, by="id")

sf2 = dplyr::select(sf, -starts_with("er_"))
sf2 = dplyr::select(sf2, -starts_with("CROPPROC"))
sf2 = dplyr::select(sf2, -starts_with("PerHHD"))
sf2 = dplyr::select(sf2, -starts_with("PET_"))
sf2 = dplyr::select(sf2, -starts_with("PPT_"))
sf2 = dplyr::select(sf2, -starts_with("SOI"))
sf2 = dplyr::select(sf2, -starts_with("monthly"))

sf_irrig = dplyr::select(sf, starts_with("er_kwh_tt")) %>% mutate(geometry=NULL) %>% mutate_all(as.numeric) %>% mutate(er_kwh_tt=rowSums(.))

sf_croppro = dplyr::select(sf, starts_with("kwh_cropproc_tt")) %>% mutate(geometry=NULL) %>% mutate_all(as.numeric) %>% mutate(kwh_cropproc_tt=rowSums(.))


sf2 = cbind(sf2, sf$PerHHD_tt, sf$er_hc_tt, sf$er_sch_tt, sf_irrig$er_kwh_tt, sf_croppro$kwh_cropproc_tt)

write_sf(sf2, 'D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/clusters_final.gpkg',driver="GPKG")




