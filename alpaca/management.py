from typing import List, Any
#import requests
import httpx
from alpaca.exceptions import AlpacaRequestException

API_VERSION = 1

def __check_error(response: httpx.Response) -> None:
    """Check response from Alpaca server for Errors.

    Args:
        response (Response): Response from Alpaca server to check.

    """
    if response.status_code != 200:
        raise AlpacaRequestException(response.status_code, 
                f"{response.text} (URL {response.url})")


def apiversions(addr: str) -> List[int]:
    """Returns a list of supported Alpaca API version numbers
    
    Args:
        addr: An `address:port` string from discovery

    Raises:
        AlpacaRequestException: Method or parameter error, internal Alpaca server error
    
    Notes:
        * Currently (April 2022) this will be [1]

    """
    response = httpx.get(f"http://{addr}/management/apiversions")
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
    response = httpx.get(f"http://{addr}/management/v{API_VERSION}/description")
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
    response = httpx.get(f"http://{addr}/management/v{API_VERSION}/configureddevices")
    __check_error(response)
    j = response.json()["Value"]
    return j
