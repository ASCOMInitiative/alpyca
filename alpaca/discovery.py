# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# discovery - Implements ASCOM Alpaca discovery functions
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.9 or later
# Doc Environment: Sphinx v5.0.2 with autodoc, autosummary, napoleon, and autoenum
# GitHub: https://github.com/ASCOMInitiative/alpyca
#
# About netifaces 0.11.0 package: This is now abandonware, Issue #17 requests
# a change. I looked at netifaces2 but it is incompatible (long story) but
# netifaces-plus appears to be a fork of the original al45tair/netifaces and
# it appears to work.
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
# 06-Mar-25 (rbd) 3.1.0 Fix Issue #17 by ditching netifaces and friends, and
#                       using ifaddr while detecting inactive IPs another way.
# -----------------------------------------------------------------------------

import time
import json
import socket
import platform
from typing import List
import ipaddress
import ifaddr
# https://ifaddr.readthedocs.io/latest/

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
        * UDP protocol restricted to the LAN/VLAN is used to perform the query.
        * Adapters which show an APIPA address (169.254.*.*) are skipped in order to avoid a
          guaranteed timeout trying to receive the datagram replies. See
          `Why Do I Have the 169.254 IP Address? <https://www.whatismyip.com/169-254-ip-address/>`_
        * See section 4 of the `Alpaca API Reference <https://ascom-standards.org/AlpacaDeveloper/ASCOMAlpacaAPIReference.html>`_
          for Discovery details.

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)
    try:
        sock.bind(('0.0.0.0', 0))  # listen to any on a temporary port
    except:
        # print('failure to bind')
        sock.close()
        raise

    addrs = []
    try:
        for i in range(numquery):
            for adapter in ifaddr.get_adapters():
                for ip in adapter.ips:
                    if(ip.is_IPv4):
                        octets = ip.ip.split('.')
                        if(len(octets) != 4):               # Quality check
                            continue
                        if octets[0] == '169' and octets[1] == '254':
                            continue                        # APIPA address, skip
                        # print(ip.ip)
                        net = ipaddress.IPv4Network(f'{ip.ip}/{ip.network_prefix}', strict = False)
                        # print(net.broadcast_address)
                        n = sock.sendto(AlpacaDiscovery.encode(),(str(net.broadcast_address), port))
                        time.sleep(timeout / 2)            # Give the server(s) a bit of time to respond
                    while True:                         # Loop through response(s) till times out
                        try:
                            pinfo, rem = sock.recvfrom(1024)  # buffer size is 1024 bytes
                            remport = json.loads(pinfo.decode())["AlpacaPort"]
                            remip, p = rem
                            if(remip == ip.ip and remip != '127.0.0.1'):
                                continue                # avoid router loop back to ourselves
                            ipp = f"{remip}:{remport}"
                            if ipp not in addrs:        # Avoid dupes if numquery > 1
                                addrs.append(ipp)
                        except:
                            break                       # leave while True (to next for)


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
        * See section 4 of the `Alpaca API Reference <https://ascom-standards.org/AlpacaDeveloper/ASCOMAlpacaAPIReference.html>`_
          for Discovery details.

    """
    my_plat = platform.system()
    addrs = []
    for i in range(numquery):
        for adapter in ifaddr.get_adapters():
            addr = ''
            for ip in adapter.ips:
                if(ip.is_IPv6):
                    addr = ip.ip[0]
                    scope = ip.ip[2]
                    # Reject everything but real link-local, including
                    # the ISATAP addresses.
                    if (not addr.startswith('fe80') or
                            addr.startswith('fe80::5efe') or
                            addr.startswith('fe80::200:5efe')):
                        addr = ''
                        continue
                # This slime checks the IPV4 address of this adapter, and if it
                # is an APIPA address (169.254.*.*), we skip this adapter as we
                # did above. I don't know of another way to determine whether
                # an adapter is alive with a real local address like using APIPA.
                elif(ip.is_IPv4):
                    octets = ip.ip.split('.')
                    if(len(octets) != 4):               # Quality check
                        addr = ''
                    if octets[0] == '169' and octets[1] == '254':
                        addr = ''
            if(addr == ''):
                continue
            # print(f'local adapter on [{addr}]')
            try:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                if my_plat == 'Linux':
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE,
                                    (adapter.name + '\0').encode())
                elif my_plat == "Windows":
                    sock.bind((addr, 0))                    # Force send from this IP
                else:
                    raise NotImplementedError('MacOS IPv6 discovery not yet supported')
                sock.settimeout(timeout)
                if(addr == '::1'):
                    dest = addr
                else:
                    dest = 'ff12::a1:9aca'
                sock.sendto(AlpacaDiscovery.encode(), (dest, port))
                time.sleep(timeout / 2)                     # Give at least a bit of time to respond
                while True:
                    try:                                    # Loop through response(s) till times out
                        pinfo, rem = sock.recvfrom(1024)    # buffer size is 1024 bytes
                        remport = json.loads(pinfo.decode())["AlpacaPort"]
                        remip = rem[0]
                        # print(f'remote IP is {remip}')
                        if(addr.startswith(remip)):
                            # print(' This is us, loopback.')
                            ipp = f"[::1]:{remport}"        # Substitute loopback
                        else:
                            ipp = f"[{remip}%{scope}]:{remport}"    # External Alpaca
                        # print(f'Rcvd from {ipp}')
                        if ipp not in addrs:                # Avoid dupes if numquery > 1
                            # print(f'Adding {ipp}')
                            addrs.append(ipp)
                    except:
                        break
            finally:
                sock.close()
    return(addrs)
