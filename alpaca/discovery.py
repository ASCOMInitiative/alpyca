import json
import socket
import netifaces
import platform
from typing import List
import re

port = 32227
AlpacaDiscovery = "alpacadiscovery1"
AlpacaResponse = "AlpacaPort"


def search_ipv4(numquery: int=2, timeout: int=2) -> List[str]:
    """Discover Alpaca device servers on the IPV4 LAN/VLAN
    
    Returns a list of strings of the form ``ipaddress:port``,
    each corresponding to a discovered Alpaca device
    server. Use :py:mod:`alpaca.management` functions to enumerate the 
    devices.

    Args:
        numquery: Number of discovery queries to send
        timeout: Time (sec.) to allow for responses to each
        discovery query. Optional, defaults to 2 seconds.
    
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
    sock.settimeout(timeout)
    try:
        sock.bind(('0.0.0.0', 0))  # listen to any on a temporary port
    except:
        print('failure to bind')
        sock.close()
        raise

    addrs = []
    try:
        for i in range(numquery):
            for interface in netifaces.interfaces():
                for interfacedata in netifaces.ifaddresses(interface):  # Sift through interfaces
                    if netifaces.AF_INET == interfacedata:             # Consider only those with IPv4
                        for ip in netifaces.ifaddresses(interface)[netifaces.AF_INET]:  # Each IPv4 address on this interface
                            addr = ip['addr']
                            if(addr ==  '127.0.0.1'):
                                sock.sendto(AlpacaDiscovery.encode(),
                                            ('127.0.0.1', port))
                            elif('broadcast' in ip):
                                sock.sendto(AlpacaDiscovery.encode(),
                                            (ip['broadcast'], port))
                            # I know this is inefficient, but this way we can filter
                            # out any of our local addresses (adapters).
                            while True:
                                try:
                                    pinfo, rem = sock.recvfrom(1024)  # buffer size is 1024 bytes
                                    remport = json.loads(pinfo.decode())["AlpacaPort"]
                                    remip, p = rem
                                    if(remip == addr and remip != '127.0.0.1'):
                                        continue                # avoid router loop back to ourselves
                                    ipp = f"{remip}:{remport}"
                                    if ipp not in addrs:        # Avoid dupes if numquery > 1
                                        addrs.append(ipp)
                                except:
                                    break
    finally:
        sock.close()
    return addrs


def search_ipv6(numquery: int=2, timeout: int=2) -> List[str]:
    """Discover Alpaca device servers on the IPV6 LAN/VLAN
    
    Returns a list of strings of the form ``[ipv6address%intfc]:port``,
    each corresponding to a discovered Alpaca device server. 
    Use :py:mod:`alpaca.management` functions to enumerate the 
    devices.

    Args:
        numquery: Number of discovery queries to send
        timeout: Time (sec.) to allow for responses to the discovery 
        query. Optional, defaults to 5 seconds.
    
    Raises:
       To be determined.

    Notes:
        * This function uses IPV6
        * UDP protocol, restricted to the LAN/VLAN attached to each interface,
          is used to perform the query. Does not query glovsl IPv6.
        * See section 4 of the `Alpaca API Reference <https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf>`
          for Discovery details. 

    """
    my_plat = platform.system()
    addrs = []
    for i in range(numquery):
        for interface in netifaces.interfaces():
            for interfacedata in netifaces.ifaddresses(interface):  # Sift through interfaces
                 if netifaces.AF_INET6 == interfacedata:            # Consider only those with IPv6
                    for info in netifaces.ifaddresses(interface)[netifaces.AF_INET6]:
                        addr = info['addr']
                        # Can't bind socket to ::1 and successfully send.
                        # So lookfor source == dest and substitute later.
                        # Reject everything but real link-local, including
                        # the ISATAP addresses. TODO Combine with short circuit
                        if not (addr.startswith('fe80')): 
                            continue;
                        if (addr.startswith('fe80::5efe') or
                                addr.startswith('fe80::200:5efe')):
                            continue
                        scope = addr.split('%')[1]
                        try:
                            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                            if my_plat == 'Linux':
                                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, 
                                                (interface + '\0').encode())
                            elif my_plat == "Windows":
                                sock.bind((addr, 0))                    # Force send from this IP
                            else:
                                raise NotImplementedError('MacOS IPv6 discovery not yet supported')
                            sock.settimeout(timeout)
                            dest = 'ff12::a1:9aca'
                            sock.sendto(AlpacaDiscovery.encode(), (dest, port))
                            while True:
                                try:
                                    pinfo, rem = sock.recvfrom(1024)    # buffer size is 1024 bytes
                                    remport = json.loads(pinfo.decode())["AlpacaPort"]
                                    remip = rem[0]
                                    if(addr.startswith(remip)):
                                        ipp = f"[::1]:{remport}"        # Substitute loopback
                                    else:
                                        ipp = f"[{remip}%{scope}]:{remport}"    # External Alpaca 
                                    if ipp not in addrs:                # Avoid dupes if numquery > 1
                                        addrs.append(ipp)
                                except:
                                    break
                        finally:
                            sock.close()

    return addrs


