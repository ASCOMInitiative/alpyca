# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# covercalibrator - Implements ASCOM Alpaca CoverCalibrator device class
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
# 04-Jun-22 (rbd) 2.0.0-dev1 Fix capitalization of OpenCover 
# -----------------------------------------------------------------------------

from alpaca.docenum import DocIntEnum
from alpaca.device import Device

class CalibratorStatus(DocIntEnum):
    """Indicates the current status of the calibrator"""
    NotPresent = 0
    Off = 1
    NotReady = 2
    Ready = 3
    Unknown = 4
    Error = 5

class CoverStatus(DocIntEnum):
    """Indicates the current status of the cover"""
    NotPresent = 0
    Closed = 1
    Moving = 2
    Open = 3
    Unknown = 4
    Error = 5

class CoverCalibrator(Device):
    """ASCOM Standard ICoverCalibratorV1 Interface"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize CoverCalibrator object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".
        
        """
        super().__init__(address, "covercalibrator", device_number, protocol)

    @property
    def Brightness(self) -> int:
        """The current calibrator brightness (0 - :py:attr:`MaxBrightness`)
        
        Raises:
            NotImplementedException: When :py:attr:`CalibratorState` is
                :py:class:`~CalibratorStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * The brightness value will be 0 when :py:attr:`CalibratorState` is 
              :py:class:`~CalibratorStatus.Off`
        
        """
        return self._get("brightness")

    @property
    def CalibratorState(self) -> CalibratorStatus:
        """The state of the calibration device

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * If no calibrator is present, the state will be 
              :py:class:`~CalibratorStatus.NotPresent`. You will not receive a
              :py:class:`~alpaca.exceptions.NotImplementedException`. 
            * The brightness value will be 0 when CalibratorState 
              is :py:class:`~CalibratorStatus.Off`
            * The :py:class:`~CalibratorStatus.Unknown` state will only be returned if 
              the device is unaware of the calibrator's state e.g. if the hardware 
              does not report the device's state and the calibrator has just been 
              powered on. You do not need to take special action if this state is 
              returned, you must carry on as usual, calling :py:meth:`CalibratorOn()`
              and :py:meth:`CalibratorOff()` methods as required.
            * If the calibrator hardware cannot report its state, the device might 
              mimic this by recording the last configured state and returning that. 
              Driver authors or device manufacturers may also wish to offer users 
              the capability of powering up in a known state and driving the 
              hardware to this state when :py:attr:`Connected` is set True.
        
        """
        return CalibratorStatus(self._get("calibratorstate"))

    @property
    def CoverState(self) -> CoverStatus:
        """The state of the device cover

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * If no cover is present, the state will be 
              :py:class:`~CoverStatus.NotPresent`. You will not receive a
              :py:class:`~alpaca.exceptions.NotImplementedException`. 
            * The :py:class:`~CoverStatus.Unknown` state will only be returned if 
              the device is unaware of the cover's state e.g. if the hardware 
              does not report the device's state and the cover has just been 
              powered on. You do not need to take special action if this state is 
              returned, you must carry on as usual, calling :py:meth:`OpenCover()`
              and :py:meth:`CloseCover()` methods as required.
            * If the cover hardware cannot report its state, the device might 
              mimic this by recording the last configured state and returning that. 
              Driver authors or device manufacturers may also wish to offer users 
              the capability of powering up in a known state and driving the 
              hardware to this state when :py:attr:`Connected` is set True.

        """
        return CoverStatus(self._get("coverstate"))

    @property
    def MaxBrightness(self) -> int:
        """The Brightness value that makes the calibrator deliver its maximum illumination. 

        Raises:
            NotImplementedException: When :py:attr:`CalibratorState` is
                :py:class:`~CalibratorStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * This is a mandatory property if a calibrator device is present
              (:py:attr:`CalibratorState` is other than 
              :py:class:`~CalibratorStatus.NotPresent`)
            * The value will always be a positive integer, indicating the available
              precision. 
            * Examples: A value of 1 indicates that the calibrator can only be 
              "off" or "on". A value of 10 indicates that the calibrator has 
              10 discrete illumination levels in addition to "off".

        """
        return self._get("maxbrightness")

    def CalibratorOff(self) -> None:
        """Turns the calibrator off if the device has calibration capability 
        
        **Non-blocking**: See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: When :py:attr:`CalibratorState` is
                :py:class:`~CalibratorStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): If the calibrator requires time to safely stabilise 
              after use, :py:class:`CalibratorState` will return :py:class:`~CalibratorStatus.NotReady`. 
              When the calibrator is safely off, :py:class:`CalibratorState` will return 
              :py:class:`~CalibratorStatus.Off`.  See :ref:`async_faq`
            * During the shutdown process, reading :py:class:`CalibratorStatus` may result in a 
              :py:exc:`~alpaca.exceptions.DriverException`.

        """
        self._put("calibratoroff")

    def CalibratorOn(self, BrightnessVal: int) -> None:
        """Turns the calibrator on if the device has calibration capability

        **Non-blocking**: See Notes, and :ref:`async_faq`

        Parameters:
            Brightness: The calibrator illumination brightness to be set

        Raises:
            NotImplementedException: When :py:attr:`CalibratorState` is
                :py:class:`~CalibratorStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): If the calibrator requires time to safely 
              stabilise, :py:class:`CalibratorState` will return
              :py:class:`~CalibratorStatus.NotReady`. 
              When the calibrator is ready for use, :py:class:`CalibratorState` will return 
              :py:class:`~CalibratorStatus.Ready`.  See :ref:`async_faq`
            * If an error condition arises while turning on the calibrator, 
              :py:class:`CalibratorState` will be set to :py:class:`~CalibratorStatus.Error`
              rather than :py:class:`~CalibratorStatus.Unknown`.
            * During the shutdown process, reading :py:class:`CalibratorStatus` may result in a 
              :py:exc:`~alpaca.exceptions.DriverException`.
        
        Attention:
            For devices with both cover and calibrator capabilities, this method may 
            change the :py:class:`CoverState`, if required. This operation is also 
            **asynchronous** (non-blocking) so you may need to wait for :py:class:`CoverState`
            to reach :py:class:`~CoverStatus.Open`. See :ref:`async_faq`

        """
        self._put("calibratoron", Brightness=BrightnessVal)

    def CloseCover(self) -> None:
        """Initiates cover closing if a cover is present 

        **Non-blocking**: See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: When :py:attr:`CoverState` is
                :py:class:`~CoverStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): :py:attr:`CoverState` indicates the 
              status of the operation once CloseCover() returns. It will be 
              :py:class:`~CoverStatus.Moving` immediately after the return of 
              CloseCover(), and will remain as long as the operation is progressing 
              successfully. See :ref:`async_faq`
            * :py:class:`~CoverStatus.Closed` indicates *successful* completion. 
            * If an error condition arises while moving between states, 
              :py:attr:`CoverState` will be set to :py:class:`~CoverStatus.Error`
              rather than :py:class:`~CoverStatus.Unknown`
            
        """
        self._put("closecover")

    def HaltCover(self) -> None:
        """Immediately stops an in-progress :py:meth:`OpenCover()` or :py:meth:`CloseCover()`

        Raises:
            NotImplementedException: When :py:attr:`CoverState` is
                :py:class:`~CoverStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This will  stop any cover movement as soon as possible and 
              set a :py:attr:`CoverState` of :py:class:`~CoverStatus.Open`, 
              :py:class:`~CoverStatus.Closed` or :py:class:`~CoverStatus.Unknown` 
              as appropriate.
            * If cover movement cannot be interrupted, a 
              :py:class:`~alpaca.exceptions.NotImplementedException` will be thrown.

            
        """
        self._put("haltcover")

    def OpenCover(self) -> None:
        """Initiates cover opening if a cover is present 
        
        **Non-blocking**: See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: When :py:attr:`CoverState` is
                :py:class:`~CoverStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): :py:attr:`CoverState` indicates the 
              status of the operation once OpenCover() returns. It will be 
              :py:class:`~CoverStatus.Moving` immediately after the return of 
              OpenCover(), and will remain as long as the operation is progressing 
              successfully.  See :ref:`async_faq`
            * :py:class:`~CoverStatus.Open` indicates *successful* completion. 
            * If an error condition arises while moving between states, 
              :py:attr:`CoverState` will be set to :py:class:`~CoverStatus.Error`
              rather than :py:class:`~CoverStatus.Unknown`
            
        """
        self._put("opencover")

