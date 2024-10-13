# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# telescope - Implements ASCOM Alpaca Telescope device classes and enums
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
# 21-Aug-22 (rbd) 2.0.2 Fix driveRates enum (GitHub issue #3). Fix descriptive
#                 text for pierWest and pierUnknown (GitHub issue #5)
# 08-Mar-24 (rbd) 3.0.0 Add Master Interfaces refs to all members
# -----------------------------------------------------------------------------

from datetime import datetime
from typing import List
import dateutil.parser
from alpaca.docenum import DocIntEnum
from alpaca.device import Device
from alpaca.exceptions import *

class AlignmentModes(DocIntEnum):
    """The geometry of the mount"""
    algAltAz        = 0, 'Altitude-Azimuth alignment'
    algPolar        = 1, 'Polar (equatorial) mount other than German equatorial.'
    algGermanPolar  = 2, 'German equatorial mount.'

class DriveRates(DocIntEnum):
    """Well-known telescope tracking rates"""
    driveSidereal   = 0, 'Sidereal tracking rate (15.041 arcseconds per second).'
    driveLunar      = 1, 'Lunar tracking rate (14.685 arcseconds per second).'
    driveSolar      = 2, 'Solar tracking rate (15.0 arcseconds per second).'
    driveKing       = 3, 'King tracking rate (15.0369 arcseconds per second).'

class EquatorialCoordinateType(DocIntEnum):
    """Equatorial coordinate systems used by telescopes."""
    equOther        = 0, 'Custom or unknown equinox and/or reference frame.'
    equTopocentric  = 1, 'Topocentric coordinates. Coordinates of the object at the current date having allowed for annual aberration, precession and nutation. This is the most common coordinate type for amateur telescopes.'
    equJ2000        = 2, 'J2000 equator/equinox. Coordinates of the object at mid-day on 1st January 2000, ICRS reference frame.'
    equJ2050        = 3, 'J2050 equator/equinox, ICRS reference frame.'
    equB1950        = 4, 'B1950 equinox, FK4 reference frame.'
##    equLocalTopocentric = 1     # OBSOLETE, use Topocentric

class GuideDirections(DocIntEnum):    # Shared by Camera
    """The direction in which the guide-rate motion is to be made."""
    guideNorth      = 0, 'North (+ declination/altitude).'
    guideSouth      = 1, 'South (- declination/altitude).'
    guideEast       = 2, 'East (+ right ascension/azimuth).'
    guideWest       = 3, 'West (- right ascension/azimuth).'

class PierSide(DocIntEnum):
    """The pointing state of the mount"""
    pierEast        = 0, 'Normal pointing state - Mount on the East side of pier (looking West)'
    pierWest        = 1,  'Through the pole pointing state - Mount on the West side of pier (looking East)'
    pierUnknown     = -1, 'Unknown or indeterminate.'

class TelescopeAxes(DocIntEnum):
    axisPrimary     = 0, 'Primary axis (e.g., Right Ascension or Azimuth).'
    axisSecondary   = 1, 'Secondary axis (e.g., Declination or Altitude).'
    axisTertiary    = 2, 'Tertiary axis (e.g. imager rotator/de-rotator).'

class Rate:
    """Describes a range of rates supported by the :py:meth:`MoveAxis()` method"""

    def __init__(
        self,
        maxv: float,
        minv: float
    ):
        self.maxv = maxv
        self.minv = minv

    @property
    def Maximum(self) -> float:
        """The maximum rate (degrees per second)"""
        return self.maxv

    @property
    def Minimum(self) -> float:
        """The minimum rate (degrees per second)"""
        return self.minv

class Telescope(Device):
    """ASCOM Standard ITelescope V3 Interface"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize the Telescope object.

        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        Raises:
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        super().__init__(address, "telescope", device_number, protocol)

    @property
    def AlignmentMode(self) -> AlignmentModes:
        """The current mount alignment mode.

        Raises:
            NotImplementedException: If the mount cannot report its alignment mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |AlignmentMode|

            .. |AlignmentMode| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AlignmentMode" target="_blank">
                Telescope.AlignmentMode</a> (external)
        """
        return AlignmentModes(self._get("alignmentmode"))

    @property
    def Altitude(self) -> float:
        """The mount's current Altitude (degrees) above the horizon.

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Altitude|

            .. |Altitude| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Altitude" target="_blank">
                Telescope.Altitude</a> (external)
        """
        return self._get("altitude")

    @property
    def ApertureArea(self) -> float:
        """The telescope's aperture area (square meters).

        Raises:
            NotImplementedException:Not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * The area takes into account any obstructions; it is the actual
              light-gathering area.

        .. admonition:: Master Interfaces Reference
            :class: green

            |ApertureArea|

            .. |ApertureArea| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.ApertureArea" target="_blank">
                Telescope.ApertureArea</a> (external)
        """
        return self._get("aperturearea")

    @property
    def ApertureDiameter(self) -> float:
        """Return the telescope's effective aperture (meters).

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |ApertureDiameter|

            .. |ApertureDiameter| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.ApertureDiameter" target="_blank">
                Telescope.ApertureDiameter</a> (external)
        """
        return self._get("aperturediameter")

    @property
    def AtHome(self) -> bool:
        """The mount is at the home position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is the correct property to use to determine *successful* completion of
              the (non-blocking) :py:meth:`FindHome()` operation. See :ref:`async_faq`
            * True if the telescope is stopped in the Home position. Can be True
              only following a FindHome() operation.
            * Will become False immediately upon any slewing operation
            * Will always be False if the telescope does not support homing. Use
              :py:attr:`CanFindHome` to determine if the mount supports homing.

        .. admonition:: Master Interfaces Reference
            :class: green

            |AtHome|

            .. |AtHome| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AtHome" target="_blank">
                Telescope.AtHome</a> (external)
        """
        return self._get("athome")

    @property
    def AtPark(self) -> bool:
        """The telescope is at the park position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is the correct property to use to determine *successful* completion of
              the (non-blocking) :py:meth:`Park()` operation. See :ref:`async_faq`
            * True if the telescope is stopped in the Park position. Can be True
              only following successful completion of a :py:meth:`Park()` operation.
            * When parked, the telescope will be stationary or restricted to a small
              safe range of movement. :py:attr:`Tracking` will be False.
            * You must take the telescope out of park by calling :py:meth:`Unpark()`;
              attempts to slew enabling tracking while parked will raise
              a :py:class:`~alpaca.exceptions.ParkedException`.
            * Will always be False if the telescope does not support parking. Use
              :py:attr:`CanPark` to determine if the mount supports parking.

        .. admonition:: Master Interfaces Reference
            :class: green

            |AtPark|

            .. |AtPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AtPark" target="_blank">
                Telescope.AtPark</a> (external)
        """
        return self._get("atpark")

    @property
    def Azimuth(self) -> float:
        """The azimuth (degrees) at which the telescope is currently pointing.

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Azimuth is per the usual alt/az coordinate convention: degrees
              North-referenced, positive East/clockwise.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Azimuth|

            .. |Azimuth| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Azimuth" target="_blank">
                Telescope.Azimuth</a> (external)
        """
        return self._get("azimuth")

    @property
    def CanFindHome(self) -> bool:
        """The mount can find its home position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`FindHome()`

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanFindHome|

            .. |CanFindHome| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanFindHome" target="_blank">
                Telescope.CanFindHome</a> (external)
        """
        return self._get("canfindhome")

    @property
    def CanPark(self) -> bool:
        """The mount can be parked.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`Park()`

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanPark|

            .. |CanPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanPark" target="_blank">
                Telescope.CanPark</a> (external)
        """
        return self._get("canpark")

    @property
    def CanPulseGuide(self) -> bool:
        """The mount can be pulse guided.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:attr:`PulseGuide`

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanPulseGuide|

            .. |CanPulseGuide| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanPulseGuide" target="_blank">
                Telescope.CanPulseGuide</a> (external)
        """
        return self._get("canpulseguide")

    @property
    def CanSetDeclinationRate(self) -> bool:
        """The Declination tracking rate may be offset.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:attr:`DeclinationRate`

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetDeclinationRate|

            .. |CanSetDeclinationRate| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetDeclinationRate" target="_blank">
                Telescope.CanSetDeclinationRate</a> (external)
        """
        return self._get("cansetdeclinationrate")

    @property
    def CanSetGuideRates(self) -> bool:
        """The guiding rates for :py:meth:`PulseGuide()` can be adjusted

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:attr:`PulseGuide()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetGuideRates|

            .. |CanSetGuideRates| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetGuideRates" target="_blank">
                Telescope.CanSetGuideRates</a> (external)
        """
        return self._get("cansetguiderates")

    @property
    def CanSetPark(self) -> bool:
        """The mount's park position can be set.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:attr:`SetPark()`

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetPark|

            .. |CanSetPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetPark" target="_blank">
                Telescope.CanSetPark</a> (external)
        """
        return self._get("cansetpark")

    @property
    def CanSetPierSide(self) -> bool:
        """The mount can be force-flipped via setting :py:attr:`SideOfPier`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:attr:`SideOfPier`.
            * Will always be False for non-German mounts

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetPierSide|

            .. |CanSetPierSide| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetPierSide" target="_blank">
                Telescope.CanSetPierSide</a> (external)
        """
        return self._get("cansetpierside")

    @property
    def CanSetRightAscensionRate(self) -> bool:
        """The Right Ascension tracking rate may be offset

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:attr:`RightAscensionRate`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetRightAscensionRate|

            .. |CanSetRightAscensionRate| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetRightAscensionRate" target="_blank">
                Telescope.CanSetRightAscensionRate</a> (external)
        """
        return self._get("cansetrightascensionrate")

    @property
    def CanSetTracking(self) -> bool:
        """The mount's sidereal tracking may be turned on and off

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:attr:`Tracking`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSetTracking|

            .. |CanSetTracking| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetTracking" target="_blank">
                Telescope.CanSetTracking</a> (external)
        """
        return self._get("cansettracking")

    @property
    def CanSlew(self) -> bool:
        """The mount can slew to equatorial coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`SlewToCoordinates()`, :py:meth:`SlewToCoordinatesAsync()`
              :py:meth:`SlewToTarget()`, and :py:meth:`SlewToTargetAsync()`.

        Attention:
            Do not use synchronous methods unless the mount cannot do asynchronous
            slewing (:py:attr:`CanSlewAsync` = False). Synchronous methods will be
            deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSlew|

            .. |CanSlew| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlew" target="_blank">
                Telescope.CanSlew</a> (external)
        """
        return self._get("canslew")

    @property
    def CanSlewAsync(self) -> bool:
        """The mount can slew to equatorial coordinates synchronously.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * :py:attr:`CanSlew` will be True if CanSlewAsync is True.
            * See :py:meth:`SlewToCoordinatesAsync()`
              and :py:meth:`SlewToTargetAsync()`.

        Attention:
            Always use asynchronous slewing if at all possible (CanSlewAsync = True).
            Synchronous methods will be deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSlewAsync|

            .. |CanSlewAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAsync" target="_blank">
                Telescope.CanSlewAsync</a> (external)
        """
        return self._get("canslewasync")

    @property
    def CanSlewAltAz(self) -> bool:
        """The mount can slew to alt/az coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`SlewToAltAz()` and :py:meth:`SlewToAltAzAsync()`.

        Attention:
            Do not use synchronous methods unless the mount cannot do asynchronous
            slewing (:py:attr:`CanSlewAltAzAsync` = False). Synchronous methods will be
            deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSlewAltAz|

            .. |CanSlewAltAz| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAltAz" target="_blank">
                Telescope.CanSlewAltAz</a> (external)
        """
        return self._get("canslewaltaz")

    @property
    def CanSlewAltAzAsync(self) -> bool:
        """The mount can slew to alt/az coordinates asynchronously.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * :py:attr:`CanSlewAltAz` will be True if CanSlewAltAzAsync is True.
            * See :py:meth:`SlewToAltAzAsync()`.

        Attention:
            Always use asynchronous slewing if at all possible (CanSlewAltAzAsync = True).
            Synchronous methods will be deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSlewAltAzAsync|

            .. |CanSlewAltAzAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAltAzAsync" target="_blank">
                Telescope.CanSlewAltAzAsync</a> (external)
        """
        return self._get("canslewaltazasync")

    @property
    def CanSync(self) -> bool:
        """The mount can be synchronized to equatorial coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`SyncToCoordinates()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSync|

            .. |CanSync| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSync" target="_blank">
                Telescope.CanSync</a> (external)
        """
        return self._get("cansync")

    @property
    def CanSyncAltAz(self) -> bool:
        """The mount can be synchronized to alt/az coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`SyncToAltAz()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanSyncAltAz|

            .. |CanSyncAltAz| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSyncAltAz" target="_blank">
                Telescope.CanSyncAltAz</a> (external)
        """
        return self._get("cansyncaltaz")

    @property
    def CanUnpark(self) -> bool:
        """The mount can be unparked

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`Unpark()` and :py:meth:`Park()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanUnpark|

            .. |CanUnpark| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanUnpark" target="_blank">
                Telescope.CanUnpark</a> (external)
        """
        return self._get("canunpark")

    @property
    def Declination(self) -> float:
        """The mount's current Declination (degrees) in the current
        :py:attr:`EquatorialSystem` (see Notes)

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Declination will be in the equinox given by the current value of
              :py:attr:`EquatorialSystem`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Declination|

            .. |Declination| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Declination" target="_blank">
                Telescope.Declination</a> (external)
        """
        return self._get("declination")

    @property
    def DeclinationRate(self) -> float:
        """(Read/Write) The mount's declination tracking rate (see Notes).

        Raises:
            NotImplementedException: If :py:attr:`CanSetDeclinationRate` is False,
            yet an attempt is made to write to this property.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * DeclinationRate is an offset from 0 (no change in declination), given in arc seconds
              per SI (atomic) second. (Please note that the units of :py:attr:`RightAscensionRate`
              are in (sidereal) seconds of RA per *sidereal* second).
            * The supported range for this property is mount-specific.
            * Offset tracking is most commonly used to track a solar system object such as a
              minor planet or comet.
            * Offset tracking may also be used (less commonly) as a method for reducing
              dynamic mount errors.
            * If offset tracking is in effect (non-zero), and a slew is initiated, the
              mount will continue to update the slew destination coordinates at the
              given offset rate.

        .. admonition:: Master Interfaces Reference
            :class: green

            |DeclinationRate|

            .. |DeclinationRate| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.DeclinationRate" target="_blank">
                Telescope.DeclinationRate</a> (external)
        """
        return self._get("declinationrate")
    @DeclinationRate.setter
    def DeclinationRate(self, DeclinationRate: float):
        self._put("declinationrate", DeclinationRate=DeclinationRate)

    @property
    def DoesRefraction(self) -> bool:
        """(Read/Write) The mount applies atmospheric refraction to corrections

        Raises:
            NotImplementedException: If either reading or writing of this
                property is not implemented
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * If the driver does not know whether the attached telescope does its
              own refraction, and if the driver does not itself calculate refraction,
              this property (if implemented) will raise
              :py:class:`~alpaca.exceptions.DriverException` when read.
            * If the mount indicates that it can apply refraction, yet you wish to
              calculate your own (more accurate) correction, try setting this to
              False then, if successful, supply your own refracted coordinates.
            * If you set this to True, and the mount (already) does refraction, or
              if you set this to Fales, and the mount (already) does not do
              refraction, no exception will be raised.

        .. admonition:: Master Interfaces Reference
            :class: green

            |DoesRefraction|

            .. |DoesRefraction| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.DoesRefraction" target="_blank">
                Telescope.DoesRefraction</a> (external)
        """
        return self._get("doesrefraction")
    @DoesRefraction.setter
    def DoesRefraction(self, DoesRefraction: bool):
        self._put("doesrefraction", DoesRefraction=DoesRefraction)

    @property
    def EquatorialSystem(self) -> EquatorialCoordinateType:
        """The current equatorial coordinate system used by the mount

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:class:`EquatorialCoordinateType`.
            * Most mounts use topocentric coordinates. Some high-end research
              mounts use J2000 coordinates.

        .. admonition:: Master Interfaces Reference
            :class: green

            |EquatorialSystem|

            .. |EquatorialSystem| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.EquatorialSystem" target="_blank">
                Telescope.EquatorialSystem</a> (external)
        """
        return EquatorialCoordinateType(self._get("equatorialsystem"))

    @property
    def FocalLength(self) -> float:
        """Return the telescope's focal length in meters.

        Raises:
            NotImplementedException: Focal length is not available from the mount
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |FocalLength|

            .. |FocalLength| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.FocalLength" target="_blank">
                Telescope.FocalLength</a> (external)
        """
        return self._get("focallength")

    @property
    def GuideRateDeclination(self) -> float:
        """(Read/Write) The current Declination rate offset (deg/sec) for guiding.

        Raises:
            InvalidValueException: If an invalid guide rate is set
            NotImplementedException: Rate cannot be set, :py:attr:`CanSetGuideRates` = False
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is the rate for both hardware/relay guiding and for
              :py:meth:`PulseGuide()`.
            * The mount may not support separate right ascension and declination
              guide rates. If so, setting either rate will set the other to the
              same value.
            * This value will be set to a default upon startup.

        .. admonition:: Master Interfaces Reference
            :class: green

            |GuideRateDeclination|

            .. |GuideRateDeclination| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.GuideRateDeclination" target="_blank">
                Telescope.GuideRateDeclination</a> (external)
        """
        return self._get("guideratedeclination")
    @GuideRateDeclination.setter
    def GuideRateDeclination(self, GuideRateDeclination: float):
        self._put("guideratedeclination", GuideRateDeclination=GuideRateDeclination)

    @property
    def GuideRateRightAscension(self) -> float:
        """(Read/Write) The current Right Ascension rate offset (deg/sec) for guiding.

        Raises:
            InvalidValueException: If an invalid guide rate is set
            NotImplementedException: Rate cannot be set, :py:attr:`CanSetGuideRates` = False
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is the rate for both hardware/relay guiding and for
              :py:meth:`PulseGuide()`.
            * The mount may not support separate right ascension and declination
              guide rates. If so, setting either rate will set the other to the
              same value.
            * This value will be set to a default upon startup.

        .. admonition:: Master Interfaces Reference
            :class: green

            |GuideRateRightAscension|

            .. |GuideRateRightAscension| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.GuideRateRightAscension" target="_blank">
                Telescope.GuideRateRightAscension</a> (external)
        """
        return self._get("guideraterightascension")
    @GuideRateRightAscension.setter
    def GuideRateRightAscension(self, GuideRateRightAscension: float):
        self._put("guideraterightascension", GuideRateRightAscension=GuideRateRightAscension)

    @property
    def IsPulseGuiding(self) -> bool:
        """The mount is currently executing a :py:meth:`PulseGuide()` command.

        Use this property to determine when a (non-blocking) pulse guide command
        has completed. See Notes and :ref:`async_faq`

        Raises:
            NotImplementedException: Pulse guiding is not supported
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
          * A pulse guide command may be so short that you won't see this equal to True.
            If you can read False after calling :py:meth:`PulseGuide()`, then you know it
            completed *successfully*. See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            |IsPulseGuiding|

            .. |IsPulseGuiding| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.IsPulseGuiding" target="_blank">
                Telescope.IsPulseGuiding</a> (external)
        """
        return self._get("ispulseguiding")

    @property
    def RightAscension(self) -> float:
        """The mount's current right ascension (hours) in the current
        :py:attr:`EquatorialSystem`. See Notes.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |RightAscension|

            .. |RightAscension| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.RightAscension" target="_blank">
                Telescope.RightAscension</a> (external)
        """
        return self._get("rightascension")

    @property
    def RightAscensionRate(self) -> float:
        """(Read/Write) Read or set a secular rate of change to the mount’s RightAscension
        (seconds of RA per **sidereal** second). See |RARateFAQ|

        Raises:
            NotImplementedException: If :py:attr:`CanSetRightAscensionRate` is False,
            yet an attempt is made to write to this property.
            InvalidOperationException: If the current :py:attr:`TrackingRate` is not
               ``driveSidereal``.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * RightAscensionRate is an offset from 0 (no change in Right Ascension). Note that
              a mount that is tracking sidereally is pointing to an *unchanging* right ascension.
              See |RARateFAQ|
            * Right Ascension is a *time* coordinate not an angular coordinate. Seconds are not
              arc seconds.
            * To convert a given rate in units of sidereal *seconds* per UTC (clock) second,
              multiply the value by 0.9972695677 (the number of UTC seconds in a sidereal
              second) then set the RightAscensionRate property.
            * The supported range for this property is mount-specific.
            * Offset tracking is most commonly used to track a solar system object such
              as a minor planet or comet.
            * If offset tracking is in effect (non-zero), and a slew is initiated, the
              mount will continue to update the slew destination coordinates at the
              given offset rate.
            * Use the :py:attr:`Tracking` property to stop and start tracking.

        .. admonition:: Master Interfaces Reference
            :class: green

            |RightAscensionRate|

            .. |RightAscensionRate| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.RightAscensionRate" target="_blank">
                Telescope.RightAscensionRate</a> (external)

            |RARateFAQ|

            .. |RARateFAQ| raw:: html

                <a href="https://ascom-standards.org/newdocs/trkoffset-faq.html#what-are-rightascensionrate-and-declinationrate-and-how-are-they-used" target="_blank">
                What are RightAscensionRate and DeclinationRate and how are they used?</a> (external)
        """
        return self._get("rightascensionrate")
    @RightAscensionRate.setter
    def RightAscensionRate(self, RightAscensionRate: float):
        self._put("rightascensionrate", RightAscensionRate=RightAscensionRate)

    @property
    def SideOfPier(self)  -> PierSide:
        """(Read/Write) Start a change of, or return, the mount's pointing state. See :ref:`ptgstate-faq`

        **Non-blocking**: Writing to *change* pointing state returns immediately
        with :py:attr:`Slewing` = True if the state change (e.g. GEM flip) operation
        has *successfully* been started. See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the mount does not report its pointing state,
                at all, or if it doesn't support changing pointing state
                (e.g.force-flipping) by writing to SideOfPier
                (:py:attr:`CanSetPierSide` = False).
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking) if writing SideOfPier to force a
              pointing state change (e.g. GEM flip): Use the :py:attr:`Slewing` property
              to monitor the operation. When the pointing state change has been
              *successfully* completed, :py:attr:`Slewing` becomes False.
              If writing SideOfPier returns with :py:attr:`Slewing` = False then
              the mount was already in the requested pointing state, which is also a
              success.  See :ref:`async_faq`
            * May optionally be written-to to force a flip on a German mount
            * See :ref:`ptgstate-faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            |SideOfPier|

            .. |SideOfPier| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SideOfPier" target="_blank">
                Telescope.SideOfPier</a> (external)
        """
        return PierSide(self._get("sideofpier"))
    @SideOfPier.setter
    def SideOfPier(self, SideOfPier: PierSide):
        self._put("sideofpier", SideOfPier=SideOfPier.value)

    @property
    def SiderealTime(self) -> float:
        """Local apparent sidereal time (See Notes)

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * It is required for a driver to calculate this from the system clock if
              the mount has no accessible source of sidereal time.
            * Local Apparent Sidereal Time is the sidereal time used for pointing
              telescopes, and thus must be calculated from the Greenwich Mean
              Sidereal time, longitude, nutation in longitude and true ecliptic
              obliquity.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SiderealTime|

            .. |SiderealTime| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiderealTime" target="_blank">
                Telescope.SiderealTime</a> (external)
        """
        return self._get("siderealtime")

    @property
    def SiteElevation(self) -> float:
        """(Read/Write) The observing site's elevation (meters) above mean sea level.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range -300 through
                10000 meters.
            InvalidOperationException: If the application must set the SiteElevation
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Some mounts supply this via input to their control systems, in
              other scenarios the application will set this on initialization.
            * If a change is made via SiteElevation, most mounts will save the value
              persistently across power off/on.
            * If the value hasn't been set by any means, an InvalidOperationException
              will be raised.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SiteElevation|

            .. |SiteElevation| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteElevation" target="_blank">
                Telescope.SiteElevation</a> (external)
        """
        return self._get("siteelevation")
    @SiteElevation.setter
    def SiteElevation(self, SiteElevation: float):
        self._put("siteelevation", SiteElevation=SiteElevation)

    @property
    def SiteLatitude(self) -> float:
        """(Read/Write) The latitude (degrees) of the observing site. See Notes.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range -90 through
                90 degrees.
            InvalidOperationException: If the application must set the SiteLatitude
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is geodetic (map) latitude, degrees, WGS84, positive North.
            * Some mounts supply this via input to their control systems, in
              other scenarios the application will set this on initialization.
            * If a change is made via SiteLatitude, most mounts will save the value
              persistently across power off/on.
            * If the value hasn't been set by any means, an InvalidOperationException
              will be raised.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SiteLatitude|

            .. |SiteLatitude| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteLatitude" target="_blank">
                Telescope.SiteLatitude</a> (external)
        """
        return self._get("sitelatitude")
    @SiteLatitude.setter
    def SiteLatitude(self, SiteLatitude: float):
        self._put("sitelatitude", SiteLatitude=SiteLatitude)

    @property
    def SiteLongitude(self) -> float:
        """(Read/Write) The longitude (degrees) of the observing site. See Notes.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range -180 through
                180 degrees.
            InvalidOperationException: If the application must set the SiteLatitude
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is geodetic (map) longitude, degrees, WGS84, **positive East**.
            * Some mounts supply this via input to their control systems, in
              other scenarios the application will set this on initialization.
            * If a change is made via SiteLongitude, most mounts will save the value
              persistently across power off/on.
            * If the value hasn't been set by any means, an InvalidOperationException
              will be raised.

        Attention:
            West longitude is negative.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SiteLongitude|

            .. |SiteLongitude| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteLongitude" target="_blank">
                Telescope.SiteLongitude</a> (external)
        """
        return self._get("sitelongitude")
    @SiteLongitude.setter
    def SiteLongitude(self, SiteLongitude: float):
        self._put("sitelongitude", SiteLongitude=SiteLongitude)

    @property
    def Slewing(self) -> bool:
        """The mount is in motion resulting from a slew or a move-axis. See :ref:`async_faq`

        Raises:
            NotImplementedException: If the property is not implemented (none of the CanSlew
                properties are True, this is a manual mount)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is the correct property to use to determine *successful* completion of
              a (non-blocking) :py:meth:`SlewToCoordinatesAsync()`, :py:meth:`SlewToTargetAsync()`,
              :py:meth:`SlewToCoordinatesAsync()`, or by writing to :py:attr:`SideOfPier`
              to force a flip. See :ref:`async_faq`
            * Slewing will be True immediately upon
              returning from any of these calls, and will remain True until *successful*
              completion, at which time Slewing will become False.
            * You might see Slewing = False on returning from a slew or move-axis
              if the operation takes a very short time. If you see False (and not an exception)
              in this state, you can be certain that the operation completed *successfully*.
            * Slewing will not be True during pulse-guiding or application of tracking
              offsets.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Slewing|

            .. |Slewing| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Slewing" target="_blank">
                Telescope.Slewing</a> (external)
        """
        return self._get("slewing")

    @property
    def SlewSettleTime(self) -> int:
        """(Read/Write) The post-slew settling time (seconds).

        Artificially lengthen all slewing operations. Useful for mounts or
        buildings that require additional mechanical settling time after a
        slew to stabilize.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given settling time is invalid (negative or
                ridiculously high)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SlewSettleTime|

            .. |SlewSettleTime| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewSettleTime" target="_blank">
                Telescope.SlewSettleTime</a> (external)
        """
        return self._get("slewsettletime")
    @SlewSettleTime.setter
    def SlewSettleTime(self, SlewSettleTime: int):
        self._put("slewsettletime", SlewSettleTime=SlewSettleTime)

    @property
    def TargetDeclination(self) -> float:
        """(Read/Write) Set or return the target declination in the current
        :py:attr:`EquatorialSystem`. See Notes.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range -90 through
                90 degrees.
            InvalidOperationException: If the application must set the TargetDeclination
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is a pre-set target coordinate for :py:meth:`SlewToTargetAsync()`
              and :py:meth:`SyncToTarget()`
            * Target coordinates are for the current :py:attr:`EquatorialSystem`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |TargetDeclination|

            .. |TargetDeclination| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TargetDeclination" target="_blank">
                Telescope.TargetDeclination</a> (external)
        """
        return self._get("targetdeclination")
    @TargetDeclination.setter
    def TargetDeclination(self, TargetDeclination: float):
        self._put("targetdeclination", TargetDeclination=TargetDeclination)

    @property
    def TargetRightAscension(self) -> float:
        """(Read/Write) Set or return the target right ascension (hours) in the current
        :py:attr:`EquatorialSystem`

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range 0 to
                24 hours.
            InvalidOperationException: If the application must set the TargetRightAscension
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * This is a pre-set target coordinate for :py:meth:`SlewToTargetAsync()`
              and :py:meth:`SyncToTarget()`
            * Target coordinates are for the current :py:attr:`EquatorialSystem`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |TargetRightAscension|

            .. |TargetRightAscension| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TargetRightAscension" target="_blank">
                Telescope.TargetRightAscension</a> (external)
        """
        return self._get("targetrightascension")
    @TargetRightAscension.setter
    def TargetRightAscension(self, TargetRightAscension: float):
        self._put("targetrightascension", TargetRightAscension=TargetRightAscension)

    @property
    def Tracking(self) -> bool:
        """(Read/Write) The on/off state of the mount's sidereal tracking drive. See Notes.

        Raises:
            NotImplementedException: If writing to the property is not implemented.
                :py:attr:`CanSetTracking` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * When on, the mount will use the last selected :py:attr:`TrackingRate`.
            * Even if the mount doesn't support changing this, it will report the
              current state.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Tracking|

            .. |Tracking| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Tracking" target="_blank">
                Telescope.Tracking</a> (external)
        """
        return self._get("tracking")
    @Tracking.setter
    def Tracking(self, Tracking: bool):
        self._put("tracking", Tracking=Tracking)

    @property
    def TrackingRate(self) -> DriveRates:
        """(Read/Write) The current (sidereal) tracking rate of the mount,
        from :py:attr:`DriveRates`. See Notes.

        Raises:
            InvalidValueException: If value being written is not one of the
                :py:class:`DriveRates`, or if the requested rate is not
                supported by the mount (not all are).
            NotImplementedException: If the mount doesn't support writing this
                property to change the tracking rate.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Even if the mount doesn't support changing this, it will report the
              current state.
            * If this is any rate other than :py:class:`~DriveRates.driveSidereal` then
              :py:attr:`RightAscensionRate` and :py:attr:`DeclinationRate` will
              raise :py:class:`~alpaca.exceptions.InvalidOperationException`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |TrackingRate|

            .. |TrackingRate| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TrackingRate" target="_blank">
                Telescope.TrackingRate</a> (external)
        """
        return DriveRates(self._get("trackingrate"))
    @TrackingRate.setter
    def TrackingRate(self, TrackingRate: DriveRates):
        self._put("trackingrate", TrackingRate=TrackingRate.value)

    @property
    def TrackingRates(self) -> List[DriveRates]:
        """Return a list of supported :py:class:`DriveRates` values

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * At a minimum, this list will contain an item for
              :py:class:`~DriveRates.driveSidereal`

        .. admonition:: Master Interfaces Reference
            :class: green

            |TrackingRates|

            .. |TrackingRates| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TrackingRates" target="_blank">
                Telescope.TrackingRates</a> (external)
        """
        return self._get("trackingrates")

    @property
    def UTCDate(self) -> datetime:
        """(Read/Write) The UTC date/time of the mount's internal clock. See Notes.

        You may write either a Python datetime (tz=UTC) or an ISO 8601 string
        for example::

            ``2022-04-22T20:21:01.123+00:00``

        Raises:
            InvalidValueException: if an illegal ISO 8601 string or a bad Python
                datetime value is written to change the time. See Notes.
            NotImplementedException: If the mount doesn't support writing this
                property to change the UTC time
            InvalidOperationException: When UTCDate is read and the
                mount cannot provide this property itslef and a value has
                not yet be established by writing to the property.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Changing time by writing to this property can be done with either a
              Python datetime value or an ISO 8601 string, for example
              ``2022-04-22T20:21:01.123+00:00``.
            * Even if the mount doesn't support changing this, it will report the
              current UTC date/time. The value may be derived from the system clock
              by the driver if the mount doesn't provide it.
            * If the UTC date/time is being derived from the system clock, you will
              not be able to write this  (you'll get
              :py:class:`~exceptions.NotImplementedException`).

        .. admonition:: Master Interfaces Reference
            :class: green

            |UTCDate|

            .. |UTCDate| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.UTCDate" target="_blank">
                Telescope.UTCDate</a> (external)
        """
        return dateutil.parser.parse(self._get("utcdate"))
    @UTCDate.setter
    def UTCDate(self, UTCDate) -> datetime:         # Variable format
        if type(UTCDate) is str:
            data = UTCDate
        elif type(UTCDate) is datetime:
            data = UTCDate.isoformat()  # Convert to ISO string
        else:
            raise TypeError("Must be an ISO 8601 string or a Python datetime value")
        self._put("utcdate", UTCDate=data)

    def AxisRates(self, Axis: TelescopeAxes) -> List[Rate]:
        """Angular rates at which the mount may be moved with :py:meth:`MoveAxis()`. See Notes.

        Returns:
            A list of :py:class:`Rate` objects, each of which specifies a minimum
            and a maximum angular rate at which the given axis of the mount may be
            moved.

        Raises:
            InvalidValueException: An invalid axis value is specified.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * See :py:meth:`MoveAxis()` for details.
            * An empty list will be returned if :py:meth:`MoveAxis()` is not supported.
            * Returned rates will always be positive, it is up to you to choose the
              positive or negative rate for your call to :py:meth:`MoveAxis()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            |AxisRates|

            .. |AxisRates| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AxisRates" target="_blank">
                Telescope.AxisRates()</a> (external)
        """
        l = []
        jList = self._get("axisrates", Axis=Axis.value)
        for j in jList:
            l.append(Rate(j["Maximum"], j["Minimum"]))
        return l

    def CanMoveAxis(self, Axis: TelescopeAxes) -> bool:
        """The mount can be moved about the given axis

        Raises:
            InvalidValueException: An invalid axis value is specified.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |CanMoveAxis|

            .. |CanMoveAxis| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanMoveAxis" target="_blank">
                Telescope.CanMoveAxis()</a> (external)
        """
        return self._get("canmoveaxis", Axis=Axis.value)

    def DestinationSideOfPier(self, RightAscension: float, Declination: float) -> PierSide:
        """Predicts the pointing state (PierSide) after a GEM slews to given coordinates at this instant.

        Provided so apps can manage GEM flipping during an image sequence. See
        :py:attr:`SideOfPier`, :ref:`dsop-faq`, and :ref:`ptgstate-faq`

        Raises:
            InvalidValueException: An invalid axis value is specified.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |DestinationSideOfPier|

                .. |DestinationSideOfPier| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.DestinationSideOfPier" target="_blank">
                    Telescope.DestinationSideOfPier()</a> (external)

            .. only:: rinoh

                `Telescope.DestinationSideOfPier() <https://ascom-standards.org/newdocs/telescope.html#Telescope.DestinationSideOfPier>`_
        """
        return self._get("destinationsideofpier", RightAscension=RightAscension, Declination=Declination)

    def AbortSlew(self) -> None:
        """Immediatley stops an asynchronous slew in progress.

        Raises:
            InvalidOperationException: If the mount is parked (:py:attr:`AtPark` = True)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Effective only after an asynchronous slew/move call to
              :py:meth:`SlewToTargetAsync()`, :py:meth:`SlewToCoordinatesAsync()`,
              :py:meth:`SlewToAltAzAsync()`, or :py:meth:`MoveAxis()`.
            * Does nothing if no slew/motion is in progress.
            * Tracking is returned to its pre-slew state.

        .. admonition:: Master Interfaces Reference
            :class: green

            |AbortSlew|

            .. |AbortSlew| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AbortSlew" target="_blank">
                Telescope.AbortSlew()</a> (external)
        """
        self._put("abortslew")

    def FindHome(self) -> None:
        """Start moving the mount to the "home" position.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True
        if the homing operation has *successfully* been started, or
        :py:attr:`Slewing` = False which means the mount is already at its
        home position (and of course :py:attr:`AtHome` will already be True).
        See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If this feature is not implemented (:py:attr:`CanFindHome` = False)
            InvalidOperationException: If the mount is parked (:py:attr:`AtPark` = True)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`AtHome` property
              to monitor the operation. When the mount has
              *successfully* reached its home position, :py:attr:`Slewing`
              becomes False and :py:attr:`AtHome`
              becomes True. See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            |FindHome|

            .. |FindHome| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.FindHome" target="_blank">
                Telescope.FindHome()</a> (external)
        """
        self._put("findhome", 60)   # Extended timeout for bleeping sync method

    def MoveAxis(self, Axis: TelescopeAxes, Rate: float) -> None:
        """Move the mount about the given axis at the given angular rate.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True
        after *successfully* starting the axis rotation operation. See Notes,
        and :ref:`async_faq`

        Args:
            Axis: :py:class:`TelecopeAxes`, the axis about which rotation is desired
            Rate: The rate or rotation desired (deg/sec)

        Raises:
            NotImplementedException: If this feature is not implemented (:py:attr:`CanMoveAxis` = False)
            InvalidOperationException: If the mount is parked (:py:attr:`AtPark` = True)
            InvalidValueException: If the axis or rate value is not valid.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to determine if the mount is moving, however you must explicitly
              call MoveAxis() with a zero rate to stop motion about the given axis.
            * This is a complex feature, see :ref:`moveaxis-faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            |MoveAxis|

            .. |MoveAxis| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.MoveAxis" target="_blank">
                Telescope.MoveAxis()</a> (external)
        """
        self._put("moveaxis", Axis=Axis.value, Rate=Rate)

    def Park(self) -> None:
        """Start slewing the mount to its park position.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True
        if the park operation has *successfully* been started, or
        :py:attr:`Slewing` = False which means the mount is already parked
        (and of course :py:attr:`AtPark` will already be True). See Notes,
        and :ref:`async_faq`

        Raises:
            NotImplementedException: If the mount does not support parking.
                In this case :py:attr:`CanPark` will be False.
            NotConnectedException: If the device is not connected
            ParkedException: If :py:attr:`AtPark` is True
            SlavedException: If :py:attr:`Slaved` is True
            DriverException:An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`AtPark` property
              to monitor the operation. When the the park position has been
              *successfully* reached, :py:attr:`AtPark` becomes True, and
              :py:attr:`Slewing` becomes False.  See :ref:`async_faq`
            * An app should check :py:attr:`AtPark` before calling Park().

        .. admonition:: Master Interfaces Reference
            :class: green

            |Park|

            .. |Park| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Park" target="_blank">
                Telescope.Park()</a> (external)
        """
        self._put("park")

    def PulseGuide(self, Direction: GuideDirections, Duration: int) -> None:
        """Pulse guide in the specified direction for the specified time (ms).

        **Non-blocking**: See Notes, and :ref:`async_faq`

        Args:
            Direction: :py:class:`~alpaca.telescope.GuideDirections`
            Interval: duration of the guide move, milliseconds

        Raises:
            InvalidValueException: If either the direction or the duration are invalid
            NotImplementedException: If the mount does not support pulse guiding
                (:py:attr:`CanPulseGuide` property is False)
            NotConnectedException: If the device is not connected.
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous**: The method returns as soon the pulse-guiding operation
              has been *successfully* started, with :py:attr:`IsPulseGuiding` property True.
              However, you may find that :py:attr:`IsPulseGuiding` is False when you get
              around to checking it if the 'pulse' is short. This is still a success if you
              get False back and not an exception. See :ref:`async_faq`
            * Some mounts have implemented this as a Synchronous (blocking) operation. This
              is deprecated and will be prohbited in the future.
            * :py:class:`~alpaca.telescope.GuideDirections` for North and South
              have varying interpretations
              by German Equatorial mounts. Some GEM mounts interpret North to be
              the same rotation direction of the declination axis regardless of
              their pointing state ("side of the pier"). Others truly implement
              North and South by reversing the dec-axis rotation depending on
              their pointing state. **Apps must be prepared for either behavior**.

        .. admonition:: Master Interfaces Reference
            :class: green

            |PulseGuide|

            .. |PulseGuide| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.PulseGuide" target="_blank">
                Telescope.PulseGuide()</a> (external)
        """
        self._put("pulseguide", Direction=Direction.value, Duration=Duration)

    def SetPark(self) -> None:
        """Set the telescope's park position to its current position.

        Raises:
            NotImplementedException: If the mount does not support the setting
                of the park position. In this case :py:attr:`CanSetPark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SetPark|

            .. |SetPark| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SetPark" target="_blank">
                Telescope.SetPark()</a> (external)
        """
        self._put("setpark")

    def SlewToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToAltAzAsync(self, Azimuth: float, Altitude: float) -> None:
        """Start a slew to the given local horizontal coordinates. See Notes.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Args:
            Azimuth: Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude: Altitude coordinate (degrees, positive up).

        Raises:
            ParkedException: If :py:attr:`AtPark` is True
            InvalidValueException: If either of the coordinates are invalid
            NotImplementedException: If the mount does not support alt/az slewing.
                In this case :py:attr:`CanSlewAltAz` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to monitor the operation. When the the requested coordinates have been
              *successfully* reached, :py:attr:`Slewing` becomes False.
              If SlewToAltAzAsync() returns with :py:attr:`Slewing` = False then
              the mount was already at the  requested coordinates, which is also a
              success See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            |SlewToAltAzAsync|

            .. |SlewToAltAzAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToAltAzAsync" target="_blank">
                Telescope.SlewToAltAzAsync()</a> (external)
        """
        self._put("slewtoaltazasync", Azimuth=Azimuth, Altitude=Altitude)

    def SlewToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToCoordinatesAsync(self, RightAscension: float, Declination: float):
        """Start a slew to the given equatorial coordinates. See Notes.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Args:
            RightAscension: Right Ascension coordinate (hours).
            Declination: Declination coordinate (degrees).

        Raises:
            ParkedException: If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support async slewing
                to equatorial coordinates. In this case :py:attr:`CanSlewAsync` will be False.
            InvalidValueException: If either of the coordinates are invalid
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to monitor the operation. When the the requested coordinates have been
              *successfully* reached, :py:attr:`Slewing` becomes False.
              If SlewToCoordinatesAsync() returns with :py:attr:`Slewing` = False then
              the mount was already at the requested coordinates, which is also a
              success See :ref:`async_faq`
            * The given coordinates must match the mount's :py:attr:`EquatorialSystem`.
            * The given coordinates are copied to the :py:attr:`TargetRightAscension` and
              :py:attr:`TargetDeclination` properties.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SlewToCoordinatesAsync|

            .. |SlewToCoordinatesAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToCoordinatesAsync" target="_blank">
                Telescope.SlewToCoordinatesAsync()</a> (external)
        """
        self._put("slewtocoordinatesasync", RightAscension=RightAscension, Declination=Declination)

    def SlewToTarget(self) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToTargetAsync(self) -> None:
        """Start a slew to the coordinates in :py:attr:`TargetRightAscension` and
        :py:attr:`TargetDeclination`.. See Notes.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Raises:
            ParkedException: If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support async slewing
                to equatorial coordinates. In this case :py:attr:`CanSlewAsync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to monitor the operation. When the the target coordinates have been
              *successfully* reached, :py:attr:`Slewing` becomes False.
              If SlewToCoordinatesAsync() returns with :py:attr:`Slewing` = False then
              the mount was already at the target coordinates, which is also a
              success See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            |SlewToTargetAsync|

            .. |SlewToTargetAsync| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToTargetAsync" target="_blank">
                Telescope.SlewToTargetAsync()</a> (external)
        """
        self._put("slewtotargetasync")

    def SyncToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """Match the mount's alt/az coordinates with the given alt/az coordinates

        Args:
            Azimuth: Corrected Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude: Corrected Altitude coordinate (degrees, positive up).

        Raises:
            ParkedException: If :py:attr:`AtPark` is True
            InvalidValueException: If either of the coordinates are invalid
            NotImplementedException: If the mount does not support alt/az
                sync. In this case :py:attr:`CanSyncAltAz` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SyncToAltAz|

            .. |SyncToAltAz| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToAltAz" target="_blank">
                Telescope.SyncToAltAz()</a> (external)
        """
        self._put("synctoaltaz", Azimuth=Azimuth, Altitude=Altitude)

    def SyncToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """Match the mount's equatorial coordinates with the given equatorial coordinates

        Args:
            RightAscension: Corrected Right Ascension coordinate (hours).
            Declination: Corrected Declination coordinate (degrees).

        Raises:
            ParkedException: [REVIEW] If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support equatorial
                coordinate synchronization. In this case
                :py:attr:`CanSync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SyncToCoordinates|

            .. |SyncToCoordinates| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToCoordinates" target="_blank">
                Telescope.SyncToCoordinates()</a> (external)
        """
        self._put(
            "synctocoordinates", RightAscension=RightAscension, Declination=Declination
        )

    def SyncToTarget(self) -> None:
        """Match the mount's equatorial coordinates with :py:attr:TargetRightAscension and
        :py:attr:`TargetDeclination`.

        Raises:
            ParkedException: If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support equatorial
                coordinate synchronization. In this case
                :py:attr:`CanSync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            |SyncToTarget|

            .. |SyncToTarget| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToTarget" target="_blank">
                Telescope.SyncToTarget()</a> (external)
        """
        self._put("synctotarget")

    def Unpark(self) -> None:
        """Takes the mount out of parked state

        Raises:
            NotImplementedException: If this method is not implemented. In this case
                :py:attr:`CanUnpark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * Unparking a mount that is not parked is harmless and will always be
              successful.

        .. admonition:: Master Interfaces Reference
            :class: green

            |Unpark|

            .. |Unpark| raw:: html

                <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Unpark" target="_blank">
                Telescope.Unpark()</a> (external)
        """
        self._put("unpark")
