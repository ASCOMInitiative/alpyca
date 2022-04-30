import json
import socket
import netifaces
from typing import List

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

    try:
        sock.bind(('0.0.0.0', 0))  # listen to any on a temporary port
    except:
        print('failure to bind')
        sock.close()
        raise

    sock.settimeout(timeout)
    addrs = []

    for i in range(numquery):
        for interface in netifaces.interfaces():
            #for interfacedata in netifaces.ifaddresses(interface):
                # if netifaces.AF_INET == interfacedata:
                    for ip in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                        if(ip['addr'] ==  '127.0.0.1'):
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
                                if(remip == ip['addr'] and remip != '127.0.0.1'):
                                    continue                # avoid router loop back to ourselves
                                ipp = f"{remip}:{remport}"
                                if ipp not in addrs:        # Avoid dupes if numquery > 1
                                    addrs.append(ipp)
                            except:
                                break
        
    sock.close()
    return addrs


def search_ipv6(numquery: int=2, timeout: int=2) -> List[str]:
    """Discover Alpaca device servers on the IPV4 LAN/VLAN
    
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
    addrs = []
    for i in range(numquery):
        for interface in netifaces.interfaces():
            # Interface may have multiple IPv6 addresses (link local, global)
            for info in netifaces.ifaddresses(interface)[netifaces.AF_INET6]:
                # Only localhost or link-level, no global
                if not (info['addr'].startswith('fe80') or
                        info['addr'].startswith('::1')):
                    continue;
                try:
                    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                    sock.settimeout(timeout)
                    # This is the 'secret sauce'
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, 
                                    (interface + '\0').encode())
                    if(info['addr'].startswith('::1')):         # Avoid looping back via our own IPV6
                        dest = '::1'
                    else:
                        dest = 'ff12::a1:9aca'
                    sock.sendto(AlpacaDiscovery.encode(), (dest, port))
                    while True:
                        try:
                            pinfo, rem = sock.recvfrom(1024)    # buffer size is 1024 bytes
                            remport = json.loads(pinfo.decode())["AlpacaPort"]
                            remip = rem[0]
                            if(info['addr'] == '::1'):
                                ipp = f"[::1]:{remport}"        # No interface
                            elif(info['addr'].startswith(remip)):
                                continue                        # Only return '::1' not our own IPV6
                            else:
                                ipp = f"[{remip}%{interface}]:{remport}"    # External Alpaca 
                            if ipp not in addrs:                # Avoid dupes if numquery > 1
                                addrs.append(ipp)
                        except:
                            break
                finally:
                    sock.close()

    return addrs


