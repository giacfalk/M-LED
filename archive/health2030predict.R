library(sf)
library(nngeo)

desk_path <- file.path(Sys.getenv("USERPROFILE"),"Desktop")
home_repo_folder <- read.table(paste0(desk_path, "/repo_folder_path.txt"),header = F,nrows = 1)  
db_folder <- read.table(paste0(desk_path, "/repo_folder_path.txt"),header = F,nrows = 1)  


# read kenya geo
kenya_geo <- read_sf(paste0(db_folder, '/processed_folder/health_facilities_in_kenya.shp'))

kenya_geo_1 = subset(kenya_geo, kenya_geo$heal_type1==1)
kenya_geo_2 = subset(kenya_geo, kenya_geo$heal_type2==1)
kenya_geo_345 = subset(kenya_geo, kenya_geo$heal_type3==1 | kenya_geo$heal_type4==1 | kenya_geo$heal_type5==1)

# read kenya 2030
kenya_2030 <- read_sf(paste0(db_folder, '/input_folder/all_facilities_2030.gpkg'))

kenya_2030_1 = subset(kenya_2030, kenya_2030$tier=="Tier 1")
kenya_2030_2 = subset(kenya_2030, kenya_2030$tier=="Tier 2")
kenya_2030_3 = subset(kenya_2030, kenya_2030$tier=="Tier 3/4")


# nn by each of the three levels

kenya_2030_1 <- st_join(kenya_2030_1, kenya_geo_1, st_nn)
kenya_2030_2 <- st_join(kenya_2030_2, kenya_geo_2, st_nn)
kenya_2030_3 <- st_join(kenya_2030_3, kenya_geo_345, st_nn)

# bind
kenya_2030 = rbind(kenya_2030_1, kenya_2030_2, kenya_2030_3) %>% st_as_sf()

write_sf(kenya_2030, paste0(db_folder, '/processed_folder/health_facilities_in_kenya_merged.gpkg'))
