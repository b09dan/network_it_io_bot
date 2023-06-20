#!/bin/bash

#http, ping, ssh
sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I OUTPUT -p tcp --sport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport ssh -s 192.168.100.0/24 -j ACCEPT
sudo iptables -I OUTPUT -p tcp --sport ssh -s 192.168.100.0/24 -j ACCEPT
iptables -I INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -I OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
echo "Changed http, ping, ssh."
sleep 5

#outgoing
sudo iptables -I INPUT -p udp --sport 53 -j ACCEPT
sudo iptables -I INPUT -p tcp --sport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --sport 443 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT

sudo iptables -I OUTPUT -p udp --dport 53 -j ACCEPT
sudo iptables -I OUTPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

echo "Changed outgoing."
sleep 5

#deny all
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP
sudo iptables -P FORWARD DROP

echo "Changed policy."
sleep 5
