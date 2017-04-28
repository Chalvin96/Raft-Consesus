import time
import urllib
import urllib2

INTERVAL = 0.1

PORT = 13337

nodeURL = ['http://localhost:13337']

def getTimeList():
    """
    Fetches a list of time units the cpu has spent in various modes
    Detailed explanation at http://www.linuxhowtos.org/System/procstat.htm
    """
    cpuStats = file("/proc/stat", "r").readline()
    columns = cpuStats.replace("cpu", "").split(" ")
    return map(int, filter(None, columns))

def deltaTime(interval):
    """
    Returns the difference of the cpu statistics returned by getTimeList
    that occurred in the given time delta
    """
    timeList1 = getTimeList()
    time.sleep(interval)
    timeList2 = getTimeList()
    return [(t2-t1) for t1, t2 in zip(timeList1, timeList2)]

def getCpuLoad():
    """
    Returns the cpu load as a value from the interval [0.0, 1.0]
    """
    dt = list(deltaTime(INTERVAL))
    idle_time = float(dt[3])
    total_time = sum(dt)
    load = 1-(idle_time/total_time)
    return load


while True:
    print "CPU usage=%.2f%%" % (getCpuLoad()*100.0)
    time.sleep(0.1)
    for x in nodeURL:
		url = x
		json_obj = {'ip': 'localhost',
					'loadCPU': getCpuLoad(),
					'port': PORT}
		data = urllib.urlencode(json_obj)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
    

