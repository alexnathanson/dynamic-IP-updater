'''
This script retreives data from other servers.
Compares data between devices and identifies the primary.
If the local devices is the primary it updates the DNS system.
'''

import requests
import os
import fileinput
import json

subCall = 'python /home/pi/dynamic-IP-updater/cloudflare-dynamic-IP-updater.py'

dstIPs = []

headers = {
    #'X-Auth-Email': EMAIL,
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/json',
}

localData = ""

#replace with system for retrieving DST IPs
def getDstIPs():
	dstIPs = ['192.168.1.206']

#return data from a particular server
def getData(dst):
	response = requests.get(dst + '/pvData.json', headers=headers)

	return response.json()

def remoteData():
	allData = []

	for dst in dstIPs:
		allData.append(getData(dst))

	print(allData)
	#determineServer(allData)

def determineServer(arrayOfData):

	#add a mechanism for comparing time stamps...

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
	with open('/var/www/html/pvData.json', 'r') as myfile:
	    data=myfile.read()

	# parse file
	localData = json.loads(data)

	print(localData['pvData'])

localData()
getDstIPs()
remoteData()