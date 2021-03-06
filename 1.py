#!/usr/bin/env python

import sys
import fileinput
import os
import math

clusters=[]
temp=[]
cluster=""
c2=""
#bashCommand = "extract commands"
#os.system(bashCommand)
#command to copy "hadoop dfs -copyToLocal kmeans/input.txt hi"
def fileread():
   global clusters
   global temp
   global cluster
   h=open("mapper.py",'r')
   i=1
   for line in h:
    if i==7:
     cluster=line.strip()
    i=i+1 
   h.close()
   print "fierst cluster iscluster" + cluster
def fileread2():
   global clusters
   global temp
   global c2
   h=open("prac.py",'r')
   i=1
   for line in h:
    if i==7:
     c2=line.strip()
    i=i+1 
   h.close()
   print "second cluster iscluster" + c2

def fileread3():
   global clusters
   global temp
   global c2
   h=open("kmeanfile/part-00000",'r')
   j=open("output1.dat",'w')
   k=open("output2.dat",'w')
   w=open("output3.dat",'w')
   i=1
   for line in h:
     line=line.strip().split("\t")
     if line[0]=='0':
       q=line[1].strip().split(";")
       j.write(q[0]+"\t"+q[1]+"\n")
     if line[0]=='1':
       q=line[1].strip().split(";")
       k.write(q[0]+"\t"+q[1]+"\n") 
     if  line[0]=='2':
       q=line[1].strip().split(";")
       w.write(q[0]+"\t"+q[1]+"\n")
   h.close()
   w.close()
   k.close()
   j.close()  
   

def finddist(j):
  global clusters
  global temp
  print clusters[j][1]
  print temp[j][1]
  dist=((clusters[j][1]-temp[j][1])*(clusters[j][1]-temp[j][1]))+((clusters[j][2]-temp[j][2])*(clusters[j][2]-temp[j][2]))
  dist1=math.sqrt(dist)
  if dist1>0.05:
   return 1
  return 0 
 
def main():
   global clusters
   global temp
   global cluster
   global c2
   flag=1
   n=open("clusters.txt",'r')
   for line in n:
     l=line.strip().split("\t")
     centroids, coords=l
     z, w=coords.strip().split(";")
     x=float(z)
     y=float(w)
     clusters.append((centroids, x, y))
   n.close()
   temp=clusters[:]
   b="""hadoop fs -rm -r input
      hadoop fs -mkdir input
      hadoop fs -put input.txt input"""
   os.system(b)   
   while flag==1:
    fileread()
    bashCommand = """hadoop fs -rm -r output
                 hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py -input input -output output
                 hadoop dfs -copyToLocal output/part-00000 clusterfile"""
    os.system(bashCommand)
    filename="mapper.py"
    f=open(filename,'r')
    if len(temp)>0:
     del temp[:]
    temp=clusters[:]
    del clusters[:]
    g=open("clusterfile/part-00000",'r') 
    for line in g:
     l=line.strip().split("\t")
     centroids, coords=l
     z, w=coords.strip().split(";")
     x=float(z)
     y=float(w)
     clusters.append((centroids, x, y))
    g.close()
    b="""rm -f clusterfile/part-00000"""
    os.system(b)
    
    p="clusters = "+str(clusters)
    print "p is"+p
    l=0
    s=0
    while l<len(clusters):
       print clusters
       print temp
       v=finddist(l)
       if(v==1):
         s=1
       l=l+1
    if s==1:
       for lines in fileinput.input(filename, inplace=True): 
         print lines.rstrip().replace(cluster,p)
    else:
       print "hi"
       flag=0
    
    f.close()
   fileread()
   fileread2()
   filename2="prac.py"
   for lines in fileinput.input(filename2, inplace=True): 
         print lines.rstrip().replace(c2,cluster)
   b="""hadoop fs -rm -r output
        hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar -D mapred.map.tasks=4 -D mapred.reduce.tasks=1 -mapper prac.py -reducer new.py -file prac.py -file new.py -input input -output output
        hadoop dfs -copyToLocal output/part-00000 kmeanfile"""
   os.system(b)
   fileread3()
   c="gnuplot -e \"plot 'output1.dat','output2.dat','output3.dat'; pause -1\""
   os.system(c)
if __name__ == '__main__':
  main()
