# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# dome - Implements ASCOM Alpaca dome device class
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
# 21-Jul-22 (rbd) 2.0.1 Resolve TODO reviews
# 06-Mar-24 (rbd) 3.0.0 Add Master Interfaces refs to all members
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        """
        super().__init__(address, "dome", device_number, protocol)

    @property
    def Altitude(self) -> float:
        """Dome altitude (degrees) of the opening to the sky.

        Raises:
            NotImplementedException: If the dome does not support vertical (altitude)
                control / placement of its observing opening (including a roll-off roof).
                In this case :attr:`CanSetAltitude` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * The specified altitude (*referenced to the dome center/equator*) is of the
              opening to the sky through which the optics receive light.
            * It is up to the dome control and driver to determine how best to locate the
              dome aperture in order to expose the specified alt/az area to the sky,
              including positioning clamshell leaves, split shutters, etc. Your app
              need not know how this is happening, just that the alt/az area of the sky
              will be visible.
            * Do not use Altitude as a way to determine if a (non-blocking)
              :meth:`SlewToAltitude()` has completed. The Altitude may transit through
              the requested position before finally settling, and may be slightly off
              when it stops. Use the :attr:`Slewing` property.

        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :attr:`Slaved` property for details
            on slaving (telescope motion tracking).  Only an *integrated* mount/dome system
            will offer both a Telescope and a Dome interface, and be capable of slaving.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Altitude|

            .. |Altitude| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.Altitude" target="_blank">
                Dome.Altitude</a> (external)
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

        .. admonition:: Master Interfaces Reference
            :class: green

            |AtHome|

            .. |AtHome| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.AtHome" target="_blank">
                Dome.AtHome</a> (external)
        """
        return self._get("athome")

    @property
    def AtPark(self) -> bool:
        """The telescope has *successfully* reached its park position.

        Raises:
            NotImplementedException: If the dome does not support parking.
                In this case :attr:`CanPark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            Set only following a park() operation and reset with any slew operation.

        Returns:
            True if the dome is in the programmed park position.

        .. admonition:: Master Interfaces Reference
            :class: green

            |AtPark|

            .. |AtPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.AtPark" target="_blank">
                Dome.AtPark</a> (external)
        """
        return self._get("atpark")

    @property
    def Azimuth(self) -> float:
        """Dome azimuth (degrees) of the opening to the sky

        This this does not include the geometric transformations needed
        for mount and optics configurations. See :ref:`dome-faq`.

        Raises:
            NotImplementedException: If the dome does not support directional (azimuth)
                control / placement of its observing opening (including roll-off roof).
                In this case :attr:`CanSetAzimuth` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * Azimuth has the usual sense of True North zero and increasing clockwise
              i.e. 90 East, 180 South, 270 West.
            * The specified azimuth (*referenced to the dome center/equator*) is of the
              opening to the sky through which the optics receive light.
            * You can detect a roll-off roof by :attr:`CanSetAzimuth` being False.
            * It is up to the dome control and driver to determine how best to locate the
              dome aperture in order to expose the specified alt/az area to the sky,
              including positioning clamshell leaves, split shutters, etc. Your app
              need not know how this is happening, just that the alt/az area of the sky
              will be visible.
            * Do not use Azimuth as a way to determine if a (non-blocking)
              :meth:`SlewToAzimuth()` has completed. The Azimuth may transit through
              the requested position before finally settling, and may be slightly off
              when it stops. Use the :attr:`Slewing` property.

        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :attr:`Slaved` property for details
            on slaving (telescope motion tracking). Only an *integrated* mount/dome system
            will offer both a Telescope and a Dome interface, and be capable of slaving.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Azimuth|

            .. |Azimuth| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.Azimuth" target="_blank">
                Dome.Azimuth</a> (external)
        """
        return self._get("azimuth")

    @property
    def CanFindHome(self) -> bool:
        """The dome can find its home position via :meth:`FindHome()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanFindHome|

            .. |CanFindHome| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanFindHome" target="_blank">
                Dome.CanFindHome</a> (external)
        """
        return self._get("canfindhome")

    @property
    def CanPark(self) -> bool:
        """The dome can be programmatically parked via :meth:`Park()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanPark|

            .. |CanPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanPark" target="_blank">
                Dome.CanPark</a> (external)
        """
        return self._get("canpark")

    @property
    def CanSetAltitude(self) -> bool:
        """The opening's altitude can be set via :meth:`SetAltitude()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetAltitude|

            .. |CanSetAltitude| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanSetAltitude" target="_blank">
                Dome.CanSetAltitude</a> (external)
        """
        return self._get("cansetaltitude")

    @property
    def CanSetAzimuth(self) -> bool:
        """The opening's azimuth can be set via :meth:`SetAzimuth()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetAzimuth|

            .. |CanSetAzimuth| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanSetAzimuth" target="_blank">
                Dome.CanSetAzimuth</a> (external)
        """
        return self._get("cansetazimuth")

    @property
    def CanSetPark(self) -> bool:
        """The dome park position can be set via :meth:`SetPark()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetPark|

            .. |CanSetPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanSetPark" target="_blank">
                Dome.CanSetPark</a> (external)
        """
        return self._get("cansetpark")

    @property
    def CanSetShutter(self) -> bool:
        """The shutter can be opened and closed via :meth:`OpenShutter()` and :meth:`CloseShutter()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetShutter|

            .. |CanSetShutter| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanSetShutter" target="_blank">
                Dome.CanSetShutter</a> (external)
        """
        return self._get("cansetshutter")

    @property
    def CanSlave(self) -> bool:
        """The opening can be slaved to the telescope/optics via :attr:`Slaved` (see Notes)

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * If this is True, then the exposed Dome interface is part of an integrated
              mount/dome control system that offers automatic slaving.

        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :attr:`Slaved` property for details
            on slaving (telescope motion tracking).

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSlave|

            .. |CanSlave| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanSlave" target="_blank">
                Dome.CanSlave</a> (external)
        """
        return self._get("canslave")

    @property
    def CanSyncAzimuth(self) -> bool:
        """The opening's azimuth position can be synched via :meth:`SyncToAzimuth()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSyncAzimuth|

            .. |CanSyncAzimuth| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CanSyncAzimuth" target="_blank">
                Dome.CanSyncAzimuth</a> (external)
        """
        return self._get("cansyncazimuth")

    @property
    def ShutterStatus(self) -> ShutterState:
        """Status of the dome shutter or roll-off roof.

        Raises:
            NotImplementedException: If the dome does not have a controllable
                shutter/roof. In this case :attr:`CanSetShutter` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * This property is the correct way to monitor an in-progress shutter
              movement. It will be :py:class:`~ShutterState.shutterOpening'
              immediately after returning from an :meth:`OpenShutter()` call,
              and :py:class:`~ShutterState.shutterClosing' immediately after
              returning from a :meth:`CloseShutter()` call.

        .. admonition:: Master Interfaces Reference
            :class: green

            |ShutterStatus|

            .. |ShutterStatus| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.ShutterStatus" target="_blank">
                Dome.ShutterStatus</a> (external)
        """
        return ShutterState(self._get("shutterstatus"))

    @property
    def Slaved(self) -> bool:
        """(Read/Write) Indicate or set whether the dome is slaved to the telescope.

        Raises:
            NotImplementedException: If the dome controller is not par of an
                integrated dome/telescope control system which offers controllable
                dome slaving. In this case :attr:`CanSlave` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Attention:
            An ASCOM Dome device does not include transformations for mount/optics to
            azimuth and altitude. It is prohibited for a stand-alone Dome control
            device to require cross-linking to query a telescope directly. Your app
            will need to provide the dome-centered alt/az given the geometry of the
            mount and optics in use. See also the :attr:`Slaved` property for details
            on slaving (telescope motion tracking).

        .. admonition:: Master Interfaces Reference
            :class: green

            |Slaved|

            .. |Slaved| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.Slaved" target="_blank">
                Dome.Slaved</a> (external)
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
            DriverException: If the device cannot *successfully complete*
                a previous movement request. This exception may be encountered
                on any call to the device.

        Notes:
            * This is the correct property to use to determine *successful* completion of
              a (non-blocking) :meth:`SlewToAzimuth()` and/or :meth:`SlewToAltitude()`
              request. Slewing will be True immediately upon returning from either of these
              calls, and will remain True until *successful* completion, at which time
              Slewing will become False.
            * By "any part of the dome" is meant the roof, a shutter, clamshell leaves,
              a port, etc. This will be true during alt/az movement of the opening as
              well as opening or closing.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Slewing|

            .. |Slewing| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.Slewing" target="_blank">
                Dome.Slewing</a> (external)
        """
        return self._get("slewing")

    def AbortSlew(self) -> None:
        """Immediately stops any part of the dome from moving, opening, or closing. See Notes.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException:
                If a communications failure occurs, or if the AbortSlew()
                request itself fails in some way. This exception may be encountered
                on any call to the device.

        Notes:
            * When this call succeeds, :attr:`Slewing` will become False, and slaving
              will have stopped as indicate by :attr:`Slaved` becoming False.
            * By "any part of the dome" is meant the dome itself, the roof, a shutter,
              clamshell leaves, a port, etc. Calling AbortSlew() will stop alt/az
              movement of the opening as well as stopping opening or closing.

        .. admonition:: Master Interfaces Reference
            :class: green

            |AbortSlew|

            .. |AbortSlew| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.AbortSlew" target="_blank">
                Dome.AbortSlew()</a> (external)
        """
        self._put("abortslew")

    def CloseShutter(self) -> None:
        """Start to close the shutter or otherwise shield the telescope from the sky

        **Non-blocking**: Returns immediately with :attr:`ShutterStatus` =
        :attr:`~ShutterState.shutterClosing` after *successfully* starting the operation.
        See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not have a controllable
                shutter/roof. In this case :attr:`CanSetShutter` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): :attr:`ShutterStatus` is the correct
              property to use for monitoring an in-progress shutter movement. A transition to
              :py:class:`~ShutterState.shutterClosed` indicates a *successfully
              completed* closure. If it returns with :attr:`ShutterStatus`
              :py:class:`~ShutterState.shutterClosed`, it means the shutter was already
              closed, another success. If  See :ref:`async_faq`
            * If another app calls CloseShutter() while the shutter is already closing,
              the request will be accepted and you will see :attr:`ShutterStatus` =
              :attr:`~ShutterState.shutterClosing` as you would expect.

        Attention:
            This operation is not cross-coupled in any way with the currently
            requested :attr:`Azimuth` and :attr:`Altitude`. Opening and closing
            are used to shield and expose the opening to the sky, wherever it is
            specified to be.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CloseShutter|

            .. |CloseShutter| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.CloseShutter" target="_blank">
                Dome.CloseShutter()</a> (external)
        """
        self._put("closeshutter")

    def FindHome(self):
        """Start a search for the dome's home position and synchronize Azimuth.

        **Non-blocking**: See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not support homing.
            NotConnectedException: If the device is not connected
            SlavedException: If :attr:`Slaved` is True
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :attr:`AtHome` property
              to monitor the operation. When the the home position is has been
              *successfully* reached, :attr:`Azimuth` is synchronized to the appropriate value,
              :attr:`AtHome` becomes True and :attr:`Slewing` becomes False. See :ref:`async_faq`
            * An app should check :attr:`AtHome` before calling FindHome().

        .. admonition:: Master Interfaces Reference
            :class: green

            |FindHome|

            .. |FindHome| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.FindHome" target="_blank">
                Dome.FindHome()</a> (external)
        """
        self._put("findhome")

    def OpenShutter(self) -> None:
        """Start to open shutter or otherwise expose telescope to the sky.

        **Non-blocking**: Returns immediately with :attr:`ShutterStatus` =
        :py:class:`~ShutterState.shutterOpening` if the opening has *successfully*
        been started. See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not have a controllable
                shutter/roof. In this case :attr:`CanSetShutter` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): :attr:`ShutterStatus` is the correct
              property to use for monitoring an in-progress shutter movement. A
              transition to :py:class:`~ShutterState.shutterOpen` indicates a
              *successfully completed* opening. If OpenShutter returns with
              :attr:`ShutterStatus` = :attr:`~ShutterState.shutterOpen`
              then the shutter was already open, which is also a success.
              See :ref:`async_faq`

            * If another app calls OpenShutter() while the shutter is already opening,
              the request will be accepted and you will see :attr:`ShutterStatus` =
              :attr:`~ShutterState.shutterOpening` as you would expect.

        Attention:
            This operation is not cross-coupled in any way with the currently
            requested :attr:`Azimuth` and :attr:`Altitude`. Opening and closing
            are used to shield and expose the opening to the sky, wherever it is
            specified to be.

        .. admonition:: Master Interfaces Reference
            :class: green

            |OpenShutter|

            .. |OpenShutter| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.OpenShutter" target="_blank">
                Dome.OpenShutter()</a> (external)
        """
        self._put("openshutter")

    def Park(self) -> None:
        """Start slewing the dome to its park position.

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the park operation has *successfully* been started, or
        :attr:`Slewing` = False which means the dome is already parked
        (and of course :attr:`AtPark` will already be True). See Notes,
        and :ref:`async_faq`

        Raises:
            NotImplementedException: If the dome does not support parking.
                In this case :attr:`CanPark` will be False.
            NotConnectedException: If the device is not connected
            ParkedException: If :attr:`AtPark` is True
            SlavedException: If :attr:`Slaved` is True
            DriverException:An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :attr:`AtPark` property
              to monitor the operation. When the the park position has been
              *successfully* reached, :attr:`Azimuth` is synchronized to the
              park position, :attr:`AtPark` becomes True, and
              :attr:`Slewing` becomes False.  See :ref:`async_faq`
            * An app should check :attr:`AtPark` before calling Park().

        .. admonition:: Master Interfaces Reference
            :class: green

            |Park|

            .. |Park| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.Park" target="_blank">
                Dome.Park()</a> (external)
        """
        self._put("park")

    def SetPark(self) -> None:
        """Set current position of dome to be the park position

        Raises:
            NotImplementedException: If the dome does not support the setting
                of the park position. In this case :attr:`CanSetPark` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: If :attr:`Slaved` is True
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SetPark|

            .. |SetPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.SetPark" target="_blank">
                Dome.SetPark()</a> (external)
        """
        self._put("setpark")

    def SlewToAltitude(self, Altitude: float) -> None:
        """Start slewing the opening to the given altitude (degrees).

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Args:
            Altitude: The requested altitude of the opening

        Raises:
            NotImplementedException: If the dome opening does not support vertical
                (altitude) control. In this case :attr:`CanSetAltitude` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: If :attr:`Slaved` is True
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :attr:`Slewing` property
              to monitor the operation. When the the requested Altitude has been
              *successfully* reached, :attr:`Slewing` becomes False.
              If SlewToAltitude() returns with :attr:`Slewing` = False then
              the opening was already at the requested altitude, which is also a
              success See :ref:`async_faq`
            * The specified altitude (*referenced to the dome center/equator*) is
              of the position of the opening.

        Attention:
            If the opening is closed, this method must still complete,
            with the dome controller accepting the requested position as its
            :attr:`Altitude` property. Later, when opening,
            via :meth:`OpenShutter()`, the last received/current
            :attr:`Altitude` is used to position the opening to the sky.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SlewToAltitude|

            .. |SlewToAltitude| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.SlewToAltitude" target="_blank">
                Dome.SlewToAltitude()</a> (external)
        """
        self._put("slewtoaltitude", Altitude=Altitude)

    def SlewToAzimuth(self, Azimuth: float) -> None:
        """Start slewing the opening to the given azimuth (degrees).

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Args:
            Azimuth: The requested azimuth of the opening. See Notes.

        Raises:
            NotImplementedException: If the dome does not support rotational
                (azimuth) control. In this case :attr:`CanSetAzimuth` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: If :attr:`Slaved` is True
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :attr:`Slewing` property
              to monitor the operation. When the the requested Azimuth has been
              *successfully* reached, :attr:`Slewing` becomes False.
              If SlewToAzimuth() returns with :attr:`Slewing` = False then
              the opening was already at the requested azimuth, which is also a
              success See :ref:`async_faq`
            * Azimuth has the usual sense of True North zero and increasing clockwise
              i.e. 90 East, 180 South, 270 West.
            * The specified azimuth (*referenced to the dome center/equator*) is of the
              position of the opening.

        Attention:
            If the shutter is closed, this method will still complete,
            with the dome controller accepting the requested position as its
            :attr:`Azimuth` property. Later, when the shutter is opened
            via :meth:`OpenShutter()`, the last received/current
            :attr:`Azimuth` is used to re-position the opening to the sky. This
            may extend the time needed to complete the :meth:`OpenShutter()`
            operation.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SlewToAzimuth|

            .. |SlewToAzimuth| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.SlewToAzimuth" target="_blank">
                Dome.SlewToAzimuth()</a> (external)
        """
        self._put("slewtoazimuth", Azimuth=Azimuth)

    def SyncToAzimuth(self, Azimuth: float) -> None:
        """Synchronize the current azimuth of the dome (degrees) to the given azimuth.

        Raises:
            NotImplementedException: If the shutter does not support azimuth
                synchronization. In this case :attr:`CanSyncAzimuth` will be False.
            NotConnectedException: If the device is not connected
            SlavedException: If :attr:`Slaved` is True
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SyncToAzimuth|

            .. |SyncToAzimuth| raw:: html

                <a href="https://ascom-standards.org/newdocs/dome.html#Dome.SyncToAzimuth" target="_blank">
                Dome.SyncToAzimuth()</a> (external)
        """
        self._put("synctoazimuth", Azimuth=Azimuth)

