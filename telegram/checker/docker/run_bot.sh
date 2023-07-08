#!/bin/bash

docker volume create telegram_bot_volume

docker run  -it -v telegram_bot_volume:/anf_checker/database --restart=unless-stopped  anf_checker
#docker run  -it --env-file ./tmp/conf.txt -v telegram_bot_volume:/anf_checker/database --restart=unless-stopped  anf_checker
