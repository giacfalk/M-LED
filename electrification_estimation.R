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

pop15 = ee$Image('users/giacomofalchetta/hrsl_images')$clip(gaul)

pop20_noaccess = pop15$mask(pop15$gt(0)$And(nl20$eq(0)))$clip(gaul)

popnoaccess2018 <- ee_as_raster(
  image = pop20_noaccess,
  region = gaul$geometry(),
  via = "drive",
  scale = 1000
)

population <- ee_as_raster(
  image = pop15,
  region = gaul$geometry(),
  via = "drive",
  scale = 1000
)

clusters$pop <- exactextractr::exact_extract(population, clusters, fun="sum")
clusters$noacc <- exactextractr::exact_extract(popnoaccess2018, clusters, fun="sum")

##

popnoaccess2018 = raster(paste0(processed_folder , 'noaccess/pop18_noaccess_kenya.tif'))
population = raster(paste0(processed_folder , 'noaccess/pop18_kenya.tif'))

# adjust
somma = sum(clusters$pop)
spread = ((national_official_population-somma)/somma)

print(spread)

clusters$pop <- clusters$pop * 1+spread

somma = sum(clusters$noacc)
spread = (((national_official_population*(1-national_official_elrate))-somma)/somma)

print(spread)

clusters$noacc <- clusters$noacc * 1+spread

# estimate electrification rate of each cluster
clusters$elrate <- 1- (clusters$noacc/clusters$pop)
