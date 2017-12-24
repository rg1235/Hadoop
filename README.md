# Implementation of K means clustering
Implementation of K means clustering algorithm is done using MapReduce paradigm on Hadoop.The mapper and reducer programs have bee written in Python.
Hadoop streaming is used to run the mapper reducer code written in Python.
1.py is used as the driver program because while implementing K means using mapreduce we need to run the mapper and reducer program many times until the centroids stop getting changed.
