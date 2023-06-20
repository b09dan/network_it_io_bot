#!/bin/bash
set -e
#monuser
username=monuser
password=`openssl passwd -1 xdhaJ7UkZaKv52AJ`
userall="monitoring"
#generate sshkey
mkdir /tmp/monuser
ssh-keygen -t rsa -b 4096 -C monitoring -P '' -f /tmp/monuser/id_rsa
export SSHPUBKEY=`cat /tmp/monuser/id_rsa.pub`

useradd --password "$password" --user-group --create-home --comment "$userall" \
       	-s /path/to/shell/newshell.sh  $username

mkdir /home/monuser/.ssh ; cp /tmp/monuser/* /home/monuser/.ssh/
echo $SSHPUBKEY >> /home/monuser/.ssh/authorized_keys
chown -R monuser:monuser /home/monuser

