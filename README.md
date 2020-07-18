# dynamic-IP-updater
Updates Cloudflare load balancing origin when dynamic IP changes to maintain connections

1) check external IP
2) compare current external IP with previously stored external IP and update if needed
3) check Cloud Flare origin IP
4) compare Cloud Flare origin IP with current external IP and update if needed

Cloud Flare API documentation https://api.cloudflare.com/

User email and the API key are stored in environmental variables
* The environmental variable values are CF_API_EMAIL and CF_API_KEY

Setting environmental variables on Pi (source https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
* add these lines to bottom of /etc/profile - Variables set in this file are loaded whenever a bash login shell is entered. When declaring environment variables in this file you need to use the export command:
	* export CF_API_EMAIL = api-user-email
	* export CF_API_KEY = api-key

Config file must include ip, originName, and poolID. ip gets updated automatically when it changes. Correct originName and poolID must be hardcoded in.
* ip = 0.0.0.0 
* originName = myOrigin
* poolID = abcdefghijklmnopqrstuvwxyz1234567890

For Raspberry Pi, set chron job to run on boot and every 15 minutes
* Make script runner executable
	* chmod 755 scriptrunner.sh
* Schedule Cron jobs (note: cron jobs change the environment, so environmental variables do not necessarily work - if environmental variables were set as suggested above, the below cron job lines should work. You can also try putting environment variables directly in cron)

	* */15 * * * * . /etc/profile; sh /home/pi/dynamic-IP-updater/scriptrunner.sh > /home/pi/dynamic-IP-updater/cronlog.log 2>&1
	* @reboot sleep 30 && . /etc/profile; sh /home/pi/dynamic-IP-updater/scriptrunner.sh > /home/pi/dynamic-IP-updater/cronlog.log 2>&1