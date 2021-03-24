shape = ee$FeatureCollection('USDOS/LSIB_SIMPLE/2017')$filter(ee$Filter$eq('country_na', countryname))

imageCollection = ee$Image("users/giacomofalchetta/hrsl_images")

imageCollection = imageCollection$mask(imageCollection$gte(5))$toInt()

vectors = imageCollection$addBands(imageCollection)$reduceToVectors(ee$Reducer$mean(), shape, 500, 'polygon', TRUE, 'pop', 
                                                                    imageCollection$projection(), NULL, FALSE, 1312133037)

task_vector <- ee_table_to_drive(
  collection = vectors,
  fileFormat = "GEO_JSON",
  fileNamePrefix = "vectors"
)

task_vector$start()
ee_monitoring(task_vector) # optional
clusters <- read_sf(ee_drive_to_local(task = task_vector))
