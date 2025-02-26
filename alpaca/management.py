# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# management - Implements ASCOM Alpaca server Management class
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#           Ethan Chappel <ethan.chappel@gmail.com>
#
# Python Compatibility: Requires Python 3.9 or later
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
# 13-May-22 (rbd) 2.0.0-dev1 Project now called "Alpyca" - no logic changes
# -----------------------------------------------------------------------------

from typing import List
import requests
from alpaca.exceptions import AlpacaRequestException

API_VERSION = 1

def __check_error(response: requests.Response) -> None:
    """Check response from Alpaca server, raise unless 200

    Args:
        response (Response): Response from Alpaca server to check.

    Note:
        * Raises AlpacaRequestExcepton if the server returns
          other than a 200 OK.

    """
    if response.status_code != 200:
        raise AlpacaRequestException(response.status_code,
                f"{response.text} (URL {response.url})")

def __ipv6_safe_get(endpoint: str, addr: str) -> str:
    """HTTP GET from endpoint with IPv6-safe Host: header

        Args:
            endpoint: The endpoint path starting with /
            addr: full address (IPV6 or IPv4) of server

        Note:
            * This is needed because the Pyton requests module creates HTTP
              requests with the Host: header containing the scope (%xxxx)
              for IPv6, and some servers see this as invalid and return
              a 400 Bad Request.

    """
    if(addr.startswith('[') and not addr.startswith('[::1]')):
        headers = {'Host': f'{addr.split("%")[0]}]'}
    else:
        headers = {}
    return requests.get(f"http://{addr}{endpoint}", headers=headers)

def apiversions(addr: str) -> List[int]:
    """Returns a list of supported Alpaca API version numbers

    Args:
        addr: An `address:port` string from discovery

    Raises:
        AlpacaRequestException: Method or parameter error, internal Alpaca server error

    Note:
        * Currently (April 2022) this will be [1]

    """
    response = __ipv6_safe_get('/management/apiversions', addr)
    __check_error(response)
    j = response.json()["Value"]
    return j

def description(addr: str) -> str:
    """Return a description of the device as a whole (the server)

    Args:
        addr: An `address:port` string from discovery

    Raises:
        AlpacaRequestException: Method or parameter error, internal Alpaca server error

    Note:
        * This is the description of the server at the given `address:port`,
          which may serve multiple Alpaca devices.

    """
    response = __ipv6_safe_get(f'/management/v{API_VERSION}/description', addr)
    __check_error(response)
    j = response.json()["Value"]
    return j

def configureddevices(addr: str) -> List[dict]:
    """Return a list of dictionaries describing each device served by this Alpaca Server

    Each element of the returned list is a dictionary of properties of each Alpaca
    device served by the server at `addr`. The dictionaries consist of the following
    elements:

        :DeviceName: The name of the device

        :DeviceType: The ASCOM standard name for the type of device

        :DeviceNumber: The index of the device among devices of the same type. See Notes.

        :UniqueID: A "globally unique ID" identifying this device

    Args:
        addr: An `address:port` string from discovery

    Raises:
        AlpacaRequestException: Method or parameter error, internal Alpaca server error

    """
    response = __ipv6_safe_get(f'/management/v{API_VERSION}/configureddevices', addr)
    __check_error(response)
    j = response.json()["Value"]
    return j
