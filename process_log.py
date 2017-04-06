# -*- coding: utf-8 -*-
# --------------------------------------------DESCRIPTION --------------------------------------------------------- #
# This file implements the main function to process log file,log.txt to get the first 3 features:
# 1. List in descending order the top 10 most active hosts/IP addresses that have accessed the site.-->hosts.txt
# 2. Identify the top 10 resources(descending order) on the site that consume the most bandwidth. -->resources.txt
# 3. List in descending order the site’s 10 most frequently visited 60-minute period. -->hours.txt
# Suppost the log.txt was written in the time order.
# ------------------------------------------------------- --------------------------------------------------------- #
from model import parse,parse_req,top_k 
import io
import os
# the files to save all the results
# dir = os.path.dirname(__file__)
tempdir = os.getcwd()
basedir = os.path.join(tempdir,'../../')
hostfile = os.path.join(basedir,'log_output/hosts.txt')
resfile = os.path.join(basedir,'log_output/resources.txt')
hourfile = os.path.join(basedir,'log_output/hours.txt')
lfile = os.path.join(basedir,'log_input/log.txt')

#-------------PROCEDURE-------------------#
#Analyze features 1 and 2 at the same time

host_count = {}               # a dictionary with hostname as the key and frequences of visit as the value
res_band = {}                 # a dictionary with resource as the key and the bandwidth as the value
with io.open(lfile,'r',encoding="latin-1") as logfile:
    for line in logfile:
        host,request,byte = parse(line,"host","request","rbyte")
        if host in host_count:
            host_count[host] += 1
        else:
            host_count[host] = 1
            
        res = parse_req(request)
        if res in res_band:
            res_band[res] += byte
        else:
            res_band[res] = byte 

        
hosts = top_k(host_count)
f = io.open(hostfile,'w')
for host in hosts:
  line = host[1]+","+str(host[0])+'\n'
  f.write(line)
f.close()
resources = top_k(res_band)
f = io.open(resfile,'w')
for res in resources:
  line = res[1] + '\n'
  f.write(line)
f.close()

#--------------------------PROCEDURE----------------#
# Analyze the feature 3 
import datetime
time_count = []                       # a list with visit time as the first and frequences within certain time window as the second
format = '%d/%b/%Y:%H:%M:%S'          # define the format to assign the timestamp to a datatime object
before = datetime.datetime.now()
with io.open(lfile,'r',encoding="latin-1") as logfile:
    for line in logfile:
        host,time,code = parse(line,"host","time","rcode")

        t = datetime.datetime.strptime(time[:-6],format)
        if t != before:
          time_count.append([t,1])
          before = t
        else:
          time_count[-1][1] += 1

#count frequences for each entry time within 60mins time window
P = datetime.timedelta(minutes=60)    # the time window for 60mins for counting frequences
K = 10
sum = 0
j = 1
for i in range(0,len(time_count)):
    c = time_count[i][1]
    while j < len(time_count) and time_count[j][0] - time_count[i][0] <= P:
        time_count[i][1] += sum + time_count[j][1]
        j += 1
    sum = time_count[i][1] - c

# sort the outer list based on the second item of inner list by descending order
# choose the top 10 from the beginning and ingore all the ones afterwards with time overlap
from operator import itemgetter
time_count = sorted (time_count,key=itemgetter(1),reverse=True)
hours = [time_count[0]]
for x in time_count:
  if len(hours) < K:
    if x[0] - hours[-1][0] > P:
      hours.append(x)

f = io.open(hourfile,'w')
for hour in hours:
  time = datetime.datetime.strftime(hour[0],format)
  line = time + " -0400, "+str(hour[1]) + '\n'
  f.write(line)

f.close()
