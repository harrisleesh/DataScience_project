import numpy as np
import math
import sys


# make read lines to list
def attrList(line):
    temp = line.split("\n")
    del temp[-1]
    attr_list = temp[0].split("\t")
    attr_list[0] = int(attr_list[0])
    attr_list[1] = float(attr_list[1])
    attr_list[2] = float(attr_list[2])
    attr_list.append(-1)
    return attr_list



# calculate distance between two points
def dist(a, b):
    return math.sqrt((a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2]))

def eps_neighbors(a, b, eps):
    return dist(a, b) < eps

# region Query function returns neighbor points which is inside of epsilon
def regionQuery(D, seed, eps):
    seeds = []
    for i in D:
        if eps_neighbors(seed, i, eps):
            seeds.append(i[0])
    return seeds

#main DBSCAN function
def db_scan(D, eps, Minpts):
    C = 0
    for seed in D:
        if seed[-1] == -1:                              # if the last element of list is -1, it means unvisited
            seed[-1] = C                                # if unvisited, change the value as cluster number
            NeighborPts = regionQuery(D, seed, eps)
            if len(NeighborPts) < Minpts:               # len < Minpts means outlier
                seed[-1] = -2
            else:                                       # expand function
                expandCluster(D, seed, NeighborPts, C, eps, Minpts)
                C = C + 1                               #Cluster number increases
    return C

#expand cluster function
def expandCluster(D, seed, NeighborPts, C, eps, Minpts):
    cluster = []
    for next_seed in NeighborPts:                               # from all data points in Neighbor Points, expand cluster
        if D[next_seed][-1] == -1:
            D[next_seed][-1] = C
            next_NeighborPts = regionQuery(D, D[next_seed], eps)
            if len(next_NeighborPts)>=Minpts:
                for i in next_NeighborPts:
                    if NeighborPts.count(i)==0:
                        NeighborPts.append(i)



# store commandline argument in each variables
input_filename = sys.argv[1]
clustering_number=int(sys.argv[2])
Eps = float(sys.argv[3])
MinPts = float(sys.argv[4])


data = open( input_filename , "r")
dataSet = []

# read data at dataSet
read = data.readlines()
for i in read:
    dataSet.append(attrList(i))


# db_scan function return number of clusters and this function change the last value of each line as cluster number
numOfclusters = db_scan(dataSet, Eps , MinPts )

# cluster maintain each cluster and its elements
cluster = []
for i in range(0,numOfclusters):
    cluster.append([])

for i in dataSet:
    if(i[-1]!=-2):
        cluster[i[-1]].append(i[0])

# sort cluster as the number of cluster elements descending order
for i in range(0,numOfclusters):
    cluster[i].insert(0,len(cluster[i]))

cluster.sort()
cluster.reverse()

for i in range(0,numOfclusters):
    cluster[i].reverse()
    cluster[i].pop()
    cluster[i].reverse()


# adjust output file format
for i in range(0,clustering_number):
    nameOfcluster = "input"+input_filename[5]+"_cluster_"+str(i)+".txt"
    file = open(nameOfcluster,"w")
    for j in cluster[i]:
        file.write(str(j))
        file.write("\n")
    file.close()
data.close()
