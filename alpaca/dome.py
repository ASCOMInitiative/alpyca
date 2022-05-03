# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# dome - Implements ASCOM Alpaca dome device class
#
# Part of the Alpyca Client application interface package
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
# -----------------------------------------------------------------------------

from alpaca.docenum import DocIntEnum
from alpaca.device import Device
from typing import List

class ShutterState(DocIntEnum):
    """Indicates the current state of the shutter or roof"""
    shutterOpen = 0, 'The shutter or roof is open'
    shutterClosed = 1, 'The shutter or roof is closed'
    shutterOpening = 2, 'The shutter or roof is opening'
    shutterClosing = 3, 'The shutter or roof is closing'
    shutterError = 4, 'The shutter or roof has encountered a problem'

class Dome(Device):
    """**ASCOM Standard IDomeV2 Interface**"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize Dome object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".
        
        Raises:
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        super().__init__(address, "dome", device_number, protocol)

    @property
    def Altitude(self) -> float:
        """Dome altitude (degrees) of the opening to the sky. 

        Raises:
            NotImplementedException: If the dome does not support vertical (altitude)
                control / placement of its observing opening (including a roll-off roof).
                In this case :py:attr:`CanSetAltitude` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * The specified altitude (*referenced to the dome center/equator*) is of the 
              opening to the sky through which the optics receive light.
            * It is up to the dome control and driver to determine how best to locate the 
              dome aperture in order to expose the specified alt/az area to the sky,
              including positioning clamshell leaves, split shutters, etc. Your app
              need not know how this is happening, just that the alt/az area of the sky
              will be visible.
            * Do not use Altitude as a way to determine if a (non-blocking) 
              :py:meth:`SlewToAltitude()` has completed. The Altitude may transit through 
              the requested position before finally settling, and may be slightly off
              when it stops. Use the :py:attr:`Slewing` property.
      
        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control 
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :py:attr:`Slaved` property for details 
            on slaving (telescope motion tracking).  Only an *integrated* mount/dome system
            will offer both a Telescope and a Dome interface, and be capable of slaving.
        
        """
        return self._get("altitude")

    @property
    def AtHome(self) -> bool:
        """The dome is in the home position.

        Notes:
            This is normally used following a findhome() operation. The value is reset
            with any azimuth slew operation that moves the dome away from the home
            position. athome() may also become true durng normal slew operations, if the
            dome passes through the home position and the dome controller hardware is
            capable of detecting that; or at the end of a slew operation if the dome
            comes to rest at the home position.

        Returns:
            True if dome is in the home position.
        
        """
        return self._get("athome")

    @property
    def AtPark(self) -> bool:
        """The telescope has *successfully* reached its park position.

        Raises:
            NotImplementedException: If the dome does not support parking.
                In this case :py:attr:`CanPark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            Set only following a park() operation and reset with any slew operation.

        Returns:
            True if the dome is in the programmed park position.

        """
        return self._get("atpark")

    @property
    def Azimuth(self) -> float:
        """Dome azimuth (degrees) of the opening to the sky

        TODO - Clarify  that this does not include the geometric transformations needed 
        for mount and optics configurations. See notes and attention. 

        Raises:
            NotImplementedException: If the dome does not support directional (azimuth)
                control / placement of its observing opening (including roll-off roof).
                In this case :py:attr:`CanSetAzimuth` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Azimuth has the usual sense of True North zero and increasing clockwise
              i.e. 90 East, 180 South, 270 West.
            * The specified azimuth (*referenced to the dome center/equator*) is of the 
              opening to the sky through which the optics receive light.
            * You can detect a roll-off roof by :py:attr:`CanSetAzimuth` being False.
            * It is up to the dome control and driver to determine how best to locate the 
              dome aperture in order to expose the specified alt/az area to the sky,
              including positioning clamshell leaves, split shutters, etc. Your app
              need not know how this is happening, just that the alt/az area of the sky
              will be visible.
            * Do not use Azimuth as a way to determine if a (non-blocking) 
              :py:meth:`SlewToAzimuth()` has completed. The Azimuth may transit through 
              the requested position before finally settling, and may be slightly off
              when it stops. Use the :py:attr:`Slewing` property.
        
        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control 
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :py:attr:`Slaved` property for details 
            on slaving (telescope motion tracking). Only an *integrated* mount/dome system
            will offer both a Telescope and a Dome interface, and be capable of slaving.
        
        """
        return self._get("azimuth")

    @property
    def CanFindHome(self) -> bool:
        """The dome can find its home position via :py:meth:`FindHome()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """             
        return self._get("canfindhome")

    @property
    def CanPark(self) -> bool:
        """The dome can be programmatically parked via :py:meth:`Park()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """             
        return self._get("canpark")

    @property
    def CanSetAltitude(self) -> bool:
        """The opening's altitude can be set via :py:meth:`SetAltitude()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """             
        return self._get("cansetaltitude")

    @property
    def CanSetAzimuth(self) -> bool:
        """The opening's azimuth can be set via :py:meth:`SetAzimuth()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """             
        return self._get("cansetazimuth")

    @property
    def CanSetPark(self) -> bool:
        """The dome park position can be set via :py:meth:`SetPark()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """             
        return self._get("cansetpark")

    @property
    def CanSetShutter(self) -> bool:
        """The shutter can be opened and closed via :py:meth:`OpenShutter()` and :py:meth:`CloseShutter()` 

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """             
        return self._get("cansetshutter")

    @property
    def CanSlave(self) -> bool:
        """The opening can be slaved to the telescope/optics via :py:attr:`Slaved` (see Notes)

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * If this is True, then the exposed Dome interface is part of an integrated 
              mount/dome control system that offers automatic slaving.

        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control 
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :py:attr:`Slaved` property for details 
            on slaving (telescope motion tracking).
       
        """             
        return self._get("canslave")

    @property
    def CanSyncAzimuth(self) -> bool:
        """The opening's azimuth position can be synched via :py:meth:`SyncToAzimuth()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """             
        return self._get("cansyncazimuth")

    @property
    def ShutterStatus(self) -> ShutterState:
        """Status of the dome shutter or roll-off roof.

        Raises:
            NotImplementedException: If the dome does not have a controllable
                shutter/roof. In this case :py:attr:`CanSetShutter` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This property is the correct way to monitor an in-progress shutter
              movement. It will be :py:class:`~ShutterState.shutterOpening' 
              immediately after returning from an :py:meth:`OpenShutter()` call, 
              and :py:class:`~ShutterState.shutterClosing' immediately after 
              returning from a :py:meth:`CloseShutter()` call.
            * TODO Really? If actual shutter status can not be read, then reports 
              back the last shutter state. 

        """
        return ShutterState(self._get("shutterstatus"))

    @property
    def Slaved(self) -> bool:
        """(Read/Write) Indicate or set whether the dome is slaved to the telescope.
        
        Raises:
            NotImplementedException: If the dome controller is not par of an
                integrated dome/telescope control system which offers controllable
                dome slaving. In this case :py:attr:`CanSlave` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control 
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :py:attr:`Slaved` property for details 
            on slaving (telescope motion tracking).

        """
        return self._get("slaved")
    @Slaved.setter
    def Slaved(self, SlavedState: bool):
        self._put("slaved", Slaved=SlavedState)

    @property
    def Slewing(self) -> bool:
        """Any part of the dome is moving, opening, or closing. See Notes.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: TODO Is this right? Must raise an error if :py:attr:`Slaved` 
                is true, if TODO [WHAT? or SlavedException?] not supported, 
                if a communications failure TODO [comm errors are everywhere] 
                occurs, or if the opening can not reach the requested azimuth or altitude, 
                or if it fails to open or close the roof/shutter, in other words, 
                if the device cannot *successfully complete* a previous movement 
                request. This exception may be encountered on any call to the device.
                TODO REVIEW, way too wordy. The key is "successfully complete" right?
        
        Notes:
            * This is the correct property to use to determine *successful* completion of 
              a (non-blocking) :py:meth:`SlewToAzimuth()` and/or :py:meth:`SlewToAltitude()`
              request. Slewing will be True immediately upon returning from either of these
              calls, and will remain True until *successful* completion, at which time 
              Slewing will become False.
            * By "any part of the dome" is meant the roof, a shutter, clamshell leaves,
              a port, etc. This will be true during alt/az movement of the opening as 
              well as opening or closing. 

        """
        return self._get("slewing")

    def AbortSlew(self) -> None:
        """Immediately stops any part of the dome from moving, opening, or closing. See Notes.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: TODO [REVIEW comm failure is EVERYWHERE!]
                If a communications failure occurs, or if the AbortSlew()
                request itself fails in some way. This exception may be encountered 
                on any call to the device. 
        
        Notes:
            * When this call succeeds, :py:attr:`Slewing` will become False, and slaving 
              will have stopped as indicate by :py:attr:`Slaved` becoming False.
            * By "any part of the dome" is meant the dome itself, the roof, a shutter, 
              clamshell leaves, a port, etc. Calling AbortSlew() will stop alt/az 
              movement of the opening as well as stopping opening or closing. 

        """
        self._put("abortslew")

    def CloseShutter(self) -> None:
        """Start to close the shutter or otherwise shield the telescope from the sky

        **Non-blocking**: Returns immediately with :py:attr:`ShutterStatus` = 
        :py:attr:`~ShutterState.shutterClosing` after *successfully* starting the operation.
        See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not have a controllable
                shutter/roof. In this case :py:attr:`CanSetShutter` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): :py:attr:`ShutterStatus` is the correct 
              property to use for monitoring an in-progress shutter movement. A transition to 
              :py:class:`~ShutterState.shutterClosed` indicates a *successfully
              completed* closure. If it returns with :py:attr:`ShutterStatus` 
              :py:class:`~ShutterState.shutterClosed`, it means the shutter was already 
              closed, another success. If  See :ref:`async_faq`
            * If another app calls CloseShutter() while the shutter is already closing, 
              the request will be accepted and you will see :py:attr:`ShutterStatus` = 
              :py:attr:`~ShutterState.shutterClosing` as you would expect.

        Attention:
            TODO [REVIEW] This operation is not cross-coupled in any way with the currently
            requested :py:attr:`Azimuth` and :py:attr:`Altitude`. Opening and closing 
            are used to shield and expose the opening to the sky, wherever it is 
            specified to be. 

        """

        self._put("closeshutter")

    def FindHome(self):
        """Start a search for the dome's home position and synchronize Azimuth.

        **Non-blocking**: See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not support homing.
            NotConnectedException: If the device is not connected
            SlavedException: TODO [REVIEW] If :py:attr:`Slaved` is True
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`AtHome` property
              to monitor the operation. When the the home position is has been 
              *successfully* reached, :py:attr:`Azimuth` is synchronized to the appropriate value,
              :py:attr:`AtHome` becomes True and :py:attr:`Slewing` becomes False. See :ref:`async_faq`
            * An app should check :py:attr:`AtHome` before calling FindHome(). 
        
        """

        self._put("findhome")

    def OpenShutter(self) -> None:
        """Start to open shutter or otherwise expose telescope to the sky.
        
        **Non-blocking**: Returns immediately with :py:attr:`ShutterStatus` = 
        :py:class:`~ShutterState.shutterOpening` if the opening has *successfully* 
        been started. See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not have a controllable
                shutter/roof. In this case :py:attr:`CanSetShutter` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): :py:attr:`ShutterStatus` is the correct 
              property to use for monitoring an in-progress shutter movement. A 
              transition to :py:class:`~ShutterState.shutterOpen` indicates a 
              *successfully completed* opening. If OpenShutter returns with 
              :py:attr:`ShutterStatus` = :py:attr:`~ShutterState.shutterOpen`
              then the shutter was already open, which is also a success. 
              See :ref:`async_faq`

            * If another app calls OpenShutter() while the shutter is already opening, 
              the request will be accepted and you will see :py:attr:`ShutterStatus` = 
              :py:attr:`~ShutterState.shutterOpening` as you would expect.

        Attention:
            TODO REVIEW This operation is not cross-coupled in any way with the currently
            requested :py:attr:`Azimuth` and :py:attr:`Altitude`. Opening and closing 
            are used to shield and expose the opening to the sky, wherever it is 
            specified to be. 
                
        """
        self._put("openshutter")

    def Park(self) -> None:
        """Start slewing the dome to its park position.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True 
        if the park operation has *successfully* been started, or 
        :py:attr:`Slewing` = False which means the dome is already parked 
        (and of course :py:attr:`AtPark` will already be True). See Notes, 
        and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not support parking. 
                In this case :py:attr:`CanPark` will be False.
            NotConnectedException: If the device is not connected
            ParkedException: TODO [REVIEW-not in C# docs] If :py:attr:`AtPark` is True
            SlavedException: TODO [REVIEW-Not in C# docs] If :py:attr:`Slaved` is True
            DriverException:An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`AtPark` property
              to monitor the operation. When the the park position has been 
              *successfully* reached, :py:attr:`Azimuth` is synchronized to the 
              park position, :py:attr:`AtPark` becomes True, and 
              :py:attr:`Slewing` becomes False.  See :ref:`async_faq`
            * An app should check :py:attr:`AtPark` before calling Park().
        
        """
        self._put("park")

    def SetPark(self) -> None:
        """Set current position of dome to be the park position

        Raises:
            NotImplementedException: If the dome does not support the setting
                of the park position. In this case :py:attr:`CanSetPark` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: TODO [REVIEW] If :py:attr:`Slaved` is True
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """
        self._put("setpark")

    def SlewToAltitude(self, Altitude: float) -> None:
        """Start slewing the opening to the given altitude (degrees).
        
        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True 
        if the slewing operation has *successfully* been started. 
        See Notes, and :ref:`async_faq`

        Args:
            Altitude: The requested altitude of the opening

        Raises:
            NotImplementedException: If the dome opening does not support vertical 
                (altitude) control. In this case :py:attr:`CanSetAltitude` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: TODO [REVIEW] If :py:attr:`Slaved` is True
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to monitor the operation. When the the requested Altitude has been 
              *successfully* reached, :py:attr:`Slewing` becomes False. 
              If SlewToAltitude() returns with :py:attr:`Slewing` = False then 
              the opening was already at the requested altitude, which is also a 
              success See :ref:`async_faq`
            * The specified altitude (*referenced to the dome center/equator*) is 
              of the position of the opening.

        Attention: 
            TODO [REVIEW] If the opening is closed, this method must still complete, 
            with the dome controller accepting the requested position as its
            :py:attr:`Altitude` property. Later, when opening,
            via :py:meth:`OpenShutter()`, the last received/current 
            :py:attr:`Altitude` is used to position the opening to the sky.

        """
        self._put("slewtoaltitude", Altitude=Altitude)

    def SlewToAzimuth(self, Azimuth: float) -> None:
        """Start slewing the opening to the given azimuth (degrees).
        
        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True 
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Args:
            Azimuth: The requested azimuth of the opening. See Notes.

        Raises:
            NotImplementedException: If the dome does not support rotational 
                (azimuth) control. In this case :py:attr:`CanSetAzimuth` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: TODO [REVIEW] If :py:attr:`Slaved` is True
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to monitor the operation. When the the requested Azimuth has been 
              *successfully* reached, :py:attr:`Slewing` becomes False. 
              If SlewToAzimuth() returns with :py:attr:`Slewing` = False then 
              the opening was already at the requested azimuth, which is also a 
              success See :ref:`async_faq`
            * Azimuth has the usual sense of True North zero and increasing clockwise
              i.e. 90 East, 180 South, 270 West.
            * The specified azimuth (*referenced to the dome center/equator*) is of the 
              position of the opening. 

        Attention: 
            TODO [REVIEW] If the shutter is closed, this method will still complete, 
            with the dome controller accepting the requested position as its
            :py:attr:`Azimuth` property. Later, when the shutter is opened 
            via :py:meth:`OpenShutter()`, the last received/current 
            :py:attr:`Azimuth` is used to re-position the opening to the sky. This
            may extend the time needed to complete the :py:meth:`OpenShutter()`
            operation.

        """
        self._put("slewtoazimuth", Azimuth=Azimuth)

    def SyncToAzimuth(self, Azimuth: float) -> None:
        """Synchronize the current azimuth of the dome (degrees) to the given azimuth.

        Raises:
            NotImplementedException: If the shutter does not support azimuth
                synchronization. In this case :py:attr:`CanSyncAzimuth` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: TODO [REVIEW] If :py:attr:`Slaved` is True
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        """
        self._put("synctoazimuth", Azimuth=Azimuth)

