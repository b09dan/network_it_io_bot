#!/bin/bash
#save ssh config and change
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.old
sed -i 's/#Port 22/Port 222/' /etc/ssh/sshd_config
echo "port should be 222"
cat /etc/ssh/sshd_config | grep Port | grep 2
systemctl restart sshd

sleep 5

#change back
cp /etc/ssh/sshd_config.old /etc/ssh/sshd_config

systemctl restart sshd

echo "port should be 22"
cat /etc/ssh/sshd_config | grep Port | grep 2

journalctl | tail -20 | grep port
