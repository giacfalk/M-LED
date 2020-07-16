library(sf)
library(cowplot)
library(raster)
library(ggplot2)
library(scales)
library(tidyr)
library(tidyverse)
library(sf)


sf <- read_sf('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_econ_results.gpkg')

setwd('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/results_figures')

# Plot  

# A Revenues net of transport and pumping
sf_agri = dplyr::select(sf, contains("yg"))
sf_agri$geom=NULL
sf_agri$yg_total=NULL

sf_agri = gather(sf_agri, "crop", "yield_gap", 1:42)

sf_agri = group_by(sf_agri, crop) %>% summarise(yield_gap=sum(as.numeric(yield_gap), na.rm = T))

sf_agri = subset(sf_agri, sf_agri$yield_gap>0)

sf_agri$crop = gsub("yg_", "", sf_agri$crop)

names <- read.csv("https://raw.githubusercontent.com/wri/MAPSPAM/master/metadata_tables/mapspam_names.csv")

names$SPAM_name <- as.character(names$SPAM_name)

sf_agri<-merge(sf_agri, names, by.x="crop", by.y="SPAM_name")

a<- ggplot(sf_agri)+
  theme_classic()+
  geom_col(aes(x=name, y=yield_gap/1000000000, fill=crop_group), lwd = 0.01, colour="black")+
  ggtitle("Maximum theorical yield gap in currently rainfed cropland")+
  xlab("Crop")+
  ylab("Million tons / year")+
  scale_fill_brewer(name="Crop type", palette = "Set1")+ 
  theme(axis.text.x = element_text(angle = 90))

  
ggsave("maxyields.png", a, device = "png")

# B Maximum theretical yield
template <- raster('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/input_folder/template_1km.tif')

sf$dollarsperha <- as.numeric(sf$profit_yearly)/as.numeric(sf$cr_ha_coun)

dollarsperha <- fasterize::fasterize(sf, template, field ="dollarsperha", fun="sum")

# C Transport cost map
sf$transp_costs <- as.numeric(sf$transp_costs)/as.numeric(sf$cr_ha_coun)

transp_costs <- fasterize::fasterize(sf, template, field ="transp_costs", fun="sum")

# D Pumping costs map
sf$TC_pumping <- as.numeric(sf$TC_pumping)/as.numeric(sf$cr_ha_coun)

TC_pumping <- fasterize::fasterize(sf, template, field ="TC_pumping", fun="sum")

r <- stack(dollarsperha, transp_costs, TC_pumping)

names(r) <- c("Revenues", "Trans_costs", "Pumping_costs")

ext <- as.vector(extent(r))

library(maps)  
library(mapdata)
library(maptools)

boundaries <- map('worldHires', fill=TRUE,
                  xlim=ext[1:2], ylim=ext[3:4],
                  plot=FALSE)

IDs <- sapply(strsplit(boundaries$names, ":"), function(x) x[1])
bPols <- map2SpatialPolygons(boundaries, IDs=IDs,
                             proj4string=CRS(projection(r)))

r <- stack(r)

my.at <- c(0, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 500000, 1000000)
my.brks=seq(0, 1000000, by=90909.09)
myColorkey <- list(at=my.brks, labels=list(at=my.brks, labels=my.at), space="bottom")

library(rasterVis)
YlOrRdTheme <- rasterTheme(panel.background = list(col='white'))

png("map_econ.png", width=1800, height=1200, res=150)
print(levelplot(r, xlim=c(34, 42), ylim=c(-5, 5),
                main="Yearly revenue and costs (USD/ha/year)", at=my.at, colorkey=myColorkey, xlab="Longitude", ylab="Latitude", par.settings = YlOrRdTheme) + layer(sp.polygons(bPols, lwd=0.1, col='black')))
dev.off()


library(rasterVis)

my.at <- c(1, 250, 500, 1000, 2500, 5000)
my.brks=seq(1, 5000, by=833.3333)
myColorkey <- list(at=my.brks, labels=list(at=my.brks, labels=my.at), space="bottom")

values(dollarsperha) <- ifelse(values(dollarsperha)>2500, 5000, values(dollarsperha))

png("map_revenues.png", width=1800, height=1200, res=150)
print(levelplot(dollarsperha, margin=F, xlim=c(34, 42), ylim=c(-5, 5),
                main="Local revenues net of pumping transport to market costs (USD/ha/year)", at=my.at, colorkey=myColorkey, xlab="Longitude", ylab="Latitude", par.settings = rasterVis::YlOrRdTheme) + layer(sp.polygons(bPols, lwd=0.1, col='black')))
dev.off()

