#!/bin/bash

port=5300

while [[ $# -gt 0 ]]; do
  case $1 in
    -p|--port)
      port="$2"
      shift
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done


ip_ok="127.0.0.1"

ip=`dig -p $port @127.0.0.1  +tcp +short  example.com`

dig -p $port @127.0.0.1  +tcp example.com

echo "This is ip: $ip"


#check that ip is ok

if [[ $ip == $ip_ok ]]; then
 exit 0
fi

# exit with error code in other cases
exit 11

