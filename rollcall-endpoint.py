#!/usr/bin/python3

import cgi, cgitb 
import traceback
import sys
import redis
import datetime

#cgitb.enable()

def log(line):
    with open("rollcall.log", "a") as f:
        #f.write(str(datetime.datetime.now()) + ":" + line + "\n")
		f.write("%s: %s\n" % (str(datetime.datetime.now(), line) ) )

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
    print("""Content-type:text/html\r\n\r\n
<!DOCTYPE html>
<head>
<title>Rollcall</title>
</head>
<body>""")

    try:
        form = cgi.FieldStorage()
        print(form, LINEBR)
        for thing in form:
            print(thing, ":")
            print(form.getvalue(thing), LINEBR)

    except Exception as err:
        errStr = traceback.format_exc() 
        print(errStr)
        print(
            """</body>
</html>""")

	print("""</body></html>""")

