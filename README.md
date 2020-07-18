# dynamic-IP-updater
Updates Cloudflare load balancing origin when dynamic API changes to maintain connections

1) check external IP
2) compare current external IP with previously stored external IP and update if needed
3) check Cloud Flare origin IP
4) compare Cloud Flare origin IP with current external IP and update if needed

Cloud Flare API documentation https://api.cloudflare.com/
* The API requires the user email and the API key
* The environmental variable values are CF_API_EMAIL and CF_API_KEY

Setting environmental variables on Pi (source https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
* add these lines to bottom of /etc/profile - Variables set in this file are loaded whenever a bash login shell is entered. When declaring environment variables in this file you need to use the export command:
	* export CF_API_EMAIL = api-user-email
	* export CF_API_KEY = api-key

Config file must include
* ip = 108.29.41.133
* originName = RedHook
* poolID = 6119c80789e350dd436039010c99b5df