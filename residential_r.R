library(tidyverse)

y = read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_train.csv')

y['acc_pop_share_t1'] = y['acc_pop_t1'] / (y['acc_pop_t1'] + y['acc_pop_t2'] + y['acc_pop_t3'] + y['acc_pop_t4'])
y['acc_pop_share_t2'] = y['acc_pop_t2'] / (y['acc_pop_t1'] + y['acc_pop_t2'] + y['acc_pop_t3'] + y['acc_pop_t4'])
y['acc_pop_share_t3'] = y['acc_pop_t3'] / (y['acc_pop_t1'] + y['acc_pop_t2'] + y['acc_pop_t3'] + y['acc_pop_t4'])
y['acc_pop_share_t4'] = y['acc_pop_t4'] / (y['acc_pop_t1'] + y['acc_pop_t2'] + y['acc_pop_t3'] + y['acc_pop_t4'])

y = y %>% dplyr::select('acc_pop_share_t1', 'acc_pop_share_t2', 'acc_pop_share_t3', 'acc_pop_share_t4', 'HCWIXQPLOW', 'HCWIXQP2ND', 'HCWIXQPMID', 'HCWIXQP4TH', 'HCWIXQPHGH', 'popdens', 'isurbanmaj', 'ISO') %>% as.data.frame()

y2 = y[complete.cases(y), ]


# Partition data
splitSample <- sample(1:2, size=nrow(y2), prob=c(0.8,0.2), replace = TRUE)
train.hex <- y2[splitSample==1,]
test.hex <- y2[splitSample==2,]

library(randomForestSRC)
pr = rfsrc(Multivar(acc_pop_share_t1, acc_pop_share_t2, acc_pop_share_t3, acc_pop_share_t4)~.,data = train.hex, importance=T)

print(pr)

prediction <- predict.rfsrc(pr, test.hex)

##########
clusters = read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_predict.csv')

clusters$popdens = clusters$popsum/clusters$Area
clusters$ISO = as.factor("KE")
clusters = clusters %>% dplyr::select('HCWIXQPLOW', 'HCWIXQP2ND', 'HCWIXQPMID', 'HCWIXQP4TH', 'HCWIXQPHGH', 'popdens', 'id', 'ISO', 'isurbanmajority') %>% as.data.frame()

clusters$isurbanmaj <- clusters$isurbanmajority

# 
clusters =clusters[complete.cases(clusters), ]

#########
prediction <- predict.rfsrc(pr, clusters)
clusters$acc_pop_share_t1_new = prediction$regrOutput$acc_pop_share_t1$predicted
clusters$acc_pop_share_t2_new = prediction$regrOutput$acc_pop_share_t2$predicted
clusters$acc_pop_share_t3_new = prediction$regrOutput$acc_pop_share_t3$predicted
clusters$acc_pop_share_t4_new = prediction$regrOutput$acc_pop_share_t4$predicted

clusters = clusters %>% dplyr::select(-HCWIXQPLOW, -HCWIXQP2ND, -HCWIXQPMID, -HCWIXQP4TH, -HCWIXQPHGH) %>% as.data.frame()

clusters$id = as.character(clusters$id)

clusters2 = read.csv('D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_predict.csv')

clusters2$id = as.character(clusters2$id)

clusters2 = merge(clusters, clusters2, by="id")

#
clusters2$id = as.character(clusters2$id)

write.csv(clusters2, 'D:/OneDrive - FONDAZIONE ENI ENRICO MATTEI/Current papers/Prod_Uses_Agriculture/PrElGen_database/processed_folder/clusters_predict.csv')
