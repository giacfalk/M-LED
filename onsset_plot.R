library(tidyverse)
library(ggplot2)

residential<-read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/onsset/results/ke-1-0_0_0_0_0_0_summary.csv') %>% mutate(Scenario="Residential")
  
all<-read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/Repo/onsset/results/ke-1-0_1_0_0_1_0_summary.csv') %>% mutate(Scenario="All")

scenarios <- rbind(residential, all)

capacity <- scenarios %>% filter(str_detect(X, "Capacity"))
investment <- scenarios %>% filter(str_detect(X, "Investment"))
connections <- scenarios %>% filter(str_detect(X, "Connections"))

capacity$X=gsub("3.Capacity_", "", capacity$X)
investment$X=gsub("4.Investment_", "", investment$X)
connections$X=gsub("2.New_Connections_", "", connections$X)

a<-ggplot(capacity, aes(x=Scenario, y=(X2025+X2030)/1000000, group=X, fill=X))+
  geom_col()+
  ylab("Capacity (GW)")+
  xlab("")+
  theme(legend.position = "bottom", legend.direction = "horizontal")+
  scale_fill_discrete(name="Tech.")

b<-ggplot(investment, aes(x=Scenario, y=(X2025+X2030)/1000000000, group=X, fill=X))+
  geom_col()+
  ylab("Investment (bn.)")+
  xlab("")+
  theme(legend.position = "none")

c<-ggplot(connections, aes(x=Scenario, y=(X2025+X2030)/1000000, group=X, fill=X))+
  geom_col()+
  ylab("New connections (million)")+
  xlab("")+
  theme(legend.position = "none")

ggsave("supply_analysis.png", cowplot::plot_grid(cowplot::plot_grid(a + theme(legend.position = "none"), b, c, nrow = 1, labels = "AUTO"), cowplot::get_legend(a), ncol = 1, rel_heights = c(1, 0.15)), device = "png", scale=1.2)
