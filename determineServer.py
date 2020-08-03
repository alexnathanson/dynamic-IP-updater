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


headers = {
    #'X-Auth-Email': EMAIL,
    #'X-Auth-Key': KEY,
    'Content-Type': 'application/json',
}

dstIPs = []
localData = ""

#replace with system for retrieving DST IPs
def getDstIPs():

	updatedIPs = ['192.168.1.206']

	for i in range(len(updatedIPs)):
		dstIPs.append(updatedIPs[i])

#return data from a particular server
def getData(dst):
	response = requests.get('http://' + dst + '/pvData.json', headers=headers)

	#print(response.json())

	return response.json()

def remoteData():
	allData = []

	for dst in dstIPs:
		#print(dst)
		allData.append(getData(dst))

	print('remoteDate')
	print(allData)
	determineServer(allData)

def determineServer(arrayOfData):

	#add a mechanism for comparing time stamps...
	print('determineServer')
	print(arrayOfData)
	thisServer = True

	#loop through data from all servers and compare voltages
	for s in arrayOfData:
		if s['pvData']['voltage']>localData['pvData']['voltage']:
			thisServer = False

	if thisServer:
		print('WINNER')
		os.system(subCall)

def localData():
	#get the local PV data

	# read file
	with open('/var/www/html/pvData.json', 'r') as myfile:
	    data=myfile.read()

	# parse file
	localData = json.loads(data)

	#print(localData['pvData'])

localData()
getDstIPs()
remoteData()