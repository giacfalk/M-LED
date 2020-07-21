desk_path <- file.path(Sys.getenv("USERPROFILE"),"Desktop")
home_repo_folder <- read.table(paste0(desk_path, "/repo_folder_path.txt"),header = F,nrows = 1)  
db_folder <- read.table(paste0(desk_path, "/repo_folder_path.txt"),header = F,nrows = 1)  

costs<-read.csv(paste0(db_folder, '/input_folder/electric_pumps_costs.csv'))

costs$Depth...m.well.=as.numeric(costs$Depth...m.well.)
costs$Yield..m3.hour..=as.numeric(costs$Yield..m3.hour..) * 0.000277778
costs$Total.costs....US...well.=as.numeric(costs$Total.costs....US...well.)
costs$Fixed.Costs..US...well. = as.numeric(costs$Fixed.Costs..US...well.)
costs$Diam...inch.well. = as.numeric(costs$Diam...inch.well.)

model <- lm(data=costs, formula="Total.costs....US...well. ~ Depth...m.well. * Yield..m3.hour..")

summary(model)

fun = function(x, y){
model$coefficients[2] * x + model$coefficients[3] * y + model$coefficients[1] + x*y*model$coefficients[4]
}

library(rgl)

persp3d(fun, 
        xlim = c(10, 50), ylim = c(1/1000, 10/1000))

