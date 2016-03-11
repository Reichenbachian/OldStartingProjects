import requests
import urllib2
import socket
import timeit
import sys

proxyList=[]
time=[]
timeout=0
# proxyNovacom=requests.get('http://www.proxynova.com/proxy-server-list/country-us/')

def getUSProxyOrg():
	usproxyorg=requests.get('https://www.us-proxy.org/')
	usproxyorg=usproxyorg.text.split("<tbody>")[1].split("</tbody>")[0].replace("<td>","\n").replace("</td>","").replace("<tr>","").replace("</tr>","").split("\n\n")
	for proxy in usproxyorg:
		info=proxy.split("\n")
		ipLine=0
		if info[0]=="":
			ipLine=ipLine+1
		proxyList.append(""+info[ipLine]+":"+info[ipLine+1])


def check_proxy(proxy):
	try:
		proxy = urllib2.ProxyHandler({'http': "http://" + str(proxy)})
		opener = urllib2.build_opener(proxy)
		urllib2.install_opener(opener)
		urllib2.urlopen('http://www.google.com', timeout=timeout)
		print "\tAlive"
	except(IOError), msg:
		print "\t[-] Dead: ", msg

def checkProxies():
	for proxy in proxyList:
		if proxy != "" or proxy != "\n":
			print "##### Testing: ", proxy
			startTime = timeit.default_timer()
			check_proxy(proxy)
			endTime = timeit.default_timer()
			print "Response time: " + str(endTime-startTime)
			time.append(endTime-startTime)

def printFastest():
	index=0
	fastestTime=time[0]
	for i in range(0,len(time)):
		if fastestTime > time[i]:
			index=i
	return index


def printFastest3():
	print ""
	print "-------------------------------------------------------"
	print ""
	for i in range(0,3):
		index=printFastest();
		print("Fastest proxy is " + str(proxyList[index]) + " with response time of " + str(time[index]) + "!")
		proxyList.pop(index)
		time.pop(index)

def main():
	global timeout
	sys.stdout.write("Set the timeout: ")
	timeout=float(raw_input())
	getUSProxyOrg()
	checkProxies()
	printFastest3()

if __name__ == '__main__':
	main()