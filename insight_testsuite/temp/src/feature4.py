# ------------------------------------------------DESCRIPTION --------------------------------------------------------- #
# This file implements the main function to process log file,log.txt to get the 4th feature: 
# 4. Detect patterns of three consecutive failed login attempts over 20 seconds and save blocked record. --> blocked.txt
# Suppost the log.txt was written in the time order.
# ----------------------------------------------------------------------------------------------------------------- #

# -*- coding: utf-8 -*-

from model import parse
import io
import os
import datetime

tempdir = os.getcwd()
basedir = os.path.join(tempdir,'../../')
blockfile = os.path.join(basedir,'log_output/blocked.txt')
lfile = os.path.join(basedir,'log_input/log.txt')

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
