#!/usr/bin/python3

import cgi, cgitb 
import traceback
import sys
import redis
import datetime
import string
import ipaddress
import os
import json


# TODO this doesn't work at all haha
def log(line):
    return None

def redisKeys(server):
    l = list()
    for k in server.keys():
        l.append( k.decode('UTF-8'))
    
    return l

"""
Allowed characters, per RFC 952:
- lowercase alpha (a-z)
- digits (0-9)
- hyphen character ("-")

Note that a 'None' type hostname returns False."""
def validHostname(hostname):
    if not hostname:
        return False
    for char in hostname:
        if char not in string.ascii_lowercase and \
            char not in string.digits and \
            char != "-":
            return False
    return True

# ---MAIN---
if __name__ == "__main__":
    print("Content-Type: application/json\r\n\r\n")     
    #print("Content-Type: text/plain\r\n\r\n")
    errMsgs = list()
    response = dict()

    while True:
        server = redis.Redis(host="localhost", port=6379)
        try:
            server.ping()
        except redis.exceptions.ConnectionError as e:
            log("rollcall.py: Failed to connect to Redis server.")
            errMsgs.append("Redis server cnxn failed")
            response['errMsgs'] = errMsgs
            response['table'] = None
            break

        IP = None
        if "REMOTE_ADDR" not in os.environ.keys():
            errMsgs.append("REMOTE_ADDR key missing")
        else:
            IP = os.environ.get("REMOTE_ADDR")

        form = cgi.FieldStorage()
        HOSTNAME = None
        for thing in form:
            if str(thing)=="hostname":
                HOSTNAME = form.getvalue(thing).lower()
        
        # validate input and update server
        if IP and validHostname(HOSTNAME):
            server.set(HOSTNAME, json.dumps({'IP': IP, 'TIME': str(datetime.datetime.now()) }))
            errMsgs.append("Redis update successful")
        else:
            errMsgs.append("HOSTNAME invalid or not found")

        # 
        table = dict()
        for hostname in server.keys():
            table[hostname.decode("UTF-8")] = server.get(hostname).decode("UTF-8")
        response['table'] = table
        response['errMsgs'] = errMsgs
        break

    # Write response to client
    print(json.dumps(response))

