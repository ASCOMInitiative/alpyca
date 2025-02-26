# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# focuser - Implements ASCOM Alpaca Focuser device class
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
# 21-Jul-22 (rbd) 2.0.1 Resolve TODO reviews
# 07-Nov-22 (rbd) 2.0.3 Focuser.Stepsize is a float (GitHub issue #7)
# 08-Mar-24 (rbd) 3.0.0 Add Master Interfaces refs to all members
# 22-Nov-24 (rbd) 3.0.1 For PDF rendering no change to logic
# -----------------------------------------------------------------------------

from alpaca.device import Device
from typing import List

class Focuser(Device):
    """ASCOM Standard IFocuserV3 Interface

    Attention:
        It is possible to command the focuser to a position exceeding
        its limits (see notes for :attr:`MaxStep`) without receiving
        an exception. This is by design.

    """
    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize Focuser object.

        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "focuser", device_number, protocol)


    @property
    def Absolute(self) -> bool:
        """The focuser does absolute positioning. See :meth:`Move`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            True means the focuser is capable of absolute position; that is, being
            commanded to a specific step location. False means this is a
            relative positioning focuser.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Absolute|

                .. |Absolute| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.Absolute" target="_blank">
                    Focuser.Absolute</a> (external)

            .. only:: rinoh

                `Focuser.Absolute <https://ascom-standards.org/newdocs/focuser.html#Focuser.Absolute>`_
        """
        return self._get("absolute")

    @property
    def IsMoving(self) -> bool:
        """The focuser is currently moving to a new position

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is the correct property to use to determine *successful* completion of
              a (non-blocking) :meth:`Move` request. IsMoving will be True
              immediately upon returning from a :meth:`Move` call, and will
              remain True until *successful* completion, at which time ``IsMoving`` will
              become False.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |IsMoving|

                .. |IsMoving| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.IsMoving" target="_blank">
                    Focuser.IsMoving</a> (external)

            .. only:: rinoh

                `Focuser.IsMoving <https://ascom-standards.org/newdocs/focuser.html#Focuser.IsMoving>`_
        """
        return self._get("ismoving")

    @property
    def MaxIncrement(self) -> int:
        """Maximum number of steps allowed in one :meth:`Move()` operation.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * For most focusers this is the same as the :attr:`MaxStep` property. This is
              normally used to limit the increment display in the host software.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |MaxIncrement|

                .. |MaxIncrement| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.MaxIncrement" target="_blank">
                    Focuser.MaxIncrement</a> (external)

            .. only:: rinoh

                `Focuser.MaxIncrement <https://ascom-standards.org/newdocs/focuser.html#Focuser.MaxIncrement>`_
        """
        return self._get("maxincrement")

    @property
    def MaxStep(self) -> int:
        """Maximum step position permitted.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * The focuser can step between 0 and MaxStep. If an attempt is made to
              move the focuser beyond these limits, it will automatically stop at
              the limit.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |MaxStep|

                .. |MaxStep| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.MaxStep" target="_blank">
                    Focuser.MaxStep</a> (external)

            .. only:: rinoh

                `Focuser.MaxStep <https://ascom-standards.org/newdocs/focuser.html#Focuser.MaxStep>`_
        """
        return self._get("maxstep")

    @property
    def Position(self) -> int:
        """Current focuser position, in steps.

        Raises:
            NotImplementedException: The device is a relative focuser (:attr:`Absolute`
                is False)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Do not use this as a way to determine if a (non-blocking) :meth:`Move()`
              has completed. The Position may transit through the requested position
              before finally settling. Use the :attr:`IsMoving` property.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Position|

                .. |Position| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.Position" target="_blank">
                    Focuser.Position</a> (external)

            .. only:: rinoh

                `Focuser.Position <https://ascom-standards.org/newdocs/focuser.html#Focuser.Position>`_
        """
        return self._get("position")

    @property
    def StepSize(self) -> float:
        """Step size (microns) for the focuser.

        Raises:
            NotImplementedException: If the device does not intrinsically
                know what the step size is.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |StepSize|

                .. |StepSize| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.StepSize" target="_blank">
                    Focuser.StepSize</a> (external)

            .. only:: rinoh

                `Focuser.StepSize <https://ascom-standards.org/newdocs/focuser.html#Focuser.StepSize>`_
        """
        return self._get("stepsize")

    @property
    def TempComp(self) -> bool:
        """(read/write) Set or indicate the state of the focuser's temp compensation.

        Raises:
            NotImplementedException: On writing to TempComp, if :attr:`TempCompAvailable`
                is False, indicating that this focuser does not have temperature
                compensation. In that case reading TempComp will always return False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Setting TempComp to True puts the focuser into temperature tracking mode;
              setting it to False will turn off temperature tracking.
            * If :attr:`TempCompAvailable` is False this property will always
              return False.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |TempComp|

                .. |TempComp| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.TempComp" target="_blank">
                    Focuser.TempComp</a> (external)

            .. only:: rinoh

                `Focuser.TempComp <https://ascom-standards.org/newdocs/focuser.html#Focuser.TempComp>`_
        """
        return self._get("tempcomp")
    @TempComp.setter
    def TempComp(self, TempCompState: bool):
        self._put("tempcomp", TempComp=TempCompState)

    @property
    def TempCompAvailable(self) -> bool:
        """If focuser has temperature compensation available.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |TempCompAvailable|

                .. |TempCompAvailable| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.TempCompAvailable" target="_blank">
                    Focuser.TempCompAvailable</a> (external)

            .. only:: rinoh

                `Focuser.TempCompAvailable <https://ascom-standards.org/newdocs/focuser.html#Focuser.TempCompAvailable>`_
        """
        return self._get("tempcompavailable")

    @property
    def Temperature(self) -> float:
        """Current **ambient** temperature (deg. C).

        Raises:
            NotImplementedException: The temperature is not available for this device.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Historically (prior to 2019) no units were specified for this property.
              You should assume this this is in degrees Celsius but old devices may
              supply temperature in other units. By now (2022) however devices should be
              providing degrees celsius.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Temperature|

                .. |Temperature| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.Temperature" target="_blank">
                    Focuser.Temperature</a> (external)

            .. only:: rinoh

                `Focuser.Temperature <https://ascom-standards.org/newdocs/focuser.html#Focuser.Temperature>`_
        """
        return self._get("temperature")

    def Halt(self) -> None:
        """Immediately stop any focuser motion due to a previous :meth:`Move` call.

        Raises:
            NotImplementedException: The focuser cannot be programmatically halted.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * You should try to call this method aftr initialization to see if halting is
              supported by your device. You can use this info to possibly disable a Halt
              button in your user interface.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Halt|

                .. |Halt| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.Halt" target="_blank">
                    Focuser.Halt()</a> (external)

            .. only:: rinoh

                `Focuser.Halt() <https://ascom-standards.org/newdocs/focuser.html#Focuser.Halt>`_
        """
        self._put("halt")

    def Move(self, Position: int) -> None:
        """Starts moving the focuser to a new position

        **Non-blocking**: Returns immediately after *successfully* starting the
        focus change with :attr:`IsMoving` = True. See Notes, and :ref:`async_faq`

        **See Notes for details on absolute versus relative focusers**

        Arguments:
            Position: Step distance or absolute position, depending on the
                value of the :attr:`Absolute` property.

        Raises:
            InvalidValueException: If Position would result in a movement beyond
                :attr:`MaxStep`.
            InvalidOperationException: **IFocuserV2 and earlier only** Raised if
                :attr:`TempComp` is true and a Move() is attempted. This
                restriction was removed in IFocuserV3, but you must be prepared
                to catch this for older focusers (2018).
            NotImplementedException: The focuser cannot be programmatically halted.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking): The method returns as soon as the focus
              change operation has been *successfully* started, with the :attr:`IsMoving`
              property True. After the requested position is *successfully* reached and
              motion stops, the :attr:`IsMoving` property becomes False. See :ref:`async_faq`
            * If the :attr:`Absolute` property is True, then this is an absolute
              positioning focuser. The :meth:`Move()` method tells the focuser to move
              to an exact step position, and the Position parameter of the :meth:`Move()`
              method is an integer between 0 and :attr:`MaxStep`.
            * If the :attr:`Absolute` property is False, then this is a relative
              positioning focuser. The :meth:`Move()` method tells the focuser to move
              in a relative direction. The Position parameter of the :meth:`Move()` method
              is actually a *step distance* and is an integer between minus :attr:`MaxIncrement`
              and plus :attr:`MaxIncrement`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Move|

                .. |Move| raw:: html

                    <a href="https://ascom-standards.org/newdocs/focuser.html#Focuser.Move" target="_blank">
                    Focuser.Move()</a> (external)

            .. only:: rinoh

                `Focuser.Move() <https://ascom-standards.org/newdocs/focuser.html#Focuser.Move>`_
        """
        self._put("move", Position=Position)
