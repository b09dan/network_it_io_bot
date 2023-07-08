#!/bin/bash

mkdir -p tmp
cp ../*.py ../*.cfg ./tmp/
docker build -t anf_checker .

