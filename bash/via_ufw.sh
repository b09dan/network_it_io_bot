#!/bin/bash

#change rules
sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp
sudo ufw allow from any to any port 80 proto tcp
sudo ufw allow out 80
sudo ufw allow out 443
sudo ufw allow out 53

echo "Rules changed."
sleep 5

#deny all
sudo ufw default deny incoming 
sudo ufw default deny outgoing

echo "All policies = deny"
sleep 5
