#!/bin/bash -1
# scriptrunner.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/dynamic-IP-updater
python cloudFlare-dynamic-IP-updater.py
cd /
