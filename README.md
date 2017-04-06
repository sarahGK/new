# Challenge Summary

- a large amount of Internet traffic data (log.txt - 446.5MB) with each line of :
    1. host: hostname/IP address
    2. timestamp : [DD/MON/YYYY:HH:MM:SS -0400]
    3. request: in quotes
    4. HTTP reply code
    5. bytes in the reply,with '-' means 0 bytes
- Challenges: perform basic analytics, provide useful metrics, and implement basic security measures.
    1. List in descending order the top 10 most active hosts/IP addresses that have accessed the site.-->hosts.txt
    2. Identify the top 10 resources(descending order) on the site that consume the most bandwidth. -->resources.txt
    3. List in descending order the site’s 10 most frequently visited 60-minute period. -->hours.txt
    4. Detect patterns of three consecutive failed login attempts over 20 seconds and each attempt that would have                      been blocked should be written to a log file. --> blocked.txt
# Implement
### Feature 1 & 2: 
List the top 10 most active host/IP addresses that have accessed the site.
Suppose the data can be loaded into memory.
1.Read through the data, for each host/IP address get the frequencies and for each resource get the total bandwidth during the period of the log file.
2.Then using min heap data structure to track the top 10 most active host or resources with most bandwidth.
If the data is beyond the capacity then use database to do aggregation on host/resource collumn.

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods.
Suppose the log file was written in time order.
1. Read through the data, for each recorded time count number of visit.
2. For each time, count the frequences within 60mins window.
3. Sort all the recorded times descendingly by the frequences.
4. Starting from the beginning of the sorted times, choose 10 times without time overlap. 

This way I think is better to show the most busiest periods of the server compared with the way showed in the results of test cases, which have time overlap and the starting time only 1 second apart.

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

This should be done in really time. Use two dictionaries to keep track the failure logins and the hosts should be blocked and the starting time.

For this case, since only need to detect 3 consective failures, I use a list to track all the failure times. While the best I think should use FIFO  queue for scalibity.


### Other considerations and optional features:
I coded in python3 and using modules re for parsing each line, queue for min heap data structure, datetime for the time data, and operator for sorting a list of lists.
The file hosts.txt,resources.txt,hours.txt and blocked.txt are the results of analyzing the big log.txt file from the link.


