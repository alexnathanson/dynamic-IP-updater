'''
This script retreives data from other servers.
Compares data between devices and identifies the primary.
If the local devices is the primary it updates the DNS system.
'''

import requests
import os
import fileinput
import json

#update with full path
subCall = 'python /home/pi/dynamic-IP-updater/cloudflare-dynamic-IP-updater.py'

myNAME = 'redhook.solarprotocol.net'

serverURL = ['nightlight.xyz']#,'bedstuy.solarprotocol.net','lic.solarprotocol.net']

headers = {
    #'X-Auth-Email': EMAIL,
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/json',
}

localData

#return data from a particular server
def getData(dst):
	response = requests.get(dst + '/v1/pvSystem.json', headers=headers)

	return response.json()

def remoteData():
	allData = []

	for dst in serverURL:
		allData.push(getData(dst))

	determineServer(allData)

def determineServer(arrayOfData):

	thisServer = True

	#loop through data from all servers and compare voltages
	for s in arrayOfData:
		if s['pvData']['voltage']>localData['pvData']['voltage']:
			thisServer = False

	if thisServer:
		os.system(subCall)

def localData():
	#get the local PV data

	# read file
	with open('pvData.json', 'r') as myfile:
	    data=myfile.read()

	# parse file
	localData = json.loads(data)

	print(obj)

localData()
remoteData()