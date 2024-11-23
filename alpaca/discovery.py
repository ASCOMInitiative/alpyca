# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# discovery - Implements ASCOM Alpaca discovery functions
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# Doc Environment: Sphinx v5.0.2 with autodoc, autosummary, napoleon, and autoenum
# GitHub: https://github.com/ASCOMInitiative/alpyca
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022-2024 Ethan Chappel and Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# Edit History:
# 02-May-22 (rbd) Initial Edit
# 03-May-22 (rbd) Remove import of 're' no longer used. IPv6 query comments,
#                 default timeout is 2 sec.
# 13-May-22 (rbd) 2.0.0-dev1 Project now called "Alpyca" - no logic changes
# 21-Aug-22 (rbd) 2.0.2 Fix multicast to 127.0.0.1 GitHub Issue #6
# -----------------------------------------------------------------------------

import json
import socket
import netifaces
import platform
from typing import List

port = 32227
AlpacaDiscovery = "alpacadiscovery1"
AlpacaResponse = "AlpacaPort"


def search_ipv4(numquery: int=2, timeout: int=2) -> List[str]:
    """Discover Alpaca device servers on the IPV4 LAN/VLAN

    Returns a list of strings of the form ``ipaddress:port``,
    each corresponding to a discovered Alpaca device
    server. Use :doc:`alpaca.management` functions to enumerate the
    devices.

    Args:
        numquery: Number of discovery queries to send (default 2)
        timeout: Time (sec.) to allow for responses to each
            discovery query. Optional, defaults to 2 seconds.

    Raises:
       To be determined.

    Note:
        * This function uses IPV4
        * UDP protocol using multicasts and restricted to the LAN/VLAN is used to perform the query.
        * See section 4 of the `Alpaca API Reference <https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf>`_
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
                                            ('127.255.255.255', port))
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
    Use :doc:`alpaca.management` functions to enumerate the
    devices.

    Args:
        numquery: Number of discovery queries to send (default 2)
        timeout: Time (sec.) to allow for responses to the discovery
            query. Optional, defaults to 2 seconds.

    Raises:
       To be determined.

    Note:
        * This function uses IPV6
        * UDP protocol, restricted link-local addresses to the LAN/VLAN attached to each
          interface, is used to perform the query. Does not query global IPv6.
        * ISATAP addresses are specifically excluded.
        * See section 4 of the `Alpaca API Reference <https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf>`_
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
                        # the ISATAP addresses.
                        if (not addr.startswith('fe80') or
                                addr.startswith('fe80::5efe') or
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


