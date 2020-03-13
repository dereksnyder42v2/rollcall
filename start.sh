#!/bin/bash

# This enables CGI for your apache server
ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled
chmod +x /usr/lib/cgi-bin/*
service apache2 start

# This allows redis to bind to the proper address & port
sed -i '/bind 127.0.0.1 ::1/c\#bind 127.0.0.1 ::1' /etc/redis/redis.conf
service redis-server start

# run forever...or else the docker will exit.
while true
do
	sleep 1
done

