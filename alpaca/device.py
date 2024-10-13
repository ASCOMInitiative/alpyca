# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# device - Implements ASCOM Alpaca Device superclass
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#           Ethan Chappel <ethan.chappel@gmail.com>
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
# 03-May-22 (rbd) Fix DriverException wording to final agreed text.
# 13-May-22 (rbd) 2.0.0-dev1 Project now called "Alpyca" - no logic changes
# 17-Jul-22 (rbd) 2.0.1rc1 Speed up by re-using ports via requests.Session().
# 21-Jul-22 (rbd) 2.0.1 Resolve TODO reviews
# 21-Aug-22 (rbd) 2.0.2 Fix DriverVersion to return the string GitHub issue #4
# 05-Mar-24 (rbd) 3.0.0 New members for Platform 7
# 06-Mar-24 (rbd) 3.0.0 Add stubbed Master Interfaces refs to all members
# -----------------------------------------------------------------------------

from threading import Lock
from typing import List
import requests
import random
from alpaca.exceptions import *     # Sorry Python purists

API_VERSION = 1

class Device:
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
        self.device_type = device_type.lower()
        self.device_number = device_number
        self.api_version = API_VERSION
        self.base_url = "%s://%s/api/v%d/%s/%d" % (
            protocol,       # not needed later
            self.address,
            self.api_version,
            self.device_type,
            self.device_number
        )
        self.rqs = requests.Session()

    # ------------------------------------------------
    # CLASS VARIABLES - SHARED ACROSS DEVICE INSTANCES
    # ------------------------------------------------
    _client_id = random.randint(0, 65535)
    _client_trans_id = 1
    _ctid_lock = Lock()
    # ------------------------------------------------

    def Action(self, ActionName: str, *Parameters) -> str:
        """Invoke the specified device-specific custom action

        **Common to all devices**

        Args:
            ActionName: A name from :py:attr:`SupportedActions` that represents
                the action to be carried out.
            *Parameters: List of required parameters or [] if none are required.

        Returns:
            String result of the action.

        Raises:
            NotImplementedException: If no actions at all are supported
            ActionNotImplementedException: If the driver does not support the requested
                ActionName. The supported action names are listed in
                :py:attr:`SupportedActions`.
            NotConnectedException: If the device is not connected
            DriverException:An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This method, combined with :py:attr:`SupportedActions`, is the supported
              mechanic for adding non-standard functionality.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``Action()``, find this specific
            device's specification, and see ``Action()`` there.

            .. |master| raw:: html

                <a href="https://ascom-standards.org/newdocs/interfaces.html#ascom-master-interface-definitions" target="_blank">
                ASCOM Master Interface Definitions</a> (external)


        """
        return self._put("action", Action=ActionName, Parameters=Parameters)["Value"]

    def CommandBlind(self, Command: str, Raw: bool) -> None:
        """Transmit an arbitrary string to the device and does not wait for a response.

        **Common to all devices**

        Args:
            Command: The literal command string to be transmitted.
            Raw: If true, command is transmitted 'as-is'.
                If false, then protocol framing characters may be added prior to
                transmission.

        Raises:
            NotImplementedException: If no actions at all are supported
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Attention:
            **Deprecated**, will most likely result in
            :py:exc:`~alpaca.exceptions.NotImplementedException`

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``CommandBlind()``, find this specific
            device's specification, and see ``CommandBlind()`` there.

        """
        self._put("commandblind", Command=Command, Raw=Raw)

    def CommandBool(self, Command: str, Raw: bool) -> bool:
        """Transmit an arbitrary string to the device and wait for a boolean response.

        **Common to all devices**

        Returns:
            The True/False response from the command

        Args:
            Command: The literal command string to be transmitted.
            Raw: If true, command is transmitted 'as-is'.
                If false, then protocol framing characters may be added prior to
                transmission.

        Raises:
            NotImplementedException: If no actions at all are supported
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Attention:
            **Deprecated**, will most likely result in
            :py:exc:`~alpaca.exceptions.NotImplementedException`

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``CommandBool()``, find this specific
            device's specification, and see ``CommandBool()`` there.

        """
        return self._put("commandbool", Command=Command, Raw=Raw)["Value"]

    def CommandString(self, Command: str, Raw: bool) -> str:
        """Transmit an arbitrary string to the device and wait for a string response.

        **Common to all devices**

        Returns:
            The string response from the command

        Args:
            Command: The literal command string to be transmitted.
            Raw: If true, command is transmitted 'as-is'.
                If false, then protocol framing characters may be added prior to
                transmission.

        Raises:
            NotImplementedException: If no actions at all are supported
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Attention:
            **Deprecated**, will most likely result in
            :py:exc:`~alpaca.exceptions.NotImplementedException`

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``CommandString()``, find this specific
            device's specification, and see ``CommandString()`` there.

        """
        return self._put("commandstring", Command=Command, Raw=Raw)["Value"]

    def Connect(self) -> None:
        """Connect to the device **asynchronously**.

        **Common to all devices**

        Returns:
            Nothing

        Raises:
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            **Non-Blocking** Use :py:attr:`Connecting` to indicate completion.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``Connect()``, find this specific
            device's specification, and see ``Connect()`` there.

        """
        return self._put("connect")

    def Disconnect(self) -> None:
        """Disconnect from the device **asynchronously**.

        **Common to all devices**

        Returns:
            Nothing

        Raises:
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            **Non-Blocking** Use :py:attr:`~Device.Connecting` to indicate completion.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``Disconnect()``, find this specific
            device's specification, and see ``Disconnect()`` there.

        """
        return self._put("disconnect")

    @property
    def Connecting(self) -> bool:
        """Returns ``True`` while the device is undertaking an asynchronous
        :py:meth:`Connect` or :py:meth:`Disconnect` operation.

        **Common to all devices**

        Raises:
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Use this property to determine when an (async)
              :py:meth:`Connect` or :py:meth:`Disconnect` has completed,
              at which time it will transition from ``True`` to ``False``.
            * Present only in Platform 7 (2024) devices. Check the device's
              :py:attr:`InterfaceVersion`.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``Connecting``, find this specific
            device's specification, and see ``Connecting`` there.

        """
        return self._get("connecting")

    @property
    def Connected(self) -> bool:
        """(Read/Write) Retrieve or set the connected state of the device.

        **Common to all devices**

        Set True to connect to the device hardware. Set False to disconnect
        from the device hardware. You can also read the property to check
        whether it is connected. This reports the current hardware state.
        See Notes below.

        Raises:
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * The ``Connected`` property sets and reports the state of connection to
              the device hardware. For a hub this means that ``Connected`` will be
              ``True`` when the first driver connects and will only be set to False
              when all drivers have disconnected. A second driver may find that
              ``Connected`` is already ``True`` and setting ``Connected`` to False does not
              report ``Connected`` as False. This is not an error because the physical
              state is that the hardware connection is still ``True``.
            * Multiple calls setting ``Connected`` to ``True`` or false will not cause
              an error.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``Connected``, find this specific
            device's specification, and see ``Connected`` there.

        """
        return self._get("connected")
    @Connected.setter
    def Connected(self, ConnectedState: bool):
        self._put("connected", Connected=ConnectedState)

    @property
    def Description(self) -> str:
        """Description of the **device** such as manufacturer and model number.

        **Common to all devices**

        Raises:
            NotConnectedException: If the device status is unavailable
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * This describes the *device*, not the driver. See the :py:attr:`DriverInfo`
              property for information on the ASCOM driver.
            * The description length will be a maximum of 64 characters so
              that it can be used in FITS image headers, which are limited
              to 80 characters including the header name.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``Description``, find this specific
            device's specification, and see ``Description`` there.

        """
        return self._get("description")

    @property
    def DeviceState(self) ->List[dict]:
        """List of key-value pairs representing the operational properties
        of the device

        **Common to all devices**

        Raises:
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``DeviceState``, find this specific
            device's specification, and see ``DeviceState`` there.

        """
        response = self._get("devicestate")
        return response

    @property
    def DriverInfo(self) -> List[str]:
        """Descriptive and version information about the ASCOM **driver**

        **Common to all devices**

        Returns:
            Python list of strings (see Notes)

        Raises:
            DriverException:An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This describes the *driver* not the device. See the :py:attr:`Description`
              property for information on the device itself
            * The return is a Python list of strings, the total length of which may be
              hundreds to thousands of characters long. It is intended to display
              detailed information on the ASCOM (COM or Alpaca) driver, including
              version and copyright data. . To get the driver version in a parse-able
              string, use the :py:attr:`DriverVersion` property.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``DriverInfo``, find this specific
            device's specification, and see ``DriverInfo`` there.

        """
        return [i.strip() for i in self._get("driverinfo").split(",")]

    @property
    def DriverVersion(self) -> str:
        """String containing only the major and minor version of the *driver*.

        **Common to all devices**

        Raises:
            DriverException:An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This must be in the form "n.n". It should not to be confused with the
              :py:attr:`InterfaceVersion` property, which is the version of this
              specification supported by the driver. **Note:** on systems with a comma
              as the decimal point you may need to make accommodations to parse the
              value.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``DriverVersion``, find this specific
            device's specification, and see ``DriverVersion`` there.

        """
        return self._get("driverversion")

    @property
    def InterfaceVersion(self) -> int:
        """ASCOM Device interface definition version that this device supports.

        **Common to all devices**

        Raises:
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * This is a single integer indicating the version of this specific
              ASCOM universal interface definition. For example, for ICameraV3,
              this will be 3. It should not to be confused with the
              :py:attr:`DriverVersion` property, which is the major.minor version
              of the driver for  this device.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``InterfaceVersion``, find this specific
            device's specification, and see ``InterfaceVersion`` there.

        """
        return int(self._get("interfaceversion"))

    @property
    def Name(self) -> str:
        """The short name of the *driver*, for display  purposes.

        **Common to all devices**

        Raises:
            DriverException: If the driver cannot *successfully* complete the request.
                This exception may be encountered on any call to the device.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``Name``, find this specific
            device's specification, and see ``Name`` there.

        """
        return self._get("name")

    @property
    def SupportedActions(self) -> List[str]:
        """The list of custom action names supported by this driver

        **Common to all devices**

        Returns:
            Python list of strings (see Notes)

        Raises:
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * This method, combined with :py:meth:`Action`, is the supported
              mechanic for adding non-standard functionality.
            * SupportedActions is a "discovery" mechanism that enables clients to know
              which Actions a device supports without having to exercise the Actions
              themselves. This mechanism is necessary because there could be
              people / equipment safety issues if actions are called unexpectedly
              or out of a defined process sequence. It follows from this that
              SupportedActions must return names that match the spelling of
              :py:meth:`Action`
              names exactly, without additional descriptive text. However, returned
              names may use any casing because the ActionName parameter of
              :py:meth:`Action` is case insensitive.

        .. admonition:: Master Interfaces Reference
            :class: green

            Alpyca uses a common Device class but this is not available in the
            |master|. To see the reference info for ``SupportedActions``, find this specific
            device's specification, and see ``SupportedActions`` there.

        """
        return self._get("supportedactions")

# ========================
# HTTP/JSON Communications
# ========================

    def _get(self, attribute: str, tmo=5.0, **data) -> str:
        """Send an HTTP GET request to an Alpaca server and check response for errors.

        Args:
            attribute (str): Attribute to get from server.
            tmo (optional) Timeout for HTTP (default = 5 sec)
            **data: Data to send with request.

        """
        # Make Host: header safe for IPv6
        if(self.address.startswith('[') and not self.address.startswith('[::1]')):
            hdrs = {'Host': f'{self.address.split("%")[0]}]'}
        else:
            hdrs = {}
        pdata = {
                "ClientTransactionID": f"{Device._client_trans_id}",
                "ClientID": f"{Device._client_id}"
                }
        pdata.update(data)
        # TODO - Catch and handle connect failures nicely
        try:
            Device._ctid_lock.acquire()
            response = self.rqs.get("%s/%s" % (self.base_url, attribute),
                            params=pdata, timeout=tmo, headers=hdrs)
            Device._client_trans_id += 1
        finally:
            Device._ctid_lock.release()
        self.__check_error(response)
        return response.json()["Value"]

    def _put(self, attribute: str, tmo=5.0, **data) -> str:
        """Send an HTTP PUT request to an Alpaca server and check response for errors.

        Args:
            attribute (str): Attribute to put to server.
            tmo (optional) Timeout for HTTP (default = 5 sec)
            **data: Data to send with request.

        """
        # Make Host: header safe for IPv6
        if(self.address.startswith('[') and not self.address.startswith('[::1]')):
            hdrs = {'Host': f'{self.address.split("%")[0]}]'}
        else:
            hdrs = {}
        pdata = {
                "ClientTransactionID": f"{Device._client_trans_id}",
                "ClientID": f"{Device._client_id}"
                }
        pdata.update(data)
        # TODO - Catch and handle connect failures nicely
        try:
            Device._ctid_lock.acquire()
            response = self.rqs.put("%s/%s" % (self.base_url, attribute),
                            data=pdata, timeout=tmo, headers=hdrs)
            Device._client_trans_id += 1
        finally:
            Device._ctid_lock.release()
        self.__check_error(response)
        return response.json()

    def __check_error(self, response) -> None:
        """Alpaca exception handler (ASCOM exception types)

        Args:
            response (Response): Response from Alpaca server to check.

        Notes:
            * Depending on the error number, the appropriate ASCOM exception type
              will be raised. See the ASCOM Alpaca API Reference for the reserved
              error codes and their corresponding exceptions. NOTE that DriverException
              and AlpacaRequestException take error code and message.
            * If an unassigned error code in the range 0x400 <= code <= 0x4FF
              is received, a DriverException will also be raised.


        """
        if response.status_code in range(200, 204):
            j = response.json()
            n = j["ErrorNumber"]
            m = j["ErrorMessage"]
            if n != 0:
                if n == 0x0400:
                    raise NotImplementedException(m)
                elif n == 0x0401:
                    raise InvalidValueException(m)
                elif n == 0x0402:
                    raise ValueNotSetException(m)
                elif n == 0x0407:
                    raise NotConnectedException(m)
                elif n == 0x0408:
                    raise ParkedException(m)
                elif n == 0x0409:
                    raise SlavedException(m)
                elif n == 0x040B:
                    raise InvalidOperationException(m)
                elif n == 0x040c:
                    raise ActionNotImplementedException(m)
                elif n == 0x40e:
                    raise OperationCancelledException(m)
                elif n >= 0x500 and n <= 0xFFF:
                    raise DriverException(n, m)
                else: # unknown 0x400-0x4FF
                    # raise UndefinedAscomException(n, m)
                    raise DriverException(n, m) # Outside 0x500-0x5FF but agreed on this
        else:
            raise AlpacaRequestException(response.status_code, f"{response.text} (URL {response.url})")



