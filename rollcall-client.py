#!/usr/bin/python3

import requests
import socket
import json
import ast

_SERVER_ADDR = "10.0.0.201/cgi-bin/rollcall-json.py"

def sendUpdate():
    payload = {'hostname': socket.gethostname()}
    r = requests.get("http://" + _SERVER_ADDR, params=payload)
    #print("Request url was:", r.url)
    return r.text

if __name__ == "__main__":
    resp = sendUpdate()
    j = json.loads(resp)
    print("ERRMSGS")
    for msg in j["errMsgs"]:
        print(msg)
    print("TABLE")
    for ka in j["table"].keys():
        ipAndTime = ast.literal_eval(j["table"][ka])
        print("%s,%s,%s" % (ka, ipAndTime["IP"], ipAndTime["TIME"]))        
