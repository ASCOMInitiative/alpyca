import json
import os
import socket
import struct
import netifaces
from typing import List, Any

port = 32227
AlpacaDiscovery = "alpacadiscovery1"
AlpacaResponse = "AlpacaPort"


def search_ipv4(timeout: int=5) -> List[str]:
    """Discover Alpaca device servers on the IPV4 LAN/VLAN
    
    Returns a list of strings of the form ``ipaddress:port``,
    each corresponding to a discovered Alpaca device
    server. Use :py:mod:`alpaca.management` functions to enumerate the 
    devices.

    Args:
        timeout: Time (sec.) to allow for responses to the discovery 
        query. Optional, defaults to 5 seconds.
    
    Raises:
       To be determined.
    
    Notes:
        * This function uses IPV4
        * UDP protocol, restricted to the LAN/VLAN is used to perform the query. 
        * See section 4 of the `Alpaca API Reference <https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf>`
          for Discovery details. 

    """
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
    sock.close()
    return addrs


def search_ipv6(timeout: int=5) -> List[str]:
    """Discover Alpaca device servers on the IPV4 LAN/VLAN
    
    Returns a list of strings of the form ``ipv6address:port``,
    each corresponding to a discovered Alpaca device
    server. Use :py:mod:`alpaca.management` functions to enumerate the 
    devices.

    Args:
        timeout: Time (sec.) to allow for responses to the discovery 
        query. Optional, defaults to 5 seconds.
    
    Raises:
       To be determined.

    Attention:
        This function does not yet work.
    
    Notes:
        * This function uses IPV^
        * UDP protocol, restricted to the LAN/VLAN is used to perform the query. 
        * See section 4 of the `Alpaca API Reference <https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf>`
          for Discovery details. 

    """
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    try:
        sock.bind(('', 0))  # listen to any on a temporary port
    except:
        print('failure to bind')
        sock.close()
        raise

    # for interface in netifaces.interfaces():
    #     for interfacedata in netifaces.ifaddresses(interface):
    #         if netifaces.AF_INET6 == interfacedata:
    #             for ip in netifaces.ifaddresses(interface)[netifaces.AF_INET6]:
    #                 sock.sendto(AlpacaDiscovery.encode(),
    #                             ("ff12::a1:9aca", port))

    sock.sendto(AlpacaDiscovery.encode(), ("ff12::a1:9aca", port))
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
    sock.close()
    return addrs


