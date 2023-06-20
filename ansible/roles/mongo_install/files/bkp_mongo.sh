#!/bin/bash
 
mkdir -p /var/bkp/mongobkp
mongodump -u admin -p admin  --gzip --archive > /var/bkp/mongobkp/`date +"%y-%m-%d"`.gz

#delete old files
ls -t /var/bkp/mongobkp/date* | tail -n+6 | xargs -i sh -c "rm {} | echo 'delete file: {}'"
