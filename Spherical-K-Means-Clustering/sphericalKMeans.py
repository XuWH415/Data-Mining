import copy
import random
import math
from sklearn.metrics import pairwise
from numpy.linalg import norm
import numpy

def getLabels(dataset, centroids):
    len_dataset = len(dataset)
    len_centroids = len(centroids)
    labels = [0] * len_dataset
    score = 0.0
    
    cosine_similarity = pairwise.cosine_similarity(dataset, centroids)
    for i in range(len(cosine_similarity)):
        m = max(cosine_similarity[i])
        score += m
        labels[i] = numpy.argmax(cosine_similarity[i])
    
    return labels, score
            
def recalculateCentroids(dataset, labels, k):
    centroids = []
    len_line = len(dataset[0])
    for i in range(k):
        centroid = [0] * len_line
            
        for j in range(len(labels)):
            if i == labels[j]:
                for k in range(len_line):
                    centroid[k] = centroid[k] + dataset[j][k]
                    
#         norm = getNorm(centroid)
        n = float(norm(centroid))
        if n != 0:
            for m in range(len_line):
                centroid[m] = float(centroid[m]) / n
        else:
            l_c = math.sqrt(len_line)
            for m in range(len_line):
                centroid[m] = 1.0 / l_c
        centroids.append(copy.deepcopy(centroid))
    
    return centroids


class SphericalKMeans:
    def __init__(self, n_clusters = 8, n_init = 10, max_iter = 300, tol = 0.001):
        self.n_clusters = n_clusters
        self.n_init = n_init
        self.max_iter = max_iter
        self.tol = tol
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        
    def fit(self, dataset):    
        temp_dataset = copy.deepcopy(dataset)
        len_line = len(temp_dataset[0])
        for i in range(len(temp_dataset)):
#             norm = getNorm(temp_dataset[i])
            n = float(norm(temp_dataset[i]))
            if n != 0:
                for j in range(len_line):
                    temp_dataset[i][j] = float(temp_dataset[i][j]) / n
            else:
                l_t = math.sqrt(len_line)
                for j in range(len_line):
                    temp_dataset[i][j] = 1.0 / l_t
                    
                    
        self.inertia_ = 0.0
        self.cluster_centers_ = []
        self.labels_ = []
        
        for i in range(self.n_init):
            cluster_centers_ = random.sample(temp_dataset, self.n_clusters)
            labels_ = []
            inertia_ = 0.0
            lastscore = 0.0
            
            for j in range(self.max_iter):
                lastscore = inertia_
                labels_, inertia_ = getLabels(temp_dataset, cluster_centers_)
                cluster_centers_ = recalculateCentroids(temp_dataset, labels_, len(cluster_centers_))
                if (float(inertia_ - lastscore) / inertia_) <= self.tol:
                    break
            
            if inertia_ > self.inertia_:
                self.cluster_centers_ = copy.deepcopy(cluster_centers_)
                self.labels_ = copy.deepcopy(labels_)
                self.inertia_ = inertia_
            
        return self.cluster_centers_, self.labels_, self.inertia_


        