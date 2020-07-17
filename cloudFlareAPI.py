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

EMAIL = os.getenv('CF_API_EMAIL')
KEY = os.environ.get('CF_API_KEY')

EXT_IP = os.environ.get('EXTERNAL_IP')
print(EXT_IP);

#os.environ['EXTERNAL_IP'] = 'TEST_username'

headers = {
    'X-Auth-Email': EMAIL,
    'X-Auth-Key': KEY,
    'Content-Type': 'application/json',
}

data = {}

def getExternalIP():
	exIP = requests.get('http://whatismyip.akamai.com/')
	return exIP.text

def getPoolInfo():
	response = requests.get('https://api.cloudflare.com/client/v4/user/load_balancers/pools', headers=headers)

	print(response.json())

def updateOriginIP():
	today = date.today()

	exIP = "google.com" #getExternalIP();
	data = {"description":"My first pool, updated "+ today,
		"origins":[{"name":"RedHook","address":exIP,"enabled":true,"weight":1}]}


getExternalIP()
