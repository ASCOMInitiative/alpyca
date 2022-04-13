from enum import Enum
from threading import Lock
from datetime import datetime
from typing import List, Any
import dateutil.parser
import requests
import random
from alpaca.exceptions import *     # Sorry Python purists

API_VERSION = 1

class Device(object):
    """Common interface members across all ASCOM Alpaca devices."""

    def __init__(
        self,
        address: str,
        device_type: str,
        device_number: int,
        protocol: str
    ):
        """Initialize Device object.
        
        Attributes:
            address: Domain name or IP address of Alpaca server.
                Can also specify port number if needed.
            device_type: One of the recognised ASCOM device types
                e.g. telescope (must be lower case).
            device_number: Zero based device number as set on the server (0 to
                4294967295).
            protocol: Protocol (http vs https) used to communicate with Alpaca server.
            api_version: Alpaca API version.
            base_url: Basic URL to easily append with commands.

        Notes: Sets a random number for ClientID that lasts 

        """
        self.address = address
        self.device_type = device_type
        self.device_number = device_number
        self.api_version = API_VERSION
        self.base_url = "%s://%s/api/v%d/%s/%d" % (
            protocol,       # not needed later
            self.address,
            self.api_version,
            self.device_type,
            self.device_number
        )
    # ------------------------------------------------
    # CLASS VARIABLES - SHARED ACROSS DEVICE INSTANCES
    # ------------------------------------------------
    _client_id = random.randint(0, 65535)
    _client_trans_id = 1
    _ctid_lock = Lock()
    # ------------------------------------------------

    def Action(self, ActionString: str, *Parameters) -> str:
        """Access functionality beyond the built-in capabilities of the ASCOM device interfaces.
        
        Args:
            ActionString (str): A well known name that represents the action to be carried out.
            *Parameters: List of required parameters or empty if none are required.

        Returns:
            Result (str) of the action.

        """
        return self._put("action", Action=ActionString, Parameters=Parameters)["Value"]

    def CommandBlind(self, Command: str, Raw: bool) -> None:
        """Transmit an arbitrary string to the device and does not wait for a response.

        Notes:
            Deprecated

        Args:
            Command (str): The literal command string to be transmitted.
            Raw (bool): If true, command is transmitted 'as-is'.
                If false, then protocol framing characters may be added prior to
                transmission.

        """
        self._put("commandblind", Command=Command, Raw=Raw)

    def CommandBool(self, Command: str, Raw: bool) -> bool:
        """Transmit an arbitrary string to the device and wait for a boolean response.
        
        Notes:
            Deprecated

        Args:
            Command (str): The literal command string to be transmitted.
            Raw (bool): If true, command is transmitted 'as-is'.
                If false, then protocol framing characters may be added prior to
                transmission.

        Returns:
            The boolean response from the device

        """
        return self._put("commandbool", Command=Command, Raw=Raw)["Value"]

    def CommandString(self, Command: str, Raw: bool) -> str:
        """Transmit an arbitrary string to the device and wait for a string response.

        Notes: 
            Deprecated

        Args:
            Command (str): The literal command string to be transmitted.
            Raw (bool): If true, command is transmitted 'as-is'.
                If false, then protocol framing characters may be added prior to
                transmission.
            
        Returns:
            The string response from the device

        """
        return self._put("commandstring", Command=Command, Raw=Raw)["Value"]

    @property
    def Connected(self) -> bool:
        """Retrieve or set the connected state of the device.

        Args:
            Connected (bool): Set True to connect to device hardware.
                Set False to disconnect from device hardware.
        
        """
        return self._get("connected")
    @Connected.setter
    def Connected(self, ConnectedState: bool):
        self._put("connected", Connected=ConnectedState)
    
    @property
    def Description(self) -> str:
        """Get description of the device."""
        return self._get("description")

    @property
    def DriverInfo(self) -> List[str]:
        """Get information of the device."""
        return [i.strip() for i in self._get("driverinfo").split(",")]

    @property
    def DriverVersion(self) -> float:
        """Get string containing only the major and minor version of the driver."""
        return float(self._get("driverversion"))

    @property
    def InterfaceVersion(self) -> int:
        """ASCOM Device interface version number that this device supports."""
        return int(self._get("interfaceversion"))
    
    @property
    def Name(self) -> str:
        """Get name of the device."""
        return self._get("name")

    @property
    def SupportedActions(self) -> List[str]:
        """Get list of action names supported by this driver."""
        return self._get("supportedactions")

# ========================
# HTTP/JSON Communications
# ========================

    def _get(self, attribute: str, **data) -> str:
        """Send an HTTP GET request to an Alpaca server and check response for errors.

        Args:
            attribute (str): Attribute to get from server.
            **data: Data to send with request.
        
        """
        url = f"{self.base_url}/{attribute}"
        pdata = {
                "ClientTransactionID": f"{Device._client_trans_id}",
                "ClientID": f"{Device._client_id}" 
                }
        pdata.update(data)
        try:
            Device._ctid_lock.acquire()
            response = requests.get("%s/%s" % (self.base_url, attribute), params = pdata)
            Device._client_trans_id += 1
        finally:
            Device._ctid_lock.release()
        self.__check_error(response)
        return response.json()["Value"]

    def _put(self, attribute: str, **data) -> str:
        """Send an HTTP PUT request to an Alpaca server and check response for errors.

        Args:
            attribute (str): Attribute to put to server.
            **data: Data to send with request.
        
        """
        url = f"{self.base_url}/{attribute}"
        pdata = {
                "ClientTransactionID": f"{Device._client_trans_id}",
                "ClientID": f"{Device._client_id}" 
                }
        pdata.update(data)
        try:
            Device._ctid_lock.acquire()
            response = requests.put("%s/%s" % (self.base_url, attribute), data=pdata)
            Device._client_trans_id += 1
        finally:
            Device._ctid_lock.release()
        self.__check_error(response)
        return response.json()  # TODO Is this right? json()?

    def __check_error(self, response: requests.Response) -> None:
        """Alpaca exception handler (ASCOM exception types)

        Args:
            response (Response): Response from Alpaca server to check.

        Notes:
            Depending on the error number, the appropriate ASCOM exception type
            will be raised. See the ASCOM Alpaca API Reference for the reserved
            error codes and their corresponding exceptions.

        """
        if response.status_code in range(200, 204):
            j = response.json()
            n = j["ErrorNumber"]
            m = j["ErrorMessage"]
            if n != 0:
                if n == 0x0400:
                    raise NotImplementedException(n, m)
                elif n == 0x0401:
                    raise InvalidValueException(n, m)
                elif n == 0x0402:
                    raise ValueNotSetException(n, m)
                elif n == 0x0407:
                    raise NotConnectedException(n, m)
                elif n == 0x0408:
                    raise ParkedException(n, m)
                elif n == 0x0409:
                    raise SlavedException(n, m)
                elif n == 0x040B:
                    raise InvalidOperationException(n, m)
                elif n == 0x040c:
                    raise ActionNotImplementedException(n, m)
                elif n >= 0x500 and n <= 0xFFF:
                    raise DriverException(n, m)
                else: # unknown 0x400-0x4FF
                    raise UnknownAscomException(n, m)
        else:
            raise AlpacaRequestException(response.status_code, f"{response.text} (URL {response.url})")



