#!/usr/bin/python3

import requests
import socket

_SERVER_ADDR = "10.0.0.201/cgi-bin/rollcall.py"

def sendUpdate():
    payload = {'hostname': socket.gethostname()}
    r = requests.get("http://" + _SERVER_ADDR, params=payload)
    print("Request url was:", r.url)
    return r.text

def main():
    resp = sendUpdate()
    print(resp)

if __name__ == "__main__":
    main()
