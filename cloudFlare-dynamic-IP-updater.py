'''
Updates Cloudflare load balancing origin when dynamic IP changes to maintain connections

1) check external IP
2) compare current external IP with previously stored external IP and update if needed
3) check Cloud Flare origin IP
4) compare Cloud Flare origin IP with current external IP and update if needed

Cloud Flare API documentation https://api.cloudflare.com/
'''

import requests
import os
import fileinput
import json

EMAIL = os.getenv('CF_API_EMAIL')
KEY = os.environ.get('CF_API_KEY')
EXTERNAL_IP = ""
oldIP = ""

headers = {
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': KEY,
    'Content-Type': 'application/json',
}

configFileList = []
configDict = {}

#write configDict to config.txt
def writeConfig():
	toWrite = []

	for l in configDict.keys():
		toWrite.append(l + ' = ' + configDict[l] + '\n')

	# and write everything back
	with open('config.txt', 'w') as file:
	    file.writelines(toWrite)

#read in config.txt and create configDict
def readConfig():
	configFile = open('config.txt', 'r' )
	configFileList = configFile.readlines()
	#configDict = {}

	for kv in configFileList:
		if '#' not in kv:
			if '\n' in kv:
				kv = kv.replace('\n','')

			kvSplit = kv.split(' = ')
		
			if len(kvSplit)-1 > 0:
				configDict[kvSplit[0]]=kvSplit[1]

	print(configDict)

#update configDict and config.txt file
def updateLocalIP():
	"""configFile = open('config.txt', 'r+' )
				configFileList = configFile.readlines()"""

	exIP = requests.get('http://whatismyip.akamai.com/').text

	print(configDict.keys())
	if 'ip' in configDict.keys():
		if configDict['ip'] != exIP:
			configDict['ip'] = exIP
			EXTERNAL_IP = exIP
			writeConfig()
			print("External IP updated to " + EXTERNAL_IP)
		else:
			EXTERNAL_IP = exIP
			print("External IP " + EXTERNAL_IP + " unchanged")
	else:
		configDict['ip'] = exIP
		EXTERNAL_IP = exIP
		writeConfig()
		print("External IP " + EXTERNAL_IP + " added to config.txt")

#return list of pools
def listPools():
	response = requests.get('https://api.cloudflare.com/client/v4/user/load_balancers/pools', headers=headers)

	return response.json()
	#test = json.loads(response.json())
	#return test

#update Cloud Flare origin info
def updateLoadBalancerOriginIP():
	
	if configDict['ip'] != getOriginIP():
		
		print('updating Cloud Flare origin IP')
		#today = date.today()

		data = {"origins":[{"name":configDict['originName'],"address":configDict['ip'],"enabled":True,"weight":1}]}
		
		dt = json.dumps(data)
		print(dt)
		response = requests.patch('https://api.cloudflare.com/client/v4/user/load_balancers/pools/' + configDict['poolID'], headers=headers, data=dt)

		print(response.json())
	else:
		print('Cloud Flare origin IP is good')

#get pool idea matching pool name in config file
"""def getPoolID():

	pools = listPools()['result']

	#get pool id
	for pool in pools:
		if pool['name'] == configDict['poolName']:
			configDict['poolID'] = pool['id']
			writeConfig()
			#print(pool)"""

#retrieve the IP address for the origin
def getOriginIP():
	response = requests.get('https://api.cloudflare.com/client/v4/user/load_balancers/pools/'+configDict['poolID'], headers=headers)

	origAddress = ""

	if response.json()['success'] == True:
		for o in response.json()['result']['origins']:
			if o['name'] == configDict['originName']:
				origAddress = o['address']
				break
	else:
		print('getOriginIP response' + str(response.json()['success']))
	return origAddress

def updateDNS():
	return

def updateRemoteIP():
	if configDict['mode'] == 'load balancer':
		updateLoadBalancerOriginIP()
	elif configDict['mode'] == 'dns':
		updateDNS()

readConfig()
updateLocalIP()

updateRemoteIP()
