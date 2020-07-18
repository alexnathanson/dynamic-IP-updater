'''
Dynamic DNS with Cloudflare on Raspberry Pi server

Updates dynamic IP

1) check public IP
2) compare with previous stored public IP
3) check Cloud Flare origins
4) if IP different, update Cloud Flare origin
'''

import requests
import os
from datetime import date
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

#data = {}

configFileList = []
configDict = {}

def writeConfig():
	toWrite = []

	for l in configDict.keys():
		toWrite.append(l + ' = ' + configDict[l] + '\n')

	# and write everything back
	with open('config.txt', 'w') as file:
	    file.writelines(toWrite)

def readConfig():
	configFile = open('config.txt', 'r' )
	configFileList = configFile.readlines()
	#configDict = {}

	for kv in configFileList:
		if '\n' in kv:
			kv = kv.replace('\n','')

		kvSplit = kv.split(' = ')
	
		if len(kvSplit)-1 > 0:
			configDict[kvSplit[0]]=kvSplit[1]

	print(configDict)

def updateIP():
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

def listPools():
	response = requests.get('https://api.cloudflare.com/client/v4/user/load_balancers/pools', headers=headers)

	return response.json()
	#test = json.loads(response.json())
	#return test

def updateOriginIP():
	#today = date.today()

	data = {"description":"My first pool","origins":[{"name":"RedHook","address":configDict['ip'],"enabled":True,"weight":1}]}
	
	dt = json.dumps(data)
	print(dt)
	response = requests.patch('https://api.cloudflare.com/client/v4/user/load_balancers/pools/' + configDict['poolID'], headers=headers, data=dt)

	print(response.json())

def getPoolID():

	pools = listPools()['result']

	#get pool id
	for pool in pools:
		if pool['name'] == configDict['poolName']:
			configDict['poolID'] = pool['id']
			writeConfig()
			#print(pool)

readConfig()
updateIP()


updateOriginIP()

#print(type(listPools().keys()))