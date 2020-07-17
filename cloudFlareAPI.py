'''
Dynamic DNS with Cloudflare on Raspberry Pi server

Updates dynamic IP

1) check public IP
2) compare with previous stored public IP
3) check Cloud Flare origins
4) if IP different, update Cloud Flare origin
'''

import requests

headers = {
    'X-Auth-Email': '',
    'X-Auth-Key': '',
    'Content-Type': 'application/json',
}

data = {}



exIP = ""

getExternalIP()

def getExternalIP():
	exIP = requests.get('http://whatismyip.akamai.com/')
	print(exIP)

def getPoolInfo():
	response = requests.get('https://api.cloudflare.com/client/v4/user/load_balancers/pools', headers=headers)

	print(response.json())

