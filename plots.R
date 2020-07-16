library(sf)
library(cowplot)
library(raster)
library(ggplot2)
library(scales)

sf <- read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_econ_results.gpkg')

setwd('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/results_figures')

fmt_dcimals <- function(decimals=0){
  # return a function responpsible for formatting the 
  # axis labels with a given number of decimals 
  function(x) as.character(round(x,decimals))
}


### pop and el access

a<- ggplot(sf)+
  geom_sf(aes(fill=popsum/Area*100), lwd = 0)+
  ggtitle("Population density")+
  scale_fill_binned(type = "viridis", trans="log", name="Inhab. / km2", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+
  guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")s

b<- ggplot(sf)+
  geom_sf(aes(fill=(1-(noaccsum/popsum))), lwd = 0)+
  ggtitle("Electricity access level")+
  scale_fill_binned(type = "viridis", breaks=seq(0, 1, by=0.25), name="El. access")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")


ggsave(plot_grid(a, b,  ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "pop_and_elaccess.png", device="png", scale=1.3)

### loads ###

a<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(PerHHD)), lwd = 0)+
  ggtitle("Residential demand")+
  scale_fill_binned(type = "viridis", name="kWh/hh", trans="log", labels = fmt_dcimals(0))+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

b<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(er_kwh)/Area*100), lwd = 0)+
  ggtitle("Irrigation demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

c<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(kwh_proc_cr)/Area*100), lwd = 0)+
  ggtitle("Crop processing demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

d<- ggplot(sf)+
  geom_sf(aes(fill=(as.numeric(HealthDemand)+as.numeric(EducationDemand))/Area*100), lwd = 0)+
  ggtitle("Health and education demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

e<- ggplot(sf)+
  geom_sf(aes(fill=ProductiveD/Area*100), lwd = 0)+
  ggtitle("Productive demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(plot_grid(a, b, c, d,  ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "sectoral_loads.png", device="png", scale=1.5)


#### barplot loads ####

d<- sf
d$residential = as.numeric(d$PerHHD)*as.numeric(d$HHs)
d <- dplyr::select(d, id, residential, HealthDemand, EducationDemand, er_kwh, kwh_proc_cr)

d = dplyr::mutate(d, share_non_res = (as.numeric(HealthDemand) + as.numeric(EducationDemand) + as.numeric(er_kwh) + as.numeric(kwh_proc_cr))/(as.numeric(HealthDemand) + as.numeric(EducationDemand) + as.numeric(er_kwh) + as.numeric(kwh_proc_cr) + as.numeric(residential)))
  
a<- ggplot(d)+
  geom_sf(aes(fill=as.numeric(share_non_res)*100), lwd = 0)+
  ggtitle("Share of non-residential demand")+
  scale_fill_binned(type = "viridis", breaks=seq(0, 100, by=10), name="%")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(a, filename = "nonres_dem.png", device="png", scale=1.3)

d$share_non_res=NULL
d$geom=NULL
d = dplyr::rename(d, Education = EducationDemand, Irrigation = er_kwh, Healthcare = HealthDemand, Crop_processing = kwh_proc_cr, `Residential (new electrification)` = residential)
d <- tidyr::gather(d, key="key", value="value", 2:6)
d$value = as.numeric(d$value)

d_graph<- ggplot(d)+
  geom_boxplot(aes(x=key, y=value/1000000, fill=key, group=key), alpha=0.8, outlier.alpha = 0)+
  scale_fill_discrete(name="Sector")+
  scale_y_log10(labels=prettyNum)+
  scale_x_discrete(labels=NULL)+
  xlab("")+
  ylab("GWh/year")+
  theme(legend.position = "bottom", legend.direction = "horizontal")

ggsave(d_graph, filename = "sectoral_loads_barplot.png", device="png")



#### agricultural maps ####
  
a<- ggplot(sf)+
  geom_sf(aes(fill=crshare), lwd = 0)+
  ggtitle("Share of cropland area")+
  scale_fill_binned(type = "viridis", breaks=seq(0, 1, by=0.2), name="%")+
  xlab("Longitude")+
  ylab("Latitude")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))

b<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(IRREQ_year)/1000), lwd = 0)+
  ggtitle("Irrigation water requirement")+
  scale_fill_binned(type = "viridis", name="Thousand m3/year", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(plot_grid(a, b,  ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "agriculture.png", device="png", scale=1.3)

c<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(yg_total)/1000/cr_ha_count), lwd = 0)+
  ggtitle("Total yield gap")+
  scale_fill_binned(type = "viridis", name="t//ha/year", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")


#### Electrification plots ####

electrification <- read.csv("D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/onsset/results/ke-1-0_0_0_0_0_0.csv")

sf = merge(sf, electrification, by.x="id", by.y="ID")


a<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(investmentreq)/as.numeric(popsum)), lwd = 0)+
  ggtitle("Local electrification \ninvestment requirement")+
  scale_fill_continuous(type = "viridis", name="USD per capita", labels = fmt_dcimals(2), breaks=c(25, 50, 100, 150, 200, 250), trans="log")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")


a<- ggplot(sf)+
  geom_sf(aes(fill=(InvestmentCost2025+InvestmentCost2030)/as.numeric(popsum)), lwd = 0)+
  ggtitle("Local electrification \ninvestment requirement")+
  scale_fill_continuous(type = "viridis", name="USD per capita", labels = fmt_dcimals(2), trans="log")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

b<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(MinimumOverallLCOE2030)), lwd = 0)+
  ggtitle("LCOE of the locally cheapest \nelectrification technology")+
  scale_fill_continuous(name="USD", labels = fmt_dcimals(2))+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(plot_grid(a, b,  ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "electrification.png", device="png", scale=1.4)


a<- ggplot(sf)+
  geom_sf(aes(fill=as.factor(MinimumOverall2030)), lwd = 0)+
  ggtitle("Local least-cost electrification technology")+
  scale_fill_discrete(name="Technology")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(a, filename = "techsplit.png", device="png", scale=1.3)



a<- ggplot(sf, aes(x="", y="", fill=MinimumOverall2030))+
  geom_bar(width = 1, stat = "identity")+ coord_polar("y", start=0)
  ggtitle("Local least-cost electrification technology")+
  scale_fill_discrete(name="Technology set-up")+
  theme(legend.position = "bottom", legend.direction = "horizontal")




### (partial) CBA ###

sf$dollarsperha <- cut(as.numeric(sf$profit_yearly)/as.numeric(sf$cr_ha_coun), 
                         breaks = c(0, 100, 250, 500, 1000, 2500, Inf), 
                         labels = c("<100 USD", "100-250 USD", "250-500 USD", "500-1000 USD", "1000 - 2500 USD", ">2500 USD"), right = FALSE)
  
a<- ggplot(sf)+
    geom_sf(aes(fill=dollarsperha), lwd = 0)+
    ggtitle("Revenue gain per year per ha \n(from artificial irrigation)")+
    scale_fill_viridis_d(name="USD/ha/year")+
    xlab("Longitude")+
    ylab("Latitude")

sf$PBT <- cut(as.numeric(sf$PBT), 
                       breaks = c(0, 1, 2, 5, 10, 15, Inf), 
                       labels = c("<1 yr.", "1-2 yrs.", "2-5 yrs.", "5-10 yrs.", "10-15 yrs.", ">15 yrs."), right = FALSE)  

b<- ggplot(sf)+
  geom_sf(aes(fill=PBT), lwd = 0)+
  ggtitle("Payback time of electrification investment from agricultural revenues")+
  scale_fill_viridis_d(name="Years")+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(a, filename = "Figure6a.png", device="png", scale=1.5)  
ggsave(b, filename = "Figure6b.png", device="png", scale=1.5)  



sf = dplyr::select(sf, contains("yg"))
sf$geom=NULL
sf$yg_total=NULL

sf = gather(sf, "crop", "yield_gap", 1:42)

sf = group_by(sf, crop) %>% summarise(yield_gap=sum(as.numeric(yield_gap), na.rm = T))

sf = subset(sf, sf$yield_gap>0)

sf$crop = gsub("yg_", "", sf$crop)

a<- ggplot(sf)+
  geom_col(aes(x=crop, y=yield_gap/1000000000), lwd = 0)+
  ggtitle("Maximum theorical yield gap in current cropland")+
  xlab("Crop")+
  ylab("Million tons / year")

ggsave("yg_kenya.png", a, device = "png", scale=2, width = 6)
=======
library(sf)
library(cowplot)
library(raster)
library(ggplot2)
library(scales)
sf <- read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_econ_results.gpkg')

setwd('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/results_figures')

fmt_dcimals <- function(decimals=0){
  # return a function responpsible for formatting the 
  # axis labels with a given number of decimals 
  function(x) as.character(round(x,decimals))
}


### pop and el access

a<- ggplot(sf)+
  geom_sf(aes(fill=popsum/Area*100), lwd = 0)+
  ggtitle("Population density")+
  scale_fill_binned(type = "viridis", trans="log", name="Inhab. / km2", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+
  guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

b<- ggplot(sf)+
  geom_sf(aes(fill=(1-(noaccsum/popsum))), lwd = 0)+
  ggtitle("Electricity access level")+
  scale_fill_binned(type = "viridis", breaks=seq(0, 1, by=0.25), name="El. access")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")


ggsave(plot_grid(a, b, labels="AUTO", ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "pop_and_elaccess.png", device="png", scale=1.3)

### loads ###

a<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(PerHHD)), lwd = 0)+
  ggtitle("Residential demand")+
  scale_fill_binned(type = "viridis", name="kWh/hh", trans="log", labels = fmt_dcimals(0))+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

b<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(er_kwh)/Area*100), lwd = 0)+
  ggtitle("Irrigation demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

c<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(kwh_proc_cr)/Area*100), lwd = 0)+
  ggtitle("Crop processing demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

d<- ggplot(sf)+
  geom_sf(aes(fill=(as.numeric(HealthDemand)+as.numeric(EducationDemand))/Area*100), lwd = 0)+
  ggtitle("Health and education demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

e<- ggplot(sf)+
  geom_sf(aes(fill=ProductiveD/Area*100), lwd = 0)+
  ggtitle("Productive demand")+
  scale_fill_binned(type = "viridis", name="kWh/km2", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(plot_grid(a, b, c, d, labels="AUTO", ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "sectoral_loads.png", device="png", scale=1.5)


#### barplot loads ####

d<- sf
d$residential = as.numeric(d$PerHHD)*as.numeric(d$HHs)
d <- dplyr::select(d, id, residential, HealthDemand, EducationDemand, er_kwh, kwh_proc_cr)

d = dplyr::mutate(d, share_non_res = (as.numeric(HealthDemand) + as.numeric(EducationDemand) + as.numeric(er_kwh) + as.numeric(kwh_proc_cr))/(as.numeric(HealthDemand) + as.numeric(EducationDemand) + as.numeric(er_kwh) + as.numeric(kwh_proc_cr) + as.numeric(residential)))
  
a<- ggplot(d)+
  geom_sf(aes(fill=as.numeric(share_non_res)*100), lwd = 0)+
  ggtitle("Share of non-residential demand")+
  scale_fill_binned(type = "viridis", breaks=seq(0, 100, by=10), name="%")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(a, filename = "nonres_dem.png", device="png", scale=1.3)

d$share_non_res=NULL
d$geom=NULL
d = dplyr::rename(d, Education = EducationDemand, Irrigation = er_kwh, Healthcare = HealthDemand, Crop_processing = kwh_proc_cr, `Residential (new electrification)` = residential)
d <- tidyr::gather(d, key="key", value="value", 2:6)
d$value = as.numeric(d$value)

d_graph<- ggplot(d)+
  geom_boxplot(aes(x=key, y=value/1000000, fill=key, group=key), alpha=0.8, outlier.alpha = 0)+
  scale_fill_discrete(name="Sector")+
  scale_y_log10(labels=prettyNum)+
  scale_x_discrete(labels=NULL)+
  xlab("")+
  ylab("GWh/year")+
  theme(legend.position = "bottom", legend.direction = "horizontal")

ggsave(d_graph, filename = "sectoral_loads_barplot.png", device="png")



#### agricultural maps ####
  
a<- ggplot(sf)+
  geom_sf(aes(fill=crshare), lwd = 0)+
  ggtitle("Share of cropland area")+
  scale_fill_binned(type = "viridis", breaks=seq(0, 1, by=0.2), name="%")+
  xlab("Longitude")+
  ylab("Latitude")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))

b<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(IRREQ_year)/1000), lwd = 0)+
  ggtitle("Irrigation water requirement")+
  scale_fill_binned(type = "viridis", name="Thousand m3/year", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(plot_grid(a, b, labels="AUTO", ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "agriculture.png", device="png", scale=1.3)

c<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(yg_total)/1000/cr_ha_count), lwd = 0)+
  ggtitle("Total yield gap")+
  scale_fill_binned(type = "viridis", name="t//ha/year", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

d<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(tt_ddvl)/cr_ha_count), lwd = 0)+
  ggtitle("Total revenue per year \n(from artificial irrigation)")+
  scale_fill_binned(type = "viridis", name="USD/ha/year", trans="log", breaks = log_breaks(n=6, base=10), labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(plot_grid(c, d, labels="AUTO", ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "agriculture2.png", device="png", scale=1.3)


#### Electrification plots ####

a<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(investmentreq)/as.numeric(popsum)), lwd = 0)+
  ggtitle("Local electrification \ninvestment requirement")+
  scale_fill_continuous(type = "viridis", name="USD per capita", labels = fmt_dcimals(2), breaks=c(25, 50, 100, 150, 200, 250), trans="log")+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

b<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(MinimumOverallLCOE2030)), lwd = 0)+
  ggtitle("LCOE of the locally cheapest \nelectrification technology")+
  scale_fill_continuous(name="USD", labels = fmt_dcimals(2))+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(plot_grid(a, b, labels="AUTO", ncol = 2, rel_heights = c(1,1), rel_widths = c(1,1)), filename = "electrification.png", device="png", scale=1.3)


a<- ggplot(sf)+
  geom_sf(aes(fill=as.factor(MinimumOverall2030)), lwd = 0)+
  ggtitle("Local least-cost electrification technology")+
  scale_fill_discrete(name="Technology")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(a, filename = "techsplit.png", device="png", scale=1.3)


### (partial) CBA ###

a<- ggplot(sf)+
  geom_sf(aes(fill=as.numeric(PBT)), lwd = 0)+
  ggtitle("Payback time of electrification investment (considering agricultural revenues)")+
  scale_fill_binned(type = "viridis", name="Years", trans="log", labels=prettyNum)+
  theme(legend.position = "bottom", legend.direction = "horizontal", legend.key.width = unit(1.5, "cm"))+   guides(fill = guide_colorbar(title.position="top", title.hjust = 0.5))+
  xlab("Longitude")+
  ylab("Latitude")

ggsave(a, filename = "partial_CBA.png", device="png", scale=1.3)

>>>>>>> bd368406b6772c89dcd5cc8ec865ee33c5860ea4
