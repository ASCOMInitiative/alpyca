import json
import os
import socket
import struct
import netifaces
from typing import List, Any

port = 32227
AlpacaDiscovery = "alpacadiscovery1"
AlpacaResponse = "AlpacaPort"


def search_ipv4(timeout: int) -> List[str]:
    # Create listening port
    # ---------------------
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        sock.bind(('0.0.0.0', 0))  # listen to any on a temporary port
    except:
        print('failure to bind')
        sock.close()
        raise

    for interface in netifaces.interfaces():
        for interfacedata in netifaces.ifaddresses(interface):
            if netifaces.AF_INET == interfacedata:
                for ip in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                    if('broadcast' in ip):
                        sock.sendto(AlpacaDiscovery.encode(),
                                    (ip['broadcast'], port))
    #
    # Spend 'timeout' sec collecting UDP responses
    # Return list of strings "ip:port" for input to all other methods
    #
    sock.settimeout(timeout)
    addrs = []
    while True:
        try:
            pinfo, rem = sock.recvfrom(1024)  # buffer size is 1024 bytes
            remport = json.loads(pinfo.decode())["AlpacaPort"]
            remip, p = rem
            addrs.append(f"{remip}:{remport}")
        except:
            break
    return addrs

