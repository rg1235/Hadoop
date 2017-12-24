#!/usr/bin/python

import sys, re, math

CLUSTERS_FILENAME = 'clusters.txt'
INPUT_FILENAME = 'input.txt'
clusters = [('0', 11.436440678, 20.198305084699999), ('1', 5.5831521739100003, 17.997826087), ('2', 6.3966292134799998, 24.442134831499999)]
delta_clusters = dict()

def read_from_clusters_cache_file(clusters_file):
    f = open(clusters_file, 'r')
    data = f.read()
    f.close()
    del f
    return data
def read_from_input_cache_file(input_file):
    f = open(input_file, 'r')
    data1 = f.read()
    f.close()
    del f
    return data1

def read_clusters():
    #cluster_data = read_from_clusters_cache_file(CLUSTERS_FILENAME)
        delta_clusters['0'] = (0, 0, 0)
        delta_clusters['1']=(0,0,0)
        delta_clusters['2']=(0,0,0)

def get_distance_coords(lat1, long1, lat2, long2):
	#Calculate euclidian distance between two coordinates
    dist = math.sqrt(math.pow(lat1 - lat2,2) + math.pow(long1 - long2,2))
    return dist

def get_nearest_cluster(latitude, longitude):
    nearest_cluster_id = None
    nearest_distance = 1000000000
    for cluster in clusters:
        dist = get_distance_coords(latitude, longitude, cluster[1], cluster[2])
        if dist < nearest_distance:
            nearest_cluster_id = cluster[0]
            nearest_distance = dist
    return nearest_cluster_id


read_clusters()

regexWords = re.compile("\s+")

#input_data = read_from_input_cache_file(INPUT_FILENAME)
for line in sys.stdin:
  words = line.strip().split()
  if words == None or len(words) != 3:
        print "ERROR PARSING LINE (Columns: "+str(len(words))+") - ",line
        continue
  else:
    latitude, longitude, pt = words
    latn = float(latitude)
    longn = float(longitude)
    nearest_cluster_id = get_nearest_cluster(latn, longn)
    sumy, sumx, cont = delta_clusters[nearest_cluster_id]
    delta_clusters[nearest_cluster_id] = (sumy+latn, sumx+longn, cont+1)
    print nearest_cluster_id + "\t" + str(latn)+";"+str(longn)


