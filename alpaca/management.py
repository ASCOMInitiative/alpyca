from typing import List, Any
from typing import List, Any
import requests

API_VERSION = 1

def __check_error(self, response: requests.Response) -> None:
    """Check response from Alpaca server for Errors.

    Args:
        response (Response): Response from Alpaca server to check.

    """
    j = response.json()
    if j["ErrorNumber"] != 0:
        raise NumericError(j["ErrorNumber"], j["ErrorMessage"])
    elif response.status_code == 400 or response.status_code == 500:
        raise ErrorMessage(j["Value"])

def apiversions(addr: str) -> List[str]:
    response = requests.get(f"http://{addr}/management/apiversions")
    j = response.json()["Value"]
    return j

def description(addr: str) -> str:
    response = requests.get(f"http://{addr}/management/v{API_VERSION}/description")
    j = response.json()["Value"]
    return j

def configureddevices(addr: str) -> List[str]:
    response = requests.get(f"http://{addr}/management/v{API_VERSION}/configureddevices")
    j = response.json()["Value"]
    return j
