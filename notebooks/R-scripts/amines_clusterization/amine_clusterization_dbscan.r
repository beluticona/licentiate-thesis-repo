library(FactoMineR)
library(factoextra)
library('dendextend')

setwd('/home/belu/VS Workplace/licentiate-thesis-repo/notebooks/R-scripts/')

amines <- read.csv('amines_clusterization/amines_fchem_properties.csv', header=TRUE)

distance.dice <- read.csv('amines_clusterization/similarity_tanimoto.csv', header=TRUE)
                   
#res.pca <- PCA(amines, ncp = 3, graph = FALSE)

hc1 <- hclust(dist(amines, method = 'canberra'), method='centroid')
hc2 <- hclust(dist(distance.dice, method = 'canberra'), method='centroid')

dend1 <- as.dendrogram(hc1)
dend2 <- as.dendrogram(hc2)

cutree(dend1, h = 150)


#dend_diff(dend1, dend2)

dl <- dendlist(dend1, dend2)
tanglegram(dl, sort = TRUE, common_subtrees_color_lines = FALSE, highlight_distinct_edges  = FALSE, highlight_branches_lwd = FALSE)

#res.hcpc <- HCPC(res.pca, graph = TRUE)

#fviz_cluster(res.hcpc, geom = "point", main = "")

#plot(res.hcpc, choice = "3D.map")



