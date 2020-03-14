#!/usr/bin/python3

import cgi, cgitb 
import traceback
import sys
import redis
import datetime
import string
import ipaddress

#cgitb.enable()

# TODO this doesn't work at all haha
def log(line):
    """
    with open("/home/derek/Desktop/rollcall/rollcall.log", "a") as f:
        f.write("%s: %s\n" % (str(datetime.datetime.now(), line) ) )
    """
    #print("%s: %s\n" % (str(datetime.datetime.now(), line) ) )
    
    return None

# returns server instance if successful, else False
def redisConnect(host, port):
    server = redis.Redis(host=host, port=port)
    try:
        server.ping()
    except redis.exceptions.ConnectionError as err:
        log("rollcall.py#redisConnect: failed to connect to redis server.")
        return False
    
    return server

"""
server 	the redis server instance, 
k 		the key to write to in redis,
v 		the value to write to k"""
def redisWrite(server, k, v):
    try:
        server.set(k, v)
    except:
        log("rollcall.py#redisWrite: failed to connect to redis server.")
        return False
    
    return True

def redisRead(server, k):
    try:
        val = server.get(k).decode("UTF-8")
    except:
        log("rollcall#redisRead: failed to retrieve key.")

    return val


def redisKeys(server):
    l = list()
    for k in server.keys():
        l.append( k.decode('UTF-8'))
    
    return l

def validIp(addr):
    try:
        ipaddress.ip_address(addr)
    except ValueError:
        return False
    return True

"""
Allowed characters, per RFC 952:
- lowercase alpha (a-z)
- digits (0-9)
- hyphen character ("-")"""
def validHostname(host):
    for char in host:
        if char not in string.ascii_lowercase and \
            char not in string.digits and \
            char != "-":
            return False
        else:
            return True

# ---MAIN---
if __name__ == "__main__":
    print("Content-Type: text/plain\r\n\r\n")     
    server = redisConnect("localhost", 6379)
    if not server:
        print("Redis server connection failed.")
        exit()
    form = cgi.FieldStorage()
    #print(form, LINEBR) # for debugging - show the whole form
    IP = None
    HOSTNAME = None
    for thing in form:
        if str(thing)=="ip":
            IP = form.getvalue(thing)
        elif str(thing)=="hostname":
            HOSTNAME = form.getvalue(thing).lower()
    # validate input 
    if validIp(IP) and validHostname(HOSTNAME):
        print("OK")
        redisWrite(server, HOSTNAME, IP)
    else:
        print("FAIL")
    print("(key),(value)")
    for h in redisKeys(server):
        print("%s,%s" % (h, redisRead(server, h)) )
