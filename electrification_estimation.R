#####################
# Population and electrification calculation
#####################
gaul_code <-countrycode(countryiso3, "iso3c", "gaul")
gaul = ee$FeatureCollection("FAO/GAUL/2015/level0")$filter(ee$Filter$eq('ADM0_CODE', gaul_code))
imageCollection = ee$ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG");
nl20 =  imageCollection$filterDate('2019-01-01', '2020-01-01')$select('avg_rad')$median()
zero = ee$Image(0)

Sys.sleep(1)

nl20 = nl20$where(nl20$lt(0.37), zero)$clip(gaul)

pop = ee$Image('users/giacomofalchetta/hrsl_images')$clip(gaul)

popnoaccess = pop$mask(nl20$eq(0))$clip(gaul)

popnoaccess <- ee_as_raster(
  image = popnoaccess,
  region = gaul$geometry(),
  via = "drive",
  scale = 1000
)

clusters$noacc <- exactextractr::exact_extract(popnoaccess, clusters, fun="sum")

pop <- ee_as_raster(
  image = pop,
  region = gaul$geometry(),
  via = "drive",
  scale = 1000
)

clusters$pop <- exactextractr::exact_extract(pop, clusters, fun="sum")

# estimate electrification rate of each cluster
clusters$elrate <- 1- (clusters$noacc/clusters$pop)

# adjust
somma = sum(clusters$pop)
spread = ((national_official_population-somma)/somma)
clusters$pop <- clusters$pop * (1+spread)

somma = sum(clusters$noacc)
spread = (((national_official_population*(1-national_official_elrate))-somma)/somma)
clusters$noacc <- clusters$noacc * (1+spread)

elrate_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=elrate))+
  scale_fill_viridis_c(trans="log", name="Electr. acc. rate (2019 estimate)")

pop_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=pop))+
  scale_fill_viridis_c(trans="log")

noacc_plot <- ggplot(data=clusters)+
  geom_sf(aes(fill=noacc))+
  scale_fill_viridis_c(trans="log")
