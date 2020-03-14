#!/usr/bin/python3

import cgi, cgitb 
import traceback
import sys
import redis
import datetime
import os

#cgitb.enable()

# accepts name of environment variable as argument
def getEnvVar(varName):
    result = os.environ.get(varName)
    return result

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
v 		the value to write to k 	"""
def redisWrite(server, k, v):
    try:
        server.set(k, v)
    except:
        log("rollcall.py#redisWrite: failed to connect to redis server.")
        return False
    return True

# ---MAIN---
if __name__ == "__main__":

    LINEBR = "<br>"     

    print("""Content-Type: text/html\r\n\r\n
<!DOCTYPE html>
<head>
<title>Rollcall</title>
</head>
<body>""")
    
    """# for debugging:
    cgi.print_environ_usage() # for debugging
    print("REMOTE_ADDR: %s<br>\n" % (getEnvVar("REMOTE_ADDR") ) )
    print("REMOTE_HOST: %s<br>\n" % (getEnvVar("REMOTE_HOST") ) )
    print("REMOTE_IDENT: %s<br>\n" % (getEnvVar("REMOTE_IDENT") ) )
    print("REMOTE_USER: %s<br>\n" % (getEnvVar("REMOTE_USER") ) )
    print("HTTP_USER_AGENT: %s<br>\n" % (getEnvVar("HTTP_USER_AGENT") ) )
    print(os.environ)
    """
    
    server = redisConnect("localhost", 6379)
    if not server:
        print("Redis server connection failed.<br>\n")
    form = cgi.FieldStorage()
    #print(form, LINEBR) # for debugging - show the whole form
    IP = None
    HOSTNAME = None
    for thing in form:
        #print("%s: %s<br>\n" % (thing, form.getvalue(thing)))
        if str(thing)=="ip":
            IP = form.getvalue(thing)
        elif str(thing)=="hostname":
            HOSTNAME = form.getvalue(thing)
    if (IP != None) and (HOSTNAME != None):
        print("IP: %s, HOSTNAME: %s<br>\n" % (IP, HOSTNAME))
        redisWrite(server, HOSTNAME, IP)
    else:
        print("IP address and HOSTNAME not received.<br>\n")
    """
    except Exception as err:
        errStr = traceback.format_exc() 
        print(errStr)
        #print( "</body>\n</html>")
    """

    print("</body>\n</html>")
