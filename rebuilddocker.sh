#!/bin/bash
bash ./destroyalldockers.sh
yes | docker system prune -a
docker build -t rollcall . && docker container run --publish 80:80 --detach --name willy rollcall
