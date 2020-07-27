# dynamic-IP-updater
Updates Cloudflare load balancing origin when a server's dynamic IP changes to maintain connections

This was designed for a server running on a Raspberry Pi 3B+ on a residential network with a dynamic IP. It is often not possible to get a static external IP from an ISP if you have a residential internet service contract. Commercial internet service contracts can be expensive. This allows you to run a server with a dynamic IP and maintain functionality even if the IP changes, through Cloudflare's load balancing services.

## Setup
* Server setup
	* Enable port forwarding on the router.
	* Assign port 80 to your server.

* Cloudflare setup
	* Create a CF account (the free account will work) and enable load balancing (starts at $5)
	* Cloud Flare load balancing https://developers.cloudflare.com/load-balancing/about
	* Cloud Flare API documentation https://api.cloudflare.com/

## Environmental Variables
User email and the API key are stored in environmental variables
* The environmental variable values are CF_API_EMAIL and CF_API_KEY

Setting environmental variables on the Pi (source https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
* Variables set in the /etc/profile file are loaded whenever a bash login shell is entered. You may need to reboot after adding the variables to this file.
* When declaring environment variables in this file you need to use the export command. Do not put a space around the =.
* Add these lines to bottom of /etc/profile 
	* export CF_API_EMAIL=api-user-email
	* export CF_API_KEY=api-key

## Config File
Config file must include ip, originName, and poolID. ip gets updated automatically when it changes. Correct originName and poolID must be hardcoded in.
* ip = 0.0.0.0 
* originName = myOrigin
* poolID = abcdefghijklmnopqrstuvwxyz1234567890

## Automation
For Raspberry Pi, set chron job to run on boot and every 15 minutes
* Make script runner executable
	* chmod 755 scriptrunner.sh
* Schedule Cron jobs (note: cron jobs change the environment, so environmental variables do not necessarily work - if environmental variables were set as suggested above, the below cron job lines should work. You can also try putting environment variables directly in cron)

	* */15 * * * * . /etc/profile; sh /home/pi/dynamic-IP-updater/scriptrunner.sh > /home/pi/dynamic-IP-updater/cronlog.log 2>&1
	* @reboot sleep 30 && . /etc/profile; sh /home/pi/dynamic-IP-updater/scriptrunner.sh > /home/pi/dynamic-IP-updater/cronlog.log 2>&1

## Additional Resources

The Cloudflare API examples are in cURL. This tool converts cURL syntax to Python syntax
* https://curl.trillworks.com/