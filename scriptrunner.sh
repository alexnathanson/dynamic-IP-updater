#!/bin/bash
# navigate to home directory, then to this directory, then execute python script, then back home

#printenv

cd /
cd home/pi/dynamic-IP-updater
python cloudFlare-dynamic-IP-updater.py
cd /
