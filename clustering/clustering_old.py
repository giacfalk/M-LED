# trim to pop pixels > 10
population = QgsRasterLayer(input_folder + 'Population.tif')

entries = []
# Define band1
boh1 = QgsRasterCalculatorEntry()
boh1.ref = 'boh@1'
boh1.raster = population
boh1.bandNumber = 1
entries.append(boh1)

# Process calculation with input extent and resolution
calc = QgsRasterCalculator('((boh@1>10)*boh@1) / ((boh@1>10)*1 + (boh@1<=10)*0) ', processed_folder + 'Population_trimmed.tif', 'GTiff', kernel.extent(), kernel.width(), kernel.height(), entries)
calc.processCalculation()

processing.run("native:pixelstopolygons", {'INPUT_RASTER':processed_folder + 'Population_trimmed.tif','RASTER_BAND':1,'FIELD_NAME':'VALUE','OUTPUT':processed_folder + 'pixels.shp'})

processing.run("native:buffer", {'INPUT':processed_folder + 'pixels.shp','DISTANCE':0.008333,'SEGMENTS':4,'END_CAP_STYLE':2,'JOIN_STYLE':2,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':processed_folder + 'buffered.shp'})

processing.run("native:dissolve", {'INPUT':processed_folder + 'buffered.shp','FIELD':[],'OUTPUT':processed_folder + 'dissolved.shp'})

processing.run("native:multiparttosingleparts", {'INPUT':processed_folder + 'dissolved.shp','OUTPUT':processed_folder + 'singlepart.shp'})

processing.run("native:centroids", {'INPUT':processed_folder + 'singlepart.shp','ALL_PARTS':False,'OUTPUT':processed_folder + 'centroids.shp'})

processing.run("qgis:voronoipolygons", {'INPUT':processed_folder + 'centroids.shp','BUFFER':0,'OUTPUT':processed_folder + 'voronoi.shp'})

processing.run("saga:polygonclipping", {'CLIP':gadm0,'S_INPUT':processed_folder + 'voronoi.shp','S_OUTPUT':processed_folder + 'voronoi_clipped.shp'})

processing.run("native:fixgeometries", {'INPUT':processed_folder + 'voronoi_clipped.shp','OUTPUT':processed_folder + 'voronoi_clipped_repaired.shp'})