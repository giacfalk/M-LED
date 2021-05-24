cl_bk <- clusters

source_lines <- function(file, lines){
  source(textConnection(readLines(file)[lines]))
}

source("manual_parameters.R")
source_lines("scenario_baseline.R", 230:237)

geogeo <- clusters$geometry

clusters <- cl_bk

if (is.null(geogeo)){
    geogeo <- clusters$geom
}

clusters$geometry=NULL
clusters$geom=NULL

####

sf_irrig = dplyr::select(clusters,starts_with("er_kwh_tt"))

sf_irrig$id = 1:nrow(clusters)

sf_irrig = tidyr::gather(sf_irrig, "month_tt", "value_tt", 1:12)

sf_irrig$month_tt = as.numeric(gsub("er_kwh_tt", "", sf_irrig$month_tt))

sf_irrig$value_tt = as.numeric(sf_irrig$value_tt)

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
  theme_classic()+
  geom_line(aes(group=as.factor(month_tt), colour=as.factor(month_tt)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed (daily avg.)")+
  ggtitle("Irrigation")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

### Crop processing ###
sf_croppro = dplyr::select(clusters,starts_with("kwh_cropproc_tt"))

for (i in 1:ncol(sf_croppro)){
  sf_croppro[,i] <-  ifelse(is.infinite(sf_croppro[,i]), 0, sf_croppro[,i])
  }

sf_croppro$id = 1:nrow(clusters)

sf_croppro = tidyr::gather(sf_croppro, "month_tt", "value_tt", 1:12)

sf_croppro$month_tt = as.numeric(gsub("kwh_cropproc_tt_", "", sf_croppro$month_tt))

sf_croppro$value_tt = as.numeric(sf_croppro$value_tt)

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
  theme_classic()+
  geom_line(aes(group=as.factor(month_tt), colour=as.factor(month_tt)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed (daily avg.)")+
  ggtitle("Crop processing")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

## Health ##
gc()
sf_health = dplyr::select(clusters, id, starts_with("er_hc_"))
sf_health$er_hc_tt = NULL

for (i in 1:ncol(sf_health)){
  sf_health[,i] <-  ifelse(is.infinite(sf_health[,i]) | is.nan(sf_health[,i]) | is.na(sf_health[,i]) , 0, sf_health[,i])
}


sf_health$er_hc_tt_monthly_1 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_1 )
sf_health$er_hc_tt_monthly_2 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_2 )
sf_health$er_hc_tt_monthly_3 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_3 )
sf_health$er_hc_tt_monthly_4 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_4 )
sf_health$er_hc_tt_monthly_5 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_5 )
sf_health$er_hc_tt_monthly_6 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_6 )
sf_health$er_hc_tt_monthly_7 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_7 )
sf_health$er_hc_tt_monthly_8 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_8 )
sf_health$er_hc_tt_monthly_9 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_9 )
sf_health$er_hc_tt_monthly_10 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_10 )
sf_health$er_hc_tt_monthly_11 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_11 )
sf_health$er_hc_tt_monthly_12 = ifelse(clusters$elrate>0.75, 0, sf_health$er_hc_tt_monthly_12 )

sf_health_tt = tidyr::gather(sf_health %>% dplyr::select(290:301, 1), "date_tt", "value_tt", 1:12)
sf_health_tt$month = as.numeric((sub('.*\\_', "", gsub("er_hc_tt_monthly_", "", sf_health_tt$date_tt))))

sf_health = tidyr::gather(sf_health %>% dplyr::select(2:289, 1), "date", "value", 1:288)
sf_health$hour = as.numeric((sub('.*\\_', "", gsub("er_hc_", "", sf_health$date))))
sf_health$month = as.numeric((sub('\\_.*', "", gsub("er_hc_", "", sf_health$date))))


sf_health = merge(sf_health,sf_health_tt, by=c("id", "month"))

sf_health$value = as.numeric(sf_health$value_tt)*as.numeric(sf_health$value)

sf_health = dplyr::select(sf_health, hour, value, month) %>% group_by(hour, month) %>% summarise(value=sum(value, na.rm=T)) %>% ungroup()

sf_health$hour = as.numeric(sf_health$hour)


health<-ggplot(sf_health, aes(x=as.numeric(hour), y=value))+
  theme_classic()+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed (daily avg.)")+
  ggtitle("Healthcare")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

## Edu ##
gc()
sf_edu = dplyr::select(clusters, id, starts_with("er_sch_"))
sf_edu$er_sch_tt = NULL

for (i in 1:ncol(sf_edu)){
  sf_edu[,i] <-  ifelse(is.infinite(sf_edu[,i]) | is.nan(sf_edu[,i]) | is.na(sf_edu[,i]) , 0, sf_edu[,i])
}


sf_edu$er_sch_tt_monthly_1 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_1 )
sf_edu$er_sch_tt_monthly_2 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_2 )
sf_edu$er_sch_tt_monthly_3 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_3 )
sf_edu$er_sch_tt_monthly_4 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_4 )
sf_edu$er_sch_tt_monthly_5 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_5 )
sf_edu$er_sch_tt_monthly_6 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_6 )
sf_edu$er_sch_tt_monthly_7 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_7 )
sf_edu$er_sch_tt_monthly_8 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_8 )
sf_edu$er_sch_tt_monthly_9 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_9 )
sf_edu$er_sch_tt_monthly_10 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_10 )
sf_edu$er_sch_tt_monthly_11 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_11 )
sf_edu$er_sch_tt_monthly_12 = ifelse(clusters$elrate>0.75, 0, sf_edu$er_sch_tt_monthly_12 )

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
  theme_classic()+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed (daily avg.)")+
  ggtitle("Education")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

## Residential
gc()
sf_residential = dplyr::select(clusters, id, starts_with("PerHHD_")) %>% as.data.frame()
sf_residential$PerHHD_tt = NULL

for (i in 1:ncol(sf_residential)){
  sf_residential[,i] <-  ifelse(is.infinite(sf_residential[,i]) | is.nan(sf_residential[,i]) | is.na(sf_residential[,i]) , 0, sf_residential[,i])
}

sf_residential$PerHHD_tt_monthly_1 = as.numeric(sf_residential$PerHHD_tt_monthly_1) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_2 = as.numeric(sf_residential$PerHHD_tt_monthly_2) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_3 = as.numeric(sf_residential$PerHHD_tt_monthly_3) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_4 = as.numeric(sf_residential$PerHHD_tt_monthly_4) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_5 = as.numeric(sf_residential$PerHHD_tt_monthly_5) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_6 = as.numeric(sf_residential$PerHHD_tt_monthly_6) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_7 = as.numeric(sf_residential$PerHHD_tt_monthly_7) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_8 = as.numeric(sf_residential$PerHHD_tt_monthly_8) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_9 = as.numeric(sf_residential$PerHHD_tt_monthly_9) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_10 = as.numeric(sf_residential$PerHHD_tt_monthly_10) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_11 = as.numeric(sf_residential$PerHHD_tt_monthly_11) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residential$PerHHD_tt_monthly_12 = as.numeric(sf_residential$PerHHD_tt_monthly_12) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)

sf_residential_tt = tidyr::gather(sf_residential %>% dplyr::select(290:301, 1), "date_tt", "value_tt", 1:12)

sf_residential_tt$month = as.numeric((sub('.*\\_', "", gsub("PerHHD_tt_monthly_", "", sf_residential_tt$date_tt))))

sf_residential = tidyr::gather(sf_residential %>% dplyr::select(2:289, 1), "date", "value", 1:288)
sf_residential$hour = as.numeric((sub('.*\\_', "", gsub("PerHHD_", "", sf_residential$date))))
sf_residential$month = as.numeric((sub('\\_.*', "", gsub("PerHHD_", "", sf_residential$date))))

sf_residential <- as.data.table(sf_residential)
sf_residential_tt <- as.data.table(sf_residential_tt)

sf_residential = merge(sf_residential,sf_residential_tt, by=c("id", "month"))

sf_residential$value = as.numeric(sf_residential$value_tt)*as.numeric(sf_residential$value)

sf_residential = dplyr::select(sf_residential, hour, value, month) %>% group_by(hour, month) %>% summarise(value=sum(value, na.rm=T)) %>% ungroup()

sf_residential$hour = as.numeric(sf_residential$hour)

residential <-ggplot(sf_residential, aes(x=as.numeric(hour), y=value/1000))+
  theme_classic()+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed (daily avg.)")+
  ggtitle("Residential")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

######
# residual productive
## residual_productive
gc()
sf_residual_productive = dplyr::select(clusters, id, starts_with("residual_productive_")) %>% as.data.frame()

for (i in 1:ncol(sf_residual_productive)){
  sf_residual_productive[,i] <-  ifelse(is.infinite(sf_residual_productive[,i]) | is.nan(sf_residual_productive[,i]) | is.na(sf_residual_productive[,i]) , 0, sf_residual_productive[,i])
}

sf_residual_productive$residual_productive_tt_1 = as.numeric(sf_residual_productive$residual_productive_tt_1) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_2 = as.numeric(sf_residual_productive$residual_productive_tt_2) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_3 = as.numeric(sf_residual_productive$residual_productive_tt_3) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_4 = as.numeric(sf_residual_productive$residual_productive_tt_4) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_5 = as.numeric(sf_residual_productive$residual_productive_tt_5) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_6 = as.numeric(sf_residual_productive$residual_productive_tt_6) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_7 = as.numeric(sf_residual_productive$residual_productive_tt_7) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_8 = as.numeric(sf_residual_productive$residual_productive_tt_8) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_9 = as.numeric(sf_residual_productive$residual_productive_tt_9) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_10 = as.numeric(sf_residual_productive$residual_productive_tt_10) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_11 = as.numeric(sf_residual_productive$residual_productive_tt_11) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)
sf_residual_productive$residual_productive_tt_12 = as.numeric(sf_residual_productive$residual_productive_tt_12) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)

for (i in 1:ncol(sf_residual_productive)){
  sf_residual_productive[,i] <-  ifelse(is.infinite(sf_residual_productive[,i]) | is.nan(sf_residual_productive[,i]) | is.na(sf_residual_productive[,i]) , 0, sf_residual_productive[,i])
}

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
  theme_classic()+
  geom_line(aes(group=as.factor(month), colour=as.factor(month)), size=1)+
  #facet_wrap(~Sector)+
  xlab("Hour")+
  ylab("MWh consumed (daily avg.)")+
  ggtitle("Commercial & prod.")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_colour_discrete(name="Month")

#####

all_sectors <- cowplot::plot_grid(residential + theme(legend.position = "none"), edu + theme(legend.position = "none"), health + theme(legend.position = "none"), irrigation + theme(legend.position = "none"), crop_pro + theme(legend.position = "none"), residual_productive + theme(legend.position = "none"))


all_sectors <- cowplot::plot_grid(all_sectors, get_legend(crop_pro), ncol = 1, rel_heights = c(1, 0.15))

ggsave("all.png", all_sectors, device = "png", scale=1.2)

Residential<-sum(residential$data$value)*30
Education<-sum(edu$data$value)*30
Healthcare<-sum(health$data$value)*30
Irrigation<-sum(irrigation$data$value_irrigation)*30
Crop_processing<-sum(crop_pro$data$value_cropproation)*30
Comm_prod <- sum(residual_productive$data$value)*30

print("Latent demand (estimated) TWh:")
sum(Residential, Education, Healthcare, Irrigation, Crop_processing, Comm_prod)/1e6  

df <- as.data.frame(rbind(Residential, Education, Healthcare, Irrigation, Crop_processing, Comm_prod))
df$sector<-rownames(df)

barplot <- ggplot(df, aes(x=sector, y=V1/1e6))+
  theme_classic()+
  geom_col(aes(fill=sector))+
  scale_y_continuous(name="Yearly unmet electricity demand (TWh)")+
  xlab("Sector")+
  scale_fill_discrete(name="Sector")+
  theme(legend.position = "bottom", legend.direction = "horizontal")

ggsave("barplot_sectors.png", barplot, device = "png", scale=1, width = 7, height = 5)

############

source_lines("scenario_baseline.R", c(7, 99:103))

country_temp <- st_union(gadm1) %>% st_as_sf()
country <- gadm1[1,]
country$NAME_1 <- countryiso3
country$geometry <- country_temp$x

gadm1 <- bind_rows(gadm1, country)

template <- raster(paste0(db_folder, '/input_folder/template_1km.tif'))

clusters$geometry=geogeo

clusters = st_as_sf(clusters)

clusters <- mutate(clusters, sf_residential_tt = (30 * (as.numeric(PerHHD_tt_monthly_1) + as.numeric(PerHHD_tt_monthly_2) + as.numeric(PerHHD_tt_monthly_3) + as.numeric(PerHHD_tt_monthly_4) + as.numeric(PerHHD_tt_monthly_5) + as.numeric(PerHHD_tt_monthly_6) + as.numeric(PerHHD_tt_monthly_7) + as.numeric(PerHHD_tt_monthly_8) + as.numeric(PerHHD_tt_monthly_9) + as.numeric(PerHHD_tt_monthly_10) + as.numeric(PerHHD_tt_monthly_11) + as.numeric(PerHHD_tt_monthly_12))/1000) * as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop)) 

clusters <-clusters <- mutate(clusters, sf_croppro = (30 * (as.numeric(kwh_cropproc_tt_1) + as.numeric(kwh_cropproc_tt_2) + as.numeric(kwh_cropproc_tt_3) + as.numeric(kwh_cropproc_tt_4) + as.numeric(kwh_cropproc_tt_5) + as.numeric(kwh_cropproc_tt_6) + as.numeric(kwh_cropproc_tt_7) + as.numeric(kwh_cropproc_tt_8) + as.numeric(kwh_cropproc_tt_9) + as.numeric(kwh_cropproc_tt_10) + as.numeric(kwh_cropproc_tt_11) + as.numeric(kwh_cropproc_tt_12))/1000))

clusters <-clusters <- mutate(clusters, sf_irrig = (30 * (as.numeric(er_kwh_tt1) + as.numeric(er_kwh_tt2) + as.numeric(er_kwh_tt3) + as.numeric(er_kwh_tt4) + as.numeric(er_kwh_tt5) + as.numeric(er_kwh_tt6) + as.numeric(er_kwh_tt7) + as.numeric(er_kwh_tt8) + as.numeric(er_kwh_tt9) + as.numeric(er_kwh_tt10) + as.numeric(er_kwh_tt11) + as.numeric(er_kwh_tt12))/1000))

clusters$sf_health_tt<-30* as.numeric(clusters$er_hc_tt)/1000

clusters$sf_health_tt = ifelse(clusters$elrate>0.75, 0, clusters$sf_health_tt )

clusters$sf_edu_tt<-30* as.numeric(clusters$er_sch_tt)/1000

clusters$sf_edu_tt = ifelse(clusters$elrate>0.75, 0, clusters$sf_edu_tt )

clusters = mutate(clusters, sf_residual_productive_tt = (30 * (as.numeric(residual_productive_tt_1) + as.numeric(residual_productive_tt_2) + as.numeric(residual_productive_tt_3) + as.numeric(residual_productive_tt_4) + as.numeric(residual_productive_tt_5) + as.numeric(residual_productive_tt_6) + as.numeric(residual_productive_tt_7) + as.numeric(residual_productive_tt_8) + as.numeric(residual_productive_tt_9) + as.numeric(residual_productive_tt_10) + as.numeric(residual_productive_tt_11) + as.numeric(residual_productive_tt_12))/1000)* as.numeric(clusters$HHs) * (clusters$noacc/clusters$pop))

clusters$sf_residential_tt <- ifelse(is.nan(clusters$sf_residential_tt), 0, clusters$sf_residential_tt)

clusters$sf_croppro <- ifelse(is.nan(clusters$sf_croppro), 0, clusters$sf_croppro)

clusters$sf_irrig <- ifelse(is.nan(clusters$sf_irrig), 0, clusters$sf_irrig)

clusters$sf_health_tt <- ifelse(is.nan(clusters$sf_health_tt), 0, clusters$sf_health_tt)

clusters$sf_edu_tt <- ifelse(is.nan(clusters$sf_edu_tt), 0, clusters$sf_edu_tt)

clusters$sf_residual_productive_tt <- ifelse(is.nan(clusters$sf_residual_productive_tt), 0, clusters$sf_residual_productive_tt)

sf_residential_tt <- fasterize::fasterize(clusters, template, field ="sf_residential_tt", fun="sum")

sf_croppro <- fasterize::fasterize(clusters, template, field ="sf_croppro", fun="sum")

sf_irrig <- fasterize::fasterize(clusters, template, field ="sf_irrig", fun="sum")

sf_health_tt <- fasterize::fasterize(clusters, template, field ="sf_health_tt", fun="sum")

sf_edu_tt <- fasterize::fasterize(clusters, template, field ="sf_edu_tt", fun="sum")

sf_residual_productive_tt <- fasterize::fasterize(clusters, template, field ="sf_residual_productive_tt", fun="sum")

gadm1$Residential <- exactextractr::exact_extract(sf_residential_tt, gadm1, fun="sum")
gadm1$Education<- exactextractr::exact_extract(sf_edu_tt, gadm1, fun="sum")
gadm1$Healthcare<- exactextractr::exact_extract(sf_health_tt, gadm1, fun="sum")
gadm1$Irrigation<- exactextractr::exact_extract(sf_irrig, gadm1, fun="sum")
gadm1$Crop_processing<- exactextractr::exact_extract(sf_croppro, gadm1, fun="sum")
gadm1$Comm_prod<- exactextractr::exact_extract(sf_residual_productive_tt, gadm1, fun="sum")

gadm1 <- gather(gadm1, key = "sector", value = "value", 12:17)

gadm1$countryiso3 <- ifelse(gadm1$NAME_1==countryiso3, 0, 1)

barplot_prov <- ggplot(gadm1, aes(x=NAME_1, y=value/1e9))+
  theme_classic()+
  geom_bar(aes(fill=sector), position = "stack", stat = "identity", colour="black", lwd=0.01)+
  scale_y_continuous(name="Yearly latent electricity demand (TWh)")+
  xlab("Province")+
  scale_fill_discrete(name="Sector")+
  theme(legend.position = "bottom", legend.direction = "horizontal", strip.background = element_blank(), strip.text = element_blank())+
  facet_wrap(vars(gadm1$countryiso3), scales = "free")

gt = ggplot_gtable(ggplot_build(barplot_prov))
gt$widths[5] = 0.3*gt$widths[5]
grid.draw(gt)

ggsave("gadm1.png", gt, scale = 1.3)

gadm1_map <- gadm1[-nrow(gadm1),]

map_regions <- ggplot(gadm1_map, aes(fill=NAME_1))+
  theme_classic()+
  geom_sf()+
  scale_fill_brewer(palette = "Set2", name="Regions")

ggsave("regions_map.png", map_regions, device = "png")

# raster to polygons (clusters)
grd <- sf::st_make_grid(gadm0, cellsize = 0.0083, square = T, what = "polygons", crs = 4326)
grd <- st_as_sf(grd)

# extract sum, by sector
grd$Residential <- exactextractr::exact_extract(sf_residential_tt, grd, fun="sum")
grd$Education<- exactextractr::exact_extract(sf_edu_tt, grd, fun="sum")
grd$Healthcare<- exactextractr::exact_extract(sf_health_tt, grd, fun="sum")
grd$Irrigation<- exactextractr::exact_extract(sf_irrig, grd, fun="sum")
grd$Crop_processing<- exactextractr::exact_extract(sf_croppro, grd, fun="sum")
grd$Comm_prod<- exactextractr::exact_extract(sf_residual_productive_tt, grd, fun="sum")

# Plot 
r <- stack(sf_residential_tt, sf_irrig, sf_croppro, sf_health_tt, sf_edu_tt, sf_residual_productive_tt)

names(r) <- c("Residential", "Irrigation", "Crop_processing", "Healthcare", "Education", "Productive_commercial")

ext <- as.vector(extent(r))

boundaries <- map('worldHires', fill=TRUE,
                  xlim=ext[1:2], ylim=ext[3:4],
                  plot=FALSE)

IDs <- sapply(strsplit(boundaries$names, ":"), function(x) x[1])
bPols <- map2SpatialPolygons(boundaries, IDs=IDs,
                             proj4string=CRS(projection(r)))

my.at <- c(0.1, 0.5, 1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000)
my.brks=seq(0.1, 25000, by=1666.667)
myColorkey <- list(at=my.brks, labels=list(at=my.brks, labels=my.at), space="bottom")

YlOrRdTheme <- rasterTheme(panel.background = list(col='white'))

png("map.png", width=1800, height=1200, res=150)
print(levelplot(r, xlim=c(34, 42), ylim=c(-5, 5),
                main="Yearly sectoral latent demand (MWh/km2)", at=my.at, colorkey=myColorkey, xlab="Longitude", ylab="Latitude", par.settings = YlOrRdTheme) + layer(sp.polygons(bPols, lwd=0.1, col='black')))
dev.off()
