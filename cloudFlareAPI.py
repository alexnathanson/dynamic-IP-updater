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

EMAIL = os.getenv('CF_API_EMAIL')
KEY = os.environ.get('CF_API_KEY')
EXTERNAL_IP = ""
oldIP = ""

headers = {
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': KEY,
    'Content-Type': 'application/json',
}

data = {}

configFileList = []

def checkExternalIP():
	exIP = requests.get('http://whatismyip.akamai.com/').text

	if(exIP != oldIP):
		EXTERNAL_IP = exIP

		# now change the 2nd line, note that you have to add a newline
		data[1] = 'Mage\n'

		# and write everything back
		with open('stats.txt', 'w') as file:
		    file.writelines( data )

		print("External IP updated to " + EXTERNAL_IP)
	else:
		print("External IP " + EXTNERAL_IP + " unchanged")

def writeConfig(listToWrite):
	# and write everything back
	with open('config.txt', 'w') as file:
	    file.writelines(listToWrite)

def updateIP():
	configFile = open('config.txt', 'r+' )
	configFileList = configFile.readlines()

	exIP = requests.get('http://whatismyip.akamai.com/').text

	notHere = True

	for l in range(len(configFileList)):
		if 'ip = ' in configFileList[l]:
			notHere = False
			#print(configFileList[l])
			oldIP = configFileList[l].split()[2]
			#print(oldIP)

			if(exIP != oldIP):
				EXTERNAL_IP = exIP

				# now change the 2nd line, note that you have to add a newline
				configFileList[l] = 'ip = ' + exIP +'\n'
		
				writeConfig(configFileList)

				print("External IP updated to " + EXTERNAL_IP)
			else:
				EXTERNAL_IP = oldIP
				print("External IP " + EXTERNAL_IP + " unchanged")
			break

	if notHere == True:
		EXTERNAL_IP = exIP
		configFileList.append('\nip = ' + exIP)
		writeConfig(configFileList)
		print("External IP " + EXTERNAL_IP + " added to config.txt")

def getPoolInfo():
	response = requests.get('https://api.cloudflare.com/client/v4/user/load_balancers/pools', headers=headers)

	print(response.json())

def updateOriginIP():
	today = date.today()

	exIP = "google.com" #getExternalIP();
	data = {"description":"My first pool, updated "+ today,
		"origins":[{"name":"RedHook","address":exIP,"enabled":true,"weight":1}]}

#checkExternalIP()

updateIP()