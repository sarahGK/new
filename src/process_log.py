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
import sys

script,lfile,hostfile,hourfile,resfile,blockfile = sys.argv
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
f = open(hostfile,'w')
for host in hosts:
  line = host[1]+","+str(host[0])+'\n'
  f.write(line)
f.close()
resources = top_k(res_band)
f = open(resfile,'w')
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

f = open(hourfile,'w')
for hour in hours:
  time = datetime.datetime.strftime(hour[0],format)
  line = time + " -0400, "+str(hour[1]) + '\n'
  f.write(line)

f.close()

# ------------------------------------------------DESCRIPTION --------------------------------------------------------- #
# This file implements the main function to process log file,log.txt to get the 4th feature: 
# 4. Detect patterns of three consecutive failed login attempts over 20 seconds and save blocked record. --> blocked.txt
# Suppost the log.txt was written in the time order.
# ----------------------------------------------------------------------------------------------------------------- #


f = open(blockfile,'w')

format = '%d/%b/%Y:%H:%M:%S'
CP =  datetime.timedelta(seconds=20)  # check period of 20seconds for 3 consective login failure
BP =  datetime.timedelta(minutes=5)   # block period of 5mins for identified host
phost_time = {}                       # dictionary with login failure hostname as key and a list(with length of 2)as values
bhost_start = {}                      # dictionary with blocked hostname as key and starting time as value 
current = datetime.datetime.now()
with io.open(lfile,'r',encoding="latin-1") as file:
    for line in file:
        host,time,code = parse(line,"host","time","rcode")
        current = datetime.datetime.strptime(time[:-6],format)
        if host in bhost_start:
            if current - bhost_start[host] <= BP:
                f.write(line)
            else:
                bhost_start.pop(host,None)
        else:
            login = False if int(code) == 401 else True
            if login: # login success
                if host in phost_time:
                    phost_time.pop(host,None)
            else: # login failure
                if host in phost_time:
                    if current - phost_time[host][0] <= CP:
                        if len(phost_time[host]) == 2:
                            bhost_start[host] = current
                            phost_time.pop(host,None)
                        else:
                            phost_time[host].append(current)
                    elif len(phost_time[host]) == 2 and current - phost_time[host][1] <= CP:
                        phost_time[host][0] = phost_time[host][1]
                        phost_time[host][1] = current
                    else:
                        phost_time[host] = [current]
                else:
                    phost_time[host] = [current]


f.close()

