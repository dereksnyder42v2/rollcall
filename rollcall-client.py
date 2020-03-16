#!/usr/bin/python3

import requests
import socket
import json
import ast

_SERVER_ADDR = "10.0.0.201/cgi-bin/rollcall.py"

def sendUpdate():
    payload = {'hostname': socket.gethostname()}
    r = requests.get("http://" + _SERVER_ADDR, params=payload)
    #print("Request url was:", r.url)
    return r

if __name__ == "__main__":
    req = sendUpdate()
    try:
        j = json.loads(req.text)
    except Exception as e:
        print("JSON failed to load.")
        print("\tRequested URL: %s" % req.url)
        print("\tStatus code: %d" % req.status_code)
        print("\tResponse text:\n%s" % req.text)
        quit()
    print("ERRMSGS")
    for msg in j["errMsgs"]:
        print(msg)
    print("TABLE")
    for ka in j["table"].keys():
        ipAndTime = ast.literal_eval(j["table"][ka])
        print("%s,%s,%s" % (ka, ipAndTime["IP"], ipAndTime["TIME"]))        
