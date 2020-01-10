import numpy as np
from scipy.stats import norm
from sklearn.cluster import KMeans

'''
create a dictionary with key representing crop name and value being a list of lists [id,x,y,mean_eta] 
'''
def create_crop_xy_dict(allFields):
    crops = {}
    for f in allFields:
        centroid = f.get_centroid()
        f.set_mean()
        if f.crop not in crops:
            crops[f.crop] = []
        crops[f.crop].append([f.id, centroid[0], centroid[1], f.mean])
    return crops

'''
Given a dictionary (key: crop, value: list of [id, x,y,avg_eta]), crop name, number of clusters
it runs the kmeans clutering algorithm for a given crop and returns a list if labels indicating the cluster id
and a list of [id, x,y,avg_eta]
'''
def cluster_by_crop(crops, crop, nclusters):
    xyeta = crops[crop]
    vec = np.zeros(shape=(len(xyeta),2))
    for i, v in enumerate(xyeta):
        vec[i] = v[1:3]
    kmeans = KMeans(n_clusters=nclusters).fit(vec)
    return kmeans.labels_, xyeta

'''
Pick k for every crop based on the SSE plots
Right now, I'm hard coding the number of clusters by looking at the plots 
For the crop that I haven't analyzed yet, number of clusters is 2
TODO: come up with some math to see how SSE changes and pick the k
'''
def createnclusters():
    nclusters = dict()
    nclusters["Grapes"] = 4
    nclusters["Citrus"] = 3
    nclusters["Idle"] = 2
    nclusters["Tomatoes"] = 4
    nclusters["Pistachios"] = 2
    nclusters["Almonds"] = 2
    nclusters["Wheat"] = 2
    nclusters["Cherries"] = 2
    nclusters["Cotton"] = 2
    nclusters["Flowers, Nursery and Christmas Tree Farms"] = 5
    nclusters["Miscellaneous Deciduous"] = 3
    nclusters["Alfalfa and Alfalfa Mixtures"] = 7
    nclusters["Onions and Garlic"] = 3
    nclusters["Miscellaneous Truck Crops"] = 4
    nclusters["Miscellaneous Grain and Hay"] = 3
    nclusters["Bush Berries"] = 3
    nclusters["Walnuts"] = 5
    nclusters["Carrots"] = 2
    nclusters["Corn, Sorghum and Sudan"] = 2
    nclusters["Urban"] = 2
    nclusters["Young Perennials"] = 2
    nclusters["Pomegranates"] = 2
    nclusters["Kiwis"] = 1
    nclusters["Melons, Squash and Cucumbers"] = 3
    nclusters["Peppers"] = 2
    nclusters["Cole Crops"] = 1
    return nclusters

'''
Given list of labels returned from kmeans and the list of [id, x,y,eta]
it computes the mean and standard deviation for every cluster 
and returns a list of tupels (mean, std) for clusters related to a specific crop
'''
def compute_cluster_stats(labels, xyeta):
    cluster_eta = dict()
    cluster_stats = []
    for i,label in enumerate(labels):
        if label not in cluster_eta:
            cluster_eta[label] = []
        single_xyeta = xyeta[i]
        cluster_eta[label].append(single_xyeta[3])
    for cluster, eta in cluster_eta.items():
        mean = np.mean(eta)
        std = np.std(eta)
        cluster_stats.append((mean, std))
    return cluster_stats

'''
run the clustering all at once on all the crops with different k values
return a dictionary, key is field id and value is 0 or 1 to indicate if the field's 
water use is efficiency or not
'''
def clustering(crop_xy_dict, nclusters):
    field_efficiency = dict()
    for crop, xy in crop_xy_dict.items():
        labels, xyetas = cluster_by_crop(crop_xy_dict, crop, nclusters[crop])
        cluster_stats = compute_cluster_stats(labels, xyetas)
        for i, label in enumerate(labels):
            id = xyetas[i][0]
            if xyetas[i][3] <= cluster_stats[label][0]-2*cluster_stats[label][1] or xyetas[i][3] >= cluster_stats[label][0]+2*cluster_stats[label][1]:
                field_efficiency[id] = 0
            else:
                field_efficiency[id] = 1
    return field_efficiency

'''
Run the clustring algorithm and set the efficiency
'''
def alg(allFields):
    crop_xy_dict = create_crop_xy_dict(allFields) 
    nclusters = createnclusters()
    for f in allFields:
        if f.crop not in nclusters:
            nclusters[f.crop] = 2
    result = clustering(crop_xy_dict, nclusters)
    for field in allFields:
        field.set_efficiency(result[field.id])


# def alg_stub(allFields):
#     for field in allFields:
#         field.set_efficiency(1)
