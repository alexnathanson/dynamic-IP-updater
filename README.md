# dynamic-IP-updater
A script for check for changes to dynamic IP addresses and updating Cloud Flare to maintain connections

Cloud Flare API documentation https://api.cloudflare.com/
* The API requires the user email and the API key
* The environmental variable values are CF_API_EMAIL and CF_API_KEY



Setting environmental variables on Pi (source https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
* /etc/profile - Variables set in this file are loaded whenever a bash login shell is entered. When declaring environment variables in this file you need to use the export command:
* example:
	* export CF_API_EMAIL = api-user-email
	* export CF_API_KEY = api-key