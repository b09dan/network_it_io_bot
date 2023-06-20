#!/bin/bash

set -e

date=`date '+%Y-%m-%d-%S'`
tar -zcvf ./backup/log_backup.$date.tar.gzip  logs

#delete old files
ls -t ./backup/log_backup* | tail -n+6 | xargs -i sh -c "rm {} | echo 'delete file: {}'" 

