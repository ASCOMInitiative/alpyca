# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# focuser - Implements ASCOM Alpaca Focuser device class
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#           Ethan Chappel <ethan.chappel@gmail.com>
#
# Python Compatibility: Requires Python 3.7 or later
# Doc Environment: Sphinx v4.5.0 with autodoc, autosummary, napoleon, and autoenum
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
from typing import List

class Focuser(Device):
    """ASCOM Standard IFocuserV3 Interface

    Attention:
        It is possible to command the focuser to a position exceeding 
        its limits (see notes for :py:attr:`MaxStep`) without receiving
        an exception. This is by design.  TODO [REVIEW]

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
        """The focuser does absolute positioning
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            True means the focuser is capable of absolute position; that is, being 
            commanded to a specific step location. False means this is a
            relative positioning focuser.

        """
        return self._get("absolute")

    @property
    def IsMoving(self) -> bool:
        """The focuser is currently moving to a new position
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * This is the correct property to use to determine *successful* completion of 
              a (non-blocking) :py:meth:`Move()` request. IsMoving will be True 
              immediately upon returning from a :py:meth:`Move()` call, and will 
              remain True until *successful* completion, at which time IsMoving will 
              become False.
        
        """
        return self._get("ismoving")

    @property
    def MaxIncrement(self) -> int:
        """Maximum number of steps allowed in one :py:meth:`Move()` operation. 

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * For most focusers this is the same as the :py:attr:`MaxStep` property. This is
              normally used to limit the increment display in the host software. 

        """
        return self._get("maxincrement")

    @property
    def MaxStep(self) -> int:
        """Maximum step position permitted. 

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * The focuser can step between 0 and MaxStep. If an attempt is made to 
              move the focuser beyond these limits, it will automatically stop at 
              the limit.
 
        """
        return self._get("maxstep")

    @property
    def Position(self) -> int:
        """Current focuser position, in steps.
        
        Raises:
            NotImplementedException: The device is a relative focuser (:py:attr:`Absolute` 
                is False)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * Do not use this as a way to determine if a (non-blocking) :py:meth:`Move()`
              has completed. The Position may transit through the requested position
              before finally settling. Use the :py:attr:`IsMoving` property.
        
        """
        return self._get("position")

    @property
    def StepSize(self) -> int:
        """Step size (microns) for the focuser.
        
         Raises:
            NotImplementedException: If the device does not intrinsically know what
                the step size is.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """
        return self._get("stepsize")

    @property
    def TempComp(self) -> bool:
        """(read/write) Set or indicate the state of the focuser's temp compensation.

        Raises:
            NotImplementedException: On writing to TempComp, if :py:attr:`TempCompAvailable` 
                is False, indicating that this focuser does not have temperature
                compensation. In that case reading TempComp will always return False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Setting TempComp to True puts the focuser into temperature tracking mode; 
              setting it to False will turn off temperature tracking. 
            * If :py:attr:`TempCompAvailable` is False this property will always 
              return False. 
          
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
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("tempcompavailable")

    @property
    def Temperature(self) -> float:
        """Current **ambient** temperature (deg. C).
        
        Raises:
            NotImplementedException: The temperature is not available for this device.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Historically (prior to 2019) no units were specified for this property.
              You should assume this this is in degrees Celsius but old devices may
              supply temperature in other units. By now (2022) however devices should be 
              providing degreed celsius.
        
        """
        return self._get("temperature")

    def Halt(self) -> None:
        """Immediately stop any focuser motion due to a previous :py:meth:`Move()` call.
        
        Raises:
            NotImplementedException: The focuser cannot be programmatically halted.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * You should try to call this method aftr initialization to see if halting is
              supported by your device. You can use this info to possibly disable a Halt
              button in your user interface.

        """
        self._put("halt")

    def Move(self, Position: int) -> None:
        """Starts moving the focuser to a new position
        
        **Non-blocking**: Returns immediately after *successfully* starting the 
        focus change with :py:attr:`IsMoving` = True. See Notes, and :ref:`async_faq`

        **See Notes for details on absolute versus relative focusers**

        Arguments:
            Position: Step distance or absolute position, depending on the 
                value of the :py:attr:`Absolute` property. 
            
        Raises:
            InvalidValueException: TODO [REVIEW] If Position would result in a movement beyond 
                :py:attr:`MaxStep`.
            InvalidOperationException: **IFocuserV2 and earlier only** Raised if 
                :py:attr:`TempComp` is true and a Move() is attempted. This 
                restriction was removed in IFocuserV3, but you must be prepared 
                to catch this for older focusers (2018).
            NotImplementedException: The focuser cannot be programmatically halted.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): The method returns as soon as the focus 
              change operation has been *successfully* started, with the :py:attr:`IsMoving`
              property True. After the requested position is *successfully* reached and 
              motion stops, the :py:attr:`IsMoving` property becomes False. See :ref:`async_faq`
            * If the :py:attr:`Absolute` property is True, then this is an absolute 
              positioning focuser. The :py:meth:`Move()` method tells the focuser to move 
              to an exact step position, and the Position parameter of the :py:meth:`Move()` 
              method is an integer between 0 and :py:attr:`MaxStep`.
            * If the :py:attr:`Absolute` property is False, then this is a relative 
              positioning focuser. The :py:meth:`Move()` method tells the focuser to move 
              in a relative direction. The Position parameter of the :py:meth:`Move()` method
              is actually a *step distance* and is an integer between minus :py:attr:`MaxIncrement`
              and plus :py:attr:`MaxIncrement`.

        """
        self._put("move", Position=Position)
