# --------------------------------------------DESCRIPTION ------------------------------------------------------- #
# This file define helper functions for processing logfile data, which includes:
# A parse function to parse each line of log file,log.txt mainly using re module.
# A top_n function to return a list of features with top k most values using heapq module for heap data structure.
# ---------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------------- #
# The parse function will parse each line of log file,log.txt mainly using re module.                               #
# Suppost one empty space is used to separate different feature in each line.                                       #
# Input: line, one line from log file and *args, the feature/features from the line.                                #
# The valid options for *args:"host","time","request","rcode" and "rbyte".                                          #
# Output: hostname/IP address,timestamp,resource from request,http reply code and bytes in reply according to *args.#
# ------------------------------------------------------- --------------------------------------------------------- #
import re
pattern = re.compile('^(?P<host>\S+) \S+ \S+ \[(?P<time>\S+ [-+]\d+)\] "(?P<request>.*)" (?P<rcode>\S+) (?P<rbyte>\S+)$')
def parse(line,*args):
    m = pattern.match(line)
    if not m:
        print("Unknown log format at:",line)
        return
    dict = m.groupdict()
    if dict['rbyte'] == '-':
        dict['rbyte'] = 0
    else:
        dict['rbyte'] = int(dict['rbyte'])
    if not args:
      return dict
    try:
      if len(args) ==1:
        return dict[args[0]]
      return [dict[key] for key in args]
    except KeyError:
      print("Invalid features provided in arguments:",args)


#--------------------------------------------------------------------------------------------#
# The parse_res function with parse the resource from the request which is inconsistent.     #
# Suppose the requests in double quotes have following format:                               #
# 1. Starting with GET/POST/HEAD and ending with HTTP,then the rest will be the resource.#
# 2. Only have one starting or ending, then the rest will be the resource.                   #
# 3  Neither starting nor ending exists, the request will be the resource                    #
#--------------------------------------------------------------------------------------------#
def parse_req(request):
    r1 = re.search('^GET|POST|HEAD',request)
    r2 = re.search('HTTP\S*',request)
    if r1 is not None and r2 is not None:
      return request[r1.span()[1]+1:r2.span()[0]-1]
    elif r1 is not None:
      return request[r1.span()[1]+1:]
    elif r2 is not None:
      return request[:r2.span()[0]-1]
    else:
      return request
      

# --------------------------------------------------------------------------------------------------------------- #
# The top_k function will list the top k features in descending order.                                            #
# Input: dictionary with feature as the key and the matric used for comparison as the value and k(10 as default). #
# Output: a list of pairs with value of matric as the first and feature as the second element.                    #
# It uses min heap data structure to keep track of the top k features                                             #
# For dictionary of size n, the time complexity is O(nlogk+klogk) and space complixity is O(K)                    #
# For k far less than n, it's an optimal method for time complexity.                                              #
# --------------------------------------------------------------------------------------------------------------- #
import heapq as h
def top_k(dict,k=10):
    hq = []
    for key, value in dict.items():
        if len(hq) < k:
            h.heappush(hq,[value,key])
        else:
            if (value>hq[0][0]):
                h.heappop(hq)
                h.heappush(hq,[value,key])
    return h.nlargest(k,hq) 

'''
from pprint import pprint
if __name__ == '__main__':
    line = 'unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] "GET /shuttle/countdown/ HTTP/1.0" 200 3985'
    pprint(parse(line))
    pprint(parse(line,"host"))
    line = '199.242.69.123 - - [14/Jul/1995:10:24:29 -0400] "GET /pub/] HTTP/1.0" 404 -'
    args = ("host","request")
    pprint(parse(line,"host","request"))
'''
