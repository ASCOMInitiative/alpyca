# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# switch - Implements ASCOM Alpaca Switch class
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
# 13-May-22 (rbd) 2.0.0-dev1 Project now called "Alpyca" - no logic changes
# 01-Jan-23 (rbd) 2.0.4 https://github.com/ASCOMInitiative/alpyca/issues/8
#                 Change 'ID' to 'Id' for switch parameters.
# 05-Mar-24 (rbd) 3.0.0 New members for Platform 7
# 07-Mar-24 (rbd) 3.0.0 Add Master Interfaces refs to all members
# 08-Mar-24 (rbd) 3.0.0 Clarify switch vs driver vs device etc. No
#                 logic changes.
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
        """Initialize the Switch device.

        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "switch", device_number, protocol)

    @property
    def MaxSwitch(self) -> int:
        """Count of switches managed by this device.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Number of switches managed by this device. Switches are numbered from 0
              to MaxSwitch - 1.

        .. admonition:: Master Interfaces Reference
            :class: green

            |MaxSwitch|

            .. |MaxSwitch| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.MaxSwitch" target="_blank">
                Switch.MaxSwitch</a> (external)

        """
        return self._get("maxswitch")

    def CanAsync(self, Id: int) -> bool:
        """The specified switch can operate asynchronously.
        See :py:meth:`SetAsync` and :py:meth:`SetAsyncValue`.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * Examples of switches that cannot be written to include a
              limit switch or a sensor.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanAsync|

            .. |CanAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.CanAsync" target="_blank">
                Switch.CanAsync()</a> (external)

        """
        return self._get("canasync", Id=Id)

    def CancelAsync(self, Id: int) -> None:
        """Cancels an in-progress asynchronous state change operation. See :py:meth:`SetAsync` and
        :py:meth:`SetAsyncValue` for details of asynchronous switch operations.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * On return, the next call to :py:meth:`StateChangeComplete` for this switch
              will raise an :py:class:`OperationCancelledException`; thereafter calls
              to :py:meth:`StateChangeComplete` for the switch will return ``False``.
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CancelAsync|

            .. |CancelAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.CancelAsync" target="_blank">
                Switch.CancelAsync()</a> (external)

        """
        return self._put("cancelasync", Id=Id)

    def CanWrite(self, Id: int) -> bool:
        """The specified switch can be written to.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * Examples of witches that cannot be written to include a
              limit switch or a sensor.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanWrite|

            .. |CanWrite| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.CanWrite" target="_blank">
                Switch.CanWrite()</a> (external)

        """
        return self._get("canwrite", Id=Id)

    def GetSwitch(self, Id: int) -> bool:
        """The state of the specified switch.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * On is True, Off is False.

        .. admonition:: Master Interfaces Reference
            :class: green

            |GetSwitch|

            .. |GetSwitch| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.GetSwitch" target="_blank">
                Switch.GetSwitch()</a> (external)

        """
        return self._get("getswitch", Id=Id)

    def GetSwitchDescription(self, Id: int) -> str:
        """The textual description of the specified switch.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.

        .. admonition:: Master Interfaces Reference
            :class: green

            |GetSwitchDescription|

            .. |GetSwitchDescription| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.GetSwitchDescription" target="_blank">
                Switch.GetSwitchDescription()</a> (external)

        """
        return self._get("getswitchdescription", Id=Id)

    def GetSwitchName(self, Id: int) -> str:
        """The textual name of the specified switch.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.

        .. admonition:: Master Interfaces Reference
            :class: green

            |GetSwitchName|

            .. |GetSwitchName| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.GetSwitchName" target="_blank">
                Switch.GetSwitchName()</a> (external)

        """
        return self._get("getswitchname", Id=Id)

    def GetSwitchValue(self, Id: int) -> float:
        """The value of the specified switch as a float.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.


        .. admonition:: Master Interfaces Reference
            :class: green

            |GetSwitchValue|

            .. |GetSwitchValue| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.GetSwitchValue" target="_blank">
                Switch.GetSwitchValue()</a> (external)

        """
        return self._get("getswitchvalue", Id=Id)

    def MaxSwitchValue(self, Id: int) -> float:
        """The maximum value of the specified switch as a double.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.

        .. admonition:: Master Interfaces Reference
            :class: green

            |MaxSwitchValue|

            .. |MaxSwitchValue| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.MaxSwitchValue" target="_blank">
                Switch.MaxSwitchValue()</a> (external)

        """
        return self._get("maxswitchvalue", Id=Id)

    def MinSwitchValue(self, Id: int) -> float:
        """The minimum value of the specified switch as a double.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.

        .. admonition:: Master Interfaces Reference
            :class: green

            |MinSwitchValue|

            .. |MinSwitchValue| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.MinSwitchValue" target="_blank">
                Switch.MinSwitchValue()</a> (external)

        """
        return self._get("minswitchvalue", Id=Id)

    def SetAsync(self, Id: int, State: bool) -> None:
        """Asynchronouly Set a switch to the specified boolean on/off state.

        Args:
            Id: the specified switch number (see Notes)
            State: The required control state

        Raises:
            NotImplementedException: If :py:meth:`CanAsync` ``= False`` for switch ``Id``
            InvalidValueException: The ``Id`` is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): The method returns as soon as the state change
              operation has been successfully started, with :py:meth:`StateChangeComplete` for
              switch ``Id = False``. After the state change has completed
              :py:meth:`StateChangeComplete` becomes True.
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * On is True, Off is False.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SetAsync|

            .. |SetAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.SetAsync" target="_blank">
                Switch.SetAsync()</a> (external)
        """
        self._put("setasync", Id=Id, State=State)

    def SetAsyncValue(self, Id: int, Value: float) -> None:
        """Asynchronouly Set a switch to the specified value

        Args:
            Id: the specified switch number (see Notes)
            Value: The value to be set, between :py:meth:`MinSwitchValue`` and :py:meth:`MaxSwitchValue`
                for switch ``Id``

        Raises:
            NotImplementedException: If :py:meth:`CanAsync` ``= False`` for switch ``Id``
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`), or if the
                given value is not between :py:meth:`MinSwitchValue` and :py:meth:`MaxSwitchValue`
                for the given switch ``Id``.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): The method returns as soon as the state change
              operation has been successfully started, with :py:meth:`StateChangeComplete` for
              switch ``Id = False``. After the state change has completed
              :py:meth:`StateChangeComplete` becomes True.
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * On is True, Off is False.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SetAsyncValue|

            .. |SetAsyncValue| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.SetAsyncValue" target="_blank">
                Switch.SetAsyncValue()</a> (external)
        """
        self._put("setasyncvalue", Id=Id, Value=Value)

    def SetSwitch(self, Id: int, State: bool) -> None:
        """Set a switch to the specified state

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
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * On is True, Off is False.

        """
        self._put("setswitch", Id=Id, State=State)

    def SetSwitchName(self, Id: int, Name: str) -> None:
        """Set a switch name to the specified value.

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
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * On is True, Off is False.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SetSwitchName|

            .. |SetSwitchName| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.SetSwitchName" target="_blank">
                Switch.SetSwitchName()</a> (external)
        """
        self._put("setswitchname", Id=Id, Name=Name)

    def SetSwitchValue(self, Id: int, Value: float) -> None:
        """Set a switch value to the specified value.

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
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.
            * On is True, Off is False.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SetSwitchValue|

            .. |SetSwitchValue| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.SetSwitchValue" target="_blank">
                Switch.SetSwitchValue()</a> (external)
        """
        self._put("setswitchvalue", Id=Id, Value=Value)

    def StateChangeComplete(self, Id: int) -> bool:
        """True if the last :py:meth:`SetAsync` or :py:meth:`SetAsyncValue`
        has completed and the switch is in the requested state.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            NotImplementedException: If :py:meth:`CanAsync` is ``False`` for switch ``Id``
            OperationCancelledException: If an in-progress state change is cancelled by a call to
                :py:meth:`CancelAsync` call for switch ``Id``
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.

        .. admonition:: Master Interfaces Reference
            :class: green

            |StateChangeComplete|

            .. |StateChangeComplete| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.StateChangeComplete" target="_blank">
                Switch.StateChangeComplete()</a> (external)
        """
        return self._get("statechangecomplete", Id=Id)

    def SwitchStep(self, Id: int) -> float:
        """The step size of the specified switch (see Notes).

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
            * Switches are numbered from 0 to :py:attr:`MaxSwitch` ``- 1``.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SwitchStep|

            .. |SwitchStep| raw:: html

                <a href="https://ascom-standards.org/newdocs/switch.html#Switch.SwitchStep" target="_blank">
                Switch.SwitchStep()</a> (external)
        """
        return self._get("switchstep", Id=Id)
