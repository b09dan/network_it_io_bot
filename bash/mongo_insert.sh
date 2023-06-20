#!/bin/bash
set -e


mongo admin -u admin -p admin < sc.js

for i in {1..5}
do
    for collect in {a..u}
    do
	for doc in {1..1000}
	do
	    mongo db$i -u myusr -p myusr --eval "db.$collect.insert({ page: "$RANDOM" })"

        done
    done	
done
