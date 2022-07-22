# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# switch - Implements ASCOM Alpaca Switch device class
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# Doc Environment: Sphinx v5.0.2 with autodoc, autosummary, napoleon, and autoenum
# GitHub: https://github.com/BobDenny/alpyca-client
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 Ethan Chappel and Bob Denny
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

from alpaca.device import Device

class Switch(Device):
    """ASCOM Standard ISwitch V2 Interface"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize the Switch object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "switch", device_number, protocol)

    @property
    def MaxSwitch(self) -> int:
        """Count of switch devices managed by this driver.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Number of switch devices managed by this driver. Devices are numbered from 0
              to MaxSwitch - 1.
        
        """
        return self._get("maxswitch")

    def CanWrite(self, Id: int) -> bool:
        """The specified switch device can be written to.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switch devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * Examples of witches that cannot be written to include a
              limit switch or a sensor.
        
        """
        return self._get("canwrite", ID=Id)

    def GetSwitch(self, Id: int) -> bool:
        """The state of the specified switch device.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        return self._get("getswitch", ID=Id)

    def GetSwitchDescription(self, Id: int) -> str:
        """The textual description of the specified switch device.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("getswitchdescription", ID=Id)

    def GetSwitchName(self, Id: int) -> str:
        """The textual name of the specified switch device.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("getswitchname", ID=Id)
    
    def GetSwitchValue(self, Id: int) -> float:
        """The value of the specified switch device as a float.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("getswitchvalue", ID=Id)

    def MaxSwitchValue(self, Id: int) -> float:
        """The maximum value of the specified switch device as a double.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("maxswitchvalue", ID=Id)

    def MinSwitchValue(self, Id: int) -> float:
        """The minimum value of the specified switch device as a double.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("minswitchvalue", ID=Id)

    def SetSwitch(self, Id: int, State: bool) -> None:
        """Set a switch device to the specified state

        Args:
            Id: the specified switch number (see Notes)
            State: The required control state

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        self._put("setswitch", ID=Id, State=State)

    def SetSwitchName(self, Id: int, Name: str) -> None:
        """Set a switch device name to the specified value.

        Args:
            Id: the specified switch number (see Notes)
            Name: The desired (new) name for the switch

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        self._put("setswitchname", ID=Id, Name=Name)

    def SetSwitchValue(self, Id: int, Value: float) -> None:
        """Set a switch device value to the specified value.

        Args:
            Id: the specified switch number (see Notes)
            Value: Value to be set, between :py:attr:`MinSwitchValue` and 
                :py:attr:`MinSwitchValue`.

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`), or
                the Value is out of range, not between :py:attr:`MinSwitchValue` and 
                :py:attr:`MinSwitchValue`.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        self._put("setswitchvalue", ID=Id, Value=Value)

    def SwitchStep(self, Id: int) -> float:
        """The step size of the specified switch device (see Notes).

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Step size is the difference between successive values of the device.
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.

        """
        return self._get("switchstep", ID=Id)
