from typing import List
import requests
from alpaca.exceptions import AlpacaRequestException

API_VERSION = 1

def __check_error(response: requests.Response) -> None:
    """Check response from Alpaca server, raise unless 200

    Args:
        response (Response): Response from Alpaca server to check.

    Notes:
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

        Notes:
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
    
    Notes:
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
    
    Notes:
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
