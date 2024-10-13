# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# filterwheel - Implements ASCOM Alpaca FilterWheel device class
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
# 13-May-22 (rbd) 2.0.0-dev1 Project now called "Alpyca" - no logic changes
# 08-Mar-24 (rbd) 3.0.0 Add Master Interfaces refs to all members
# -----------------------------------------------------------------------------

from alpaca.device import Device
from typing import List

class FilterWheel(Device):
    """ASCOM Standard IFilterWheelV2 interface."""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize FilterWheel object.

        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "filterwheel", device_number, protocol)

    @property
    def FocusOffsets(self) -> List[int]:
        """List of filter focus offsets for each filter in the wheel

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * The offset values in this list are in the same order as the filters in the wheel
            * The number of available filters can be determined from the length of the list.
            * If focuser offsets are not available, then the list will contain zeroes.

        .. admonition:: Master Interfaces Reference
            :class: green

            |FocusOffsets|

            .. |FocusOffsets| raw:: html

                <a href="https://ascom-standards.org/newdocs/filterwheel.html#FilterWheel.FocusOffsets" target="_blank">
                FilterWheel.FocusOffsets</a> (external)
        """
        return self._get("focusoffsets")

    @property
    def Names(self) -> List[str]:
        """List of filter names for each filter in the wheel

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * The names in this lisat are in the same order as the filters in the wheel
            * The number of available filters can be determined from the length of the list.
            * If focuser offsets are not available, then the lost will contain generic names
              of 'Filter 1', 'Filter 2', etc.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Names|

            .. |Names| raw:: html

                <a href="https://ascom-standards.org/newdocs/filterwheel.html#FilterWheel.Names" target="_blank">
                FilterWheel.Names</a> (external)
        """
        return self._get("names")

    @property
    def Position(self) -> int:
        """(Read/Write) Start a change to, or return the filter wheel position (zero-based)

        **Non-blocking**: Returns immediately upon writing to change the filter
        with Position = -1 if the operation has been *successfully* started. See Notes,
        and :ref:`async_faq`

        Raises:
            InvalidValueException: If an invalid filter number is written to Position.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            **Asynchronous** (non-blocking): Writing to Position returns as soon as the
            filter change operation has been *successfully* started. Position
            will return -1 while the change is in progress. After the requested position
            has been *successfully* reached and motion stops, Position will
            return the requested new filter number.  See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            |Position|

            .. |Position| raw:: html

                <a href="https://ascom-standards.org/newdocs/filterwheel.html#FilterWheel.Position" target="_blank">
                FilterWheel.Position</a> (external)
        """
        return self._get("position")
    @Position.setter
    def Position(self, Position: int):
        self._put("position", Position=Position)

