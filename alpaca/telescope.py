# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# telescope - Implements ASCOM Alpaca Telescope device classes and enums
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
# 21-Aug-22 (rbd) 2.0.2 Fix driveRates enum (GitHub issue #3). Fix descriptive
#                 text for pierWest and pierUnknown (GitHub issue #5)
# 08-Mar-24 (rbd) 3.0.0 Add Master Interfaces refs to all members
# 13-Oct-24 (rbd) 3.0.1 For PDF rendering no change to logic
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
    """Describes a range of rates supported by the :meth:`MoveAxis()` method"""

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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        """
        super().__init__(address, "telescope", device_number, protocol)

    @property
    def AlignmentMode(self) -> AlignmentModes:
        """The current mount alignment mode.

        Raises:
            NotImplementedException: If the mount cannot report its alignment mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |AlignmentMode|

                .. |AlignmentMode| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AlignmentMode" target="_blank">
                    Telescope.AlignmentMode()</a> (external)

            .. only:: rinoh

                `Telescope.AlignmentMode <https://ascom-standards.org/newdocs/telescope.html#Telescope.AlignmentMode>`_
        """
        return AlignmentModes(self._get("alignmentmode"))

    @property
    def Altitude(self) -> float:
        """The mount's current Altitude (degrees) above the horizon.

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Altitude|

                .. |Altitude| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Altitude" target="_blank">
                    Telescope.Altitude</a> (external)

            .. only:: rinoh

                `Telescope.Altitude <https://ascom-standards.org/newdocs/telescope.html#Telescope.Altitude>`_
        """
        return self._get("altitude")

    @property
    def ApertureArea(self) -> float:
        """The telescope's aperture area (square meters).

        Raises:
            NotImplementedException:Not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * The area takes into account any obstructions; it is the actual
              light-gathering area.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ApertureArea|

                .. |ApertureArea| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.ApertureArea" target="_blank">
                    Telescope.ApertureArea</a> (external)

            .. only:: rinoh

                `Telescope.ApertureArea <https://ascom-standards.org/newdocs/telescope.html#Telescope.ApertureArea>`_
        """
        return self._get("aperturearea")

    @property
    def ApertureDiameter(self) -> float:
        """Return the telescope's effective aperture (meters).

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ApertureDiameter|

                .. |ApertureDiameter| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.ApertureDiameter" target="_blank">
                    Telescope.ApertureDiameter</a> (external)

            .. only:: rinoh

                `Telescope.ApertureDiameter <https://ascom-standards.org/newdocs/telescope.html#Telescope.ApertureDiameter>`_
        """
        return self._get("aperturediameter")

    @property
    def AtHome(self) -> bool:
        """The mount is at the home position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is the correct property to use to determine *successful* completion of
              the (non-blocking) :meth:`FindHome()` operation. See :ref:`async_faq`
            * True if the telescope is stopped in the Home position. Can be True
              only following a FindHome() operation.
            * Will become False immediately upon any slewing operation
            * Will always be False if the telescope does not support homing. Use
              :attr:`CanFindHome` to determine if the mount supports homing.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |AtHome|

                .. |AtHome| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AtHome" target="_blank">
                    Telescope.AtHome</a> (external)

            .. only:: rinoh

                `Telescope.AtHome <https://ascom-standards.org/newdocs/telescope.html#Telescope.AtHome>`_
        """
        return self._get("athome")

    @property
    def AtPark(self) -> bool:
        """The telescope is at the park position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is the correct property to use to determine *successful* completion of
              the (non-blocking) :meth:`Park()` operation. See :ref:`async_faq`
            * True if the telescope is stopped in the Park position. Can be True
              only following successful completion of a :meth:`Park()` operation.
            * When parked, the telescope will be stationary or restricted to a small
              safe range of movement. :attr:`Tracking` will be False.
            * You must take the telescope out of park by calling :meth:`Unpark()`;
              attempts to slew enabling tracking while parked will raise
              a :py:class:`~alpaca.exceptions.ParkedException`.
            * Will always be False if the telescope does not support parking. Use
              :attr:`CanPark` to determine if the mount supports parking.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |AtPark|

                .. |AtPark| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AtPark" target="_blank">
                    Telescope.AtPark</a> (external)

            .. only:: rinoh

                `Telescope.AtPark <https://ascom-standards.org/newdocs/telescope.html#Telescope.AtPark>`_
        """
        return self._get("atpark")

    @property
    def Azimuth(self) -> float:
        """The azimuth (degrees) at which the telescope is currently pointing.

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Azimuth is per the usual alt/az coordinate convention: degrees
              North-referenced, positive East/clockwise.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Azimuth|

                .. |Azimuth| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Azimuth" target="_blank">
                    Telescope.Azimuth</a> (external)

            .. only:: rinoh

                `Telescope.Azimuth <https://ascom-standards.org/newdocs/telescope.html#Telescope.Azimuth>`_
        """
        return self._get("azimuth")

    @property
    def CanFindHome(self) -> bool:
        """The mount can find its home position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`FindHome()`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanFindHome|

                .. |CanFindHome| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanFindHome" target="_blank">
                    Telescope.CanFindHome</a> (external)

            .. only:: rinoh

                `Telescope.CanFindHome <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanFindHome>`_
        """
        return self._get("canfindhome")

    @property
    def CanPark(self) -> bool:
        """The mount can be parked.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`Park()`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanPark|

                .. |CanPark| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanPark" target="_blank">
                    Telescope.CanPark</a> (external)

            .. only:: rinoh

                `Telescope.CanPark <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanPark>`_
        """
        return self._get("canpark")

    @property
    def CanPulseGuide(self) -> bool:
        """The mount can be pulse guided.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :attr:`PulseGuide`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanPulseGuide|

                .. |CanPulseGuide| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanPulseGuide" target="_blank">
                    Telescope.CanPulseGuide</a> (external)

            .. only:: rinoh

                `Telescope.CanPulseGuide <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanPulseGuide>`_
        """
        return self._get("canpulseguide")

    @property
    def CanSetDeclinationRate(self) -> bool:
        """The Declination tracking rate may be offset.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :attr:`DeclinationRate`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSetDeclinationRate|

                .. |CanSetDeclinationRate| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetDeclinationRate" target="_blank">
                    Telescope.CanSetDeclinationRate</a> (external)

            .. only:: rinoh

                `Telescope.CanSetDeclinationRate <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetDeclinationRate>`_
        """
        return self._get("cansetdeclinationrate")

    @property
    def CanSetGuideRates(self) -> bool:
        """The guiding rates for :meth:`PulseGuide()` can be adjusted

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :attr:`PulseGuide()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSetGuideRates|

                .. |CanSetGuideRates| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetGuideRates" target="_blank">
                    Telescope.CanSetGuideRates</a> (external)

            .. only:: rinoh

                `Telescope.CanSetGuideRates <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetGuideRates>`_
        """
        return self._get("cansetguiderates")

    @property
    def CanSetPark(self) -> bool:
        """The mount's park position can be set.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :attr:`SetPark()`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSetPark|

                .. |CanSetPark| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetPark" target="_blank">
                    Telescope.CanSetPark</a> (external)

            .. only:: rinoh

                `Telescope.CanSetPark <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetPark>`_
        """
        return self._get("cansetpark")

    @property
    def CanSetPierSide(self) -> bool:
        """The mount can be force-flipped via setting :attr:`SideOfPier`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :attr:`SideOfPier`.
            * Will always be False for non-German mounts

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSetPierSide|

                .. |CanSetPierSide| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetPierSide" target="_blank">
                    Telescope.CanSetPierSide</a> (external)

            .. only:: rinoh

                `Telescope.CanSetPierSide <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetPierSide>`_
        """
        return self._get("cansetpierside")

    @property
    def CanSetRightAscensionRate(self) -> bool:
        """The Right Ascension tracking rate may be offset

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :attr:`RightAscensionRate`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSetRightAscensionRate|

                .. |CanSetRightAscensionRate| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetRightAscensionRate" target="_blank">
                    Telescope.CanSetRightAscensionRate</a> (external)

            .. only:: rinoh

                `Telescope.CanSetRightAscensionRate <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetRightAscensionRate>`_
        """
        return self._get("cansetrightascensionrate")

    @property
    def CanSetTracking(self) -> bool:
        """The mount's sidereal tracking may be turned on and off

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :attr:`Tracking`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSetTracking|

                .. |CanSetTracking| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetTracking" target="_blank">
                    Telescope.CanSetTracking</a> (external)

            .. only:: rinoh

                `Telescope.CanSetTracking <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSetTracking>`_
        """
        return self._get("cansettracking")

    @property
    def CanSlew(self) -> bool:
        """The mount can slew to equatorial coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`SlewToCoordinates()`, :meth:`SlewToCoordinatesAsync()`
              :meth:`SlewToTarget()`, and :meth:`SlewToTargetAsync()`.

        Attention:
            Do not use synchronous methods unless the mount cannot do asynchronous
            slewing (:attr:`CanSlewAsync` = False). Synchronous methods will be
            deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSlew|

                .. |CanSlew| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlew" target="_blank">
                    Telescope.CanSlew</a> (external)

            .. only:: rinoh

                `Telescope.CanSlew <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlew>`_
        """
        return self._get("canslew")

    @property
    def CanSlewAsync(self) -> bool:
        """The mount can slew to equatorial coordinates synchronously.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * :attr:`CanSlew` will be True if CanSlewAsync is True.
            * See :meth:`SlewToCoordinatesAsync()`
              and :meth:`SlewToTargetAsync()`.

        Attention:
            Always use asynchronous slewing if at all possible (CanSlewAsync = True).
            Synchronous methods will be deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSlewAsync|

                .. |CanSlewAsync| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAsync" target="_blank">
                    Telescope.CanSlewAsync</a> (external)

            .. only:: rinoh

                `Telescope.CanSlewAsync <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAsync>`_
        """
        return self._get("canslewasync")

    @property
    def CanSlewAltAz(self) -> bool:
        """The mount can slew to alt/az coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`SlewToAltAz()` and :meth:`SlewToAltAzAsync()`.

        Attention:
            Do not use synchronous methods unless the mount cannot do asynchronous
            slewing (:attr:`CanSlewAltAzAsync` = False). Synchronous methods will be
            deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSlewAltAz|

                .. |CanSlewAltAz| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAltAz" target="_blank">
                    Telescope.CanSlewAltAz</a> (external)

            .. only:: rinoh

                `Telescope.CanSlewAltAz <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAltAz>`_
        """
        return self._get("canslewaltaz")

    @property
    def CanSlewAltAzAsync(self) -> bool:
        """The mount can slew to alt/az coordinates asynchronously.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * :attr:`CanSlewAltAz` will be True if CanSlewAltAzAsync is True.
            * See :meth:`SlewToAltAzAsync()`.

        Attention:
            Always use asynchronous slewing if at all possible (CanSlewAltAzAsync = True).
            Synchronous methods will be deprecated in the next version of ITelescope.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSlewAltAzAsync|

                .. |CanSlewAltAzAsync| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAltAzAsync" target="_blank">
                    Telescope.CanSlewAltAzAsync</a> (external)

            .. only:: rinoh

                `Telescope.CanSlewAltAzAsync <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSlewAltAzAsync>`_
        """
        return self._get("canslewaltazasync")

    @property
    def CanSync(self) -> bool:
        """The mount can be synchronized to equatorial coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`SyncToCoordinates()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSync|

                .. |CanSync| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSync" target="_blank">
                    Telescope.CanSync</a> (external)

            .. only:: rinoh

                `Telescope.CanSync <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSync>`_
        """
        return self._get("cansync")

    @property
    def CanSyncAltAz(self) -> bool:
        """The mount can be synchronized to alt/az coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`SyncToAltAz()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSyncAltAz|

                .. |CanSyncAltAz| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSyncAltAz" target="_blank">
                    Telescope.CanSyncAltAz</a> (external)

            .. only:: rinoh

                `Telescope.CanSyncAltAz <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanSyncAltAz>`_
        """
        return self._get("cansyncaltaz")

    @property
    def CanUnpark(self) -> bool:
        """The mount can be unparked

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`Unpark()` and :meth:`Park()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanUnpark|

                .. |CanUnpark| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanUnpark" target="_blank">
                    Telescope.CanUnpark</a> (external)

            .. only:: rinoh

                `Telescope.CanUnpark <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanUnpark>`_
        """
        return self._get("canunpark")

    @property
    def Declination(self) -> float:
        """The mount's current Declination (degrees) in the current
        :attr:`EquatorialSystem` (see Notes)

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Declination will be in the equinox given by the current value of
              :attr:`EquatorialSystem`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Declination|

                .. |Declination| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Declination" target="_blank">
                    Telescope.Declination</a> (external)

            .. only:: rinoh

                `Telescope.Declination <https://ascom-standards.org/newdocs/telescope.html#Telescope.Declination>`_
        """
        return self._get("declination")

    @property
    def DeclinationRate(self) -> float:
        """(Read/Write) The mount's declination tracking rate (see Notes).

        Raises:
            NotImplementedException: If :attr:`CanSetDeclinationRate` is False,
            yet an attempt is made to write to this property.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * DeclinationRate is an offset from 0 (no change in declination), given in arc seconds
              per SI (atomic) second. (Please note that the units of :attr:`RightAscensionRate`
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

            .. only:: html

                |DeclinationRate|

                .. |DeclinationRate| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.DeclinationRate" target="_blank">
                    Telescope.DeclinationRate</a> (external)

                |RARateFAQ|

                .. |RARateFAQ| raw:: html

                    <a href="https://ascom-standards.org/newdocs/trkoffset-faq.html#what-are-rightascensionrate-and-declinationrate-and-how-are-they-used" target="_blank">
                    What are RightAscensionRate and DeclinationRate and how are they used?</a> (external)

            .. only:: rinoh

                `Telescope.DeclinationRate <https://ascom-standards.org/newdocs/telescope.html#Telescope.DeclinationRate>`_
                `What are RightAscensionRate and DeclinationRate and how are they used? <https://ascom-standards.org/newdocs/trkoffset-faq.html#what-are-rightascensionrate-and-declinationrate-and-how-are-they-used>`_

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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
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

            .. only:: html

                |DoesRefraction|

                .. |DoesRefraction| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.DoesRefraction" target="_blank">
                    Telescope.DoesRefraction</a> (external)

            .. only:: rinoh

                `Telescope.DoesRefraction <https://ascom-standards.org/newdocs/telescope.html#Telescope.DoesRefraction>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :py:class:`EquatorialCoordinateType`.
            * Most mounts use topocentric coordinates. Some high-end research
              mounts use J2000 coordinates.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |EquatorialSystem|

                .. |EquatorialSystem| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.EquatorialSystem" target="_blank">
                    Telescope.EquatorialSystem</a> (external)

            .. only:: rinoh

                `Telescope.EquatorialSystem <https://ascom-standards.org/newdocs/telescope.html#Telescope.EquatorialSystem>`_
        """
        return EquatorialCoordinateType(self._get("equatorialsystem"))

    @property
    def FocalLength(self) -> float:
        """Return the telescope's focal length in meters.

        Raises:
            NotImplementedException: Focal length is not available from the mount
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |FocalLength|

                .. |FocalLength| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.FocalLength" target="_blank">
                    Telescope.FocalLength</a> (external)

            .. only:: rinoh

                `Telescope.FocalLength <https://ascom-standards.org/newdocs/telescope.html#Telescope.FocalLength>`_
        """
        return self._get("focallength")

    @property
    def GuideRateDeclination(self) -> float:
        """(Read/Write) The current Declination rate offset (deg/sec) for guiding.

        Raises:
            InvalidValueException: If an invalid guide rate is set
            NotImplementedException: Rate cannot be set, :attr:`CanSetGuideRates` = False
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is the rate for both hardware/relay guiding and for
              :meth:`PulseGuide()`.
            * The mount may not support separate right ascension and declination
              guide rates. If so, setting either rate will set the other to the
              same value.
            * This value will be set to a default upon startup.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |GuideRateDeclination|

                .. |GuideRateDeclination| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.GuideRateDeclination" target="_blank">
                    Telescope.GuideRateDeclination</a> (external)

            .. only:: rinoh

                `Telescope.GuideRateDeclination <https://ascom-standards.org/newdocs/telescope.html#Telescope.GuideRateDeclination>`_
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
            NotImplementedException: Rate cannot be set, :attr:`CanSetGuideRates` = False
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is the rate for both hardware/relay guiding and for
              :meth:`PulseGuide()`.
            * The mount may not support separate right ascension and declination
              guide rates. If so, setting either rate will set the other to the
              same value.
            * This value will be set to a default upon startup.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |GuideRateRightAscension|

                .. |GuideRateRightAscension| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.GuideRateRightAscension" target="_blank">
                    Telescope.GuideRateRightAscension</a> (external)

            .. only:: rinoh

                `Telescope.GuideRateRightAscension <https://ascom-standards.org/newdocs/telescope.html#Telescope.GuideRateRightAscension>`_
        """
        return self._get("guideraterightascension")
    @GuideRateRightAscension.setter
    def GuideRateRightAscension(self, GuideRateRightAscension: float):
        self._put("guideraterightascension", GuideRateRightAscension=GuideRateRightAscension)

    @property
    def IsPulseGuiding(self) -> bool:
        """The mount is currently executing a :meth:`PulseGuide()` command.

        Use this property to determine when a (non-blocking) pulse guide command
        has completed. See Notes and :ref:`async_faq`

        Raises:
            NotImplementedException: Pulse guiding is not supported
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
          * A pulse guide command may be so short that you won't see this equal to True.
            If you can read False after calling :meth:`PulseGuide()`, then you know it
            completed *successfully*. See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |IsPulseGuiding|

                .. |IsPulseGuiding| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.IsPulseGuiding" target="_blank">
                    Telescope.IsPulseGuiding</a> (external)

            .. only:: rinoh

                `Telescope.IsPulseGuiding <https://ascom-standards.org/newdocs/telescope.html#Telescope.IsPulseGuiding>`_
        """
        return self._get("ispulseguiding")

    @property
    def RightAscension(self) -> float:
        """The mount's current right ascension (hours) in the current
        :attr:`EquatorialSystem`. See Notes.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |RightAscension|

                .. |RightAscension| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.RightAscension" target="_blank">
                    Telescope.RightAscension</a> (external)

            .. only:: rinoh

                `Telescope.RightAscension <https://ascom-standards.org/newdocs/telescope.html#Telescope.RightAscension>`_
        """
        return self._get("rightascension")

    @property
    def RightAscensionRate(self) -> float:
        """(Read/Write) Read or set a secular rate of change to the mount’s RightAscension
        (seconds of RA per **sidereal** second). See |RARateFAQ|

        Raises:
            NotImplementedException: If :attr:`CanSetRightAscensionRate` is False,
            yet an attempt is made to write to this property.
            InvalidOperationException: If the current :attr:`TrackingRate` is not
               ``driveSidereal``.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
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
            * Use the :attr:`Tracking` property to stop and start tracking.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |RightAscensionRate|

                .. |RightAscensionRate| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.RightAscensionRate" target="_blank">
                    Telescope.RightAscensionRate</a> (external)

                |RARateFAQ|

            .. only:: rinoh

                `Telescope.RightAscensionRate <https://ascom-standards.org/newdocs/telescope.html#Telescope.RightAscensionRate>`_
                `What are RightAscensionRate and DeclinationRate and how are they used? <https://ascom-standards.org/newdocs/trkoffset-faq.html#what-are-rightascensionrate-and-declinationrate-and-how-are-they-used>`_
        """
        return self._get("rightascensionrate")
    @RightAscensionRate.setter
    def RightAscensionRate(self, RightAscensionRate: float):
        self._put("rightascensionrate", RightAscensionRate=RightAscensionRate)

    @property
    def SideOfPier(self)  -> PierSide:
        """(Read/Write) Start a change of, or return, the mount's pointing state. See :ref:`ptgstate-faq`

        **Non-blocking**: Writing to *change* pointing state returns immediately
        with :attr:`Slewing` = True if the state change (e.g. GEM flip) operation
        has *successfully* been started. See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If the mount does not report its pointing state,
                at all, or if it doesn't support changing pointing state
                (e.g.force-flipping) by writing to SideOfPier
                (:attr:`CanSetPierSide` = False).
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking) if writing SideOfPier to force a
              pointing state change (e.g. GEM flip): Use the :attr:`Slewing` property
              to monitor the operation. When the pointing state change has been
              *successfully* completed, :attr:`Slewing` becomes False.
              If writing SideOfPier returns with :attr:`Slewing` = False then
              the mount was already in the requested pointing state, which is also a
              success.  See :ref:`async_faq`
            * May optionally be written-to to force a flip on a German mount
            * See :ref:`ptgstate-faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SideOfPier|

                .. |SideOfPier| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SideOfPier" target="_blank">
                    Telescope.SideOfPier</a> (external)

            .. only:: rinoh

                `Telescope.SideOfPier <https://ascom-standards.org/newdocs/telescope.html#Telescope.SideOfPier>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is required for a driver to calculate this from the system clock if
              the mount has no accessible source of sidereal time.
            * Local Apparent Sidereal Time is the sidereal time used for pointing
              telescopes, and thus must be calculated from the Greenwich Mean
              Sidereal time, longitude, nutation in longitude and true ecliptic
              obliquity.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SiderealTime|

                .. |SiderealTime| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiderealTime" target="_blank">
                    Telescope.SiderealTime</a> (external)

            .. only:: rinoh

                `Telescope.SiderealTime <https://ascom-standards.org/newdocs/telescope.html#Telescope.SiderealTime>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Some mounts supply this via input to their control systems, in
              other scenarios the application will set this on initialization.
            * If a change is made via SiteElevation, most mounts will save the value
              persistently across power off/on.
            * If the value hasn't been set by any means, an InvalidOperationException
              will be raised.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SiteElevation|

                .. |SiteElevation| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteElevation" target="_blank">
                    Telescope.SiteElevation</a> (external)

            .. only:: rinoh

                `Telescope.SiteElevation <https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteElevation>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is geodetic (map) latitude, degrees, WGS84, positive North.
            * Some mounts supply this via input to their control systems, in
              other scenarios the application will set this on initialization.
            * If a change is made via SiteLatitude, most mounts will save the value
              persistently across power off/on.
            * If the value hasn't been set by any means, an InvalidOperationException
              will be raised.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SiteLatitude|

                .. |SiteLatitude| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteLatitude" target="_blank">
                    Telescope.SiteLatitude</a> (external)

            .. only:: rinoh

                `Telescope.SiteLatitude <https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteLatitude>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
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

            .. only:: html

                |SiteLongitude|

                .. |SiteLongitude| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteLongitude" target="_blank">
                    Telescope.SiteLongitude</a> (external)

            .. only:: rinoh

                `Telescope.SiteLongitude <https://ascom-standards.org/newdocs/telescope.html#Telescope.SiteLongitude>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is the correct property to use to determine *successful* completion of
              a (non-blocking) :meth:`SlewToCoordinatesAsync()`, :meth:`SlewToTargetAsync()`,
              :meth:`SlewToCoordinatesAsync()`, or by writing to :attr:`SideOfPier`
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

            .. only:: html

                |Slewing|

                .. |Slewing| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Slewing" target="_blank">
                    Telescope.Slewing</a> (external)

            .. only:: rinoh

                `Telescope.Slewing <https://ascom-standards.org/newdocs/telescope.html#Telescope.Slewing>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SlewSettleTime|

                .. |SlewSettleTime| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewSettleTime" target="_blank">
                    Telescope.SlewSettleTime</a> (external)

            .. only:: rinoh

                `Telescope.SlewSettleTime <https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewSettleTime>`_
        """
        return self._get("slewsettletime")
    @SlewSettleTime.setter
    def SlewSettleTime(self, SlewSettleTime: int):
        self._put("slewsettletime", SlewSettleTime=SlewSettleTime)

    @property
    def TargetDeclination(self) -> float:
        """(Read/Write) Set or return the target declination in the current
        :attr:`EquatorialSystem`. See Notes.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range -90 through
                90 degrees.
            InvalidOperationException: If the application must set the TargetDeclination
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is a pre-set target coordinate for :meth:`SlewToTargetAsync()`
              and :meth:`SyncToTarget()`
            * Target coordinates are for the current :attr:`EquatorialSystem`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |TargetDeclination|

                .. |TargetDeclination| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TargetDeclination" target="_blank">
                    Telescope.TargetDeclination</a> (external)

            .. only:: rinoh

                `Telescope.TargetDeclination <https://ascom-standards.org/newdocs/telescope.html#Telescope.TargetDeclination>`_
        """
        return self._get("targetdeclination")
    @TargetDeclination.setter
    def TargetDeclination(self, TargetDeclination: float):
        self._put("targetdeclination", TargetDeclination=TargetDeclination)

    @property
    def TargetRightAscension(self) -> float:
        """(Read/Write) Set or return the target right ascension (hours) in the current
        :attr:`EquatorialSystem`

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range 0 to
                24 hours.
            InvalidOperationException: If the application must set the TargetRightAscension
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This is a pre-set target coordinate for :meth:`SlewToTargetAsync()`
              and :meth:`SyncToTarget()`
            * Target coordinates are for the current :attr:`EquatorialSystem`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |TargetRightAscension|

                .. |TargetRightAscension| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TargetRightAscension" target="_blank">
                    Telescope.TargetRightAscension</a> (external)

            .. only:: rinoh

                `Telescope.TargetRightAscension <https://ascom-standards.org/newdocs/telescope.html#Telescope.TargetRightAscension>`_
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
                :attr:`CanSetTracking` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * When on, the mount will use the last selected :attr:`TrackingRate`.
            * Even if the mount doesn't support changing this, it will report the
              current state.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Tracking|

                .. |Tracking| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Tracking" target="_blank">
                    Telescope.Tracking</a> (external)

            .. only:: rinoh

                `Telescope.Tracking <https://ascom-standards.org/newdocs/telescope.html#Telescope.Tracking>`_
        """
        return self._get("tracking")
    @Tracking.setter
    def Tracking(self, Tracking: bool):
        self._put("tracking", Tracking=Tracking)

    @property
    def TrackingRate(self) -> DriveRates:
        """(Read/Write) The current (sidereal) tracking rate of the mount,
        from :attr:`DriveRates`. See Notes.

        Raises:
            InvalidValueException: If value being written is not one of the
                :py:class:`DriveRates`, or if the requested rate is not
                supported by the mount (not all are).
            NotImplementedException: If the mount doesn't support writing this
                property to change the tracking rate.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Even if the mount doesn't support changing this, it will report the
              current state.
            * If this is any rate other than :py:class:`~DriveRates.driveSidereal` then
              :attr:`RightAscensionRate` and :attr:`DeclinationRate` will
              raise :py:class:`~alpaca.exceptions.InvalidOperationException`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |TrackingRate|

                .. |TrackingRate| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TrackingRate" target="_blank">
                    Telescope.TrackingRate</a> (external)

            .. only:: rinoh

                `Telescope.TrackingRate <https://ascom-standards.org/newdocs/telescope.html#Telescope.TrackingRate>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * At a minimum, this list will contain an item for
              :py:class:`~DriveRates.driveSidereal`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |TrackingRates|

                .. |TrackingRates| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.TrackingRates" target="_blank">
                    Telescope.TrackingRates</a> (external)

            .. only:: rinoh

                `Telescope.TrackingRates <https://ascom-standards.org/newdocs/telescope.html#Telescope.TrackingRates>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
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

            .. only:: html

                |UTCDate|

                .. |UTCDate| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.UTCDate" target="_blank">
                    Telescope.UTCDate</a> (external)

            .. only:: rinoh

                `Telescope.UTCDate <https://ascom-standards.org/newdocs/telescope.html#Telescope.UTCDate>`_
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
        """Angular rates at which the mount may be moved with :meth:`MoveAxis()`. See Notes.

        Returns:
            A list of :py:class:`Rate` objects, each of which specifies a minimum
            and a maximum angular rate at which the given axis of the mount may be
            moved.

        Raises:
            InvalidValueException: An invalid axis value is specified.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * See :meth:`MoveAxis()` for details.
            * An empty list will be returned if :meth:`MoveAxis()` is not supported.
            * Returned rates will always be positive, it is up to you to choose the
              positive or negative rate for your call to :meth:`MoveAxis()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |AxisRates|

                .. |AxisRates| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AxisRates" target="_blank">
                    Telescope.AxisRates()</a> (external)

            .. only:: rinoh

                `Telescope.AxisRates() <https://ascom-standards.org/newdocs/telescope.html#Telescope.AxisRates>`_
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
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanMoveAxis|

                .. |CanMoveAxis| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.CanMoveAxis" target="_blank">
                    Telescope.CanMoveAxis()</a> (external)

            .. only:: rinoh

                `Telescope.CanMoveAxis() <https://ascom-standards.org/newdocs/telescope.html#Telescope.CanMoveAxis>`_
        """
        return self._get("canmoveaxis", Axis=Axis.value)

    def DestinationSideOfPier(self, RightAscension: float, Declination: float) -> PierSide:
        """Predicts the pointing state (PierSide) after a GEM slews to given coordinates at this instant.

        Provided so apps can manage GEM flipping during an image sequence. See
        :attr:`SideOfPier`, :ref:`dsop-faq`, and :ref:`ptgstate-faq`

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
            InvalidOperationException: If the mount is parked (:attr:`AtPark` = True)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Effective only after an asynchronous slew/move call to
              :meth:`SlewToTargetAsync()`, :meth:`SlewToCoordinatesAsync()`,
              :meth:`SlewToAltAzAsync()`, or :meth:`MoveAxis()`.
            * Does nothing if no slew/motion is in progress.
            * Tracking is returned to its pre-slew state.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |AbortSlew|

                .. |AbortSlew| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.AbortSlew" target="_blank">
                    Telescope.AbortSlew()</a> (external)

            .. only:: rinoh

                `Telescope.AbortSlew() <https://ascom-standards.org/newdocs/telescope.html#Telescope.AbortSlew>`_
        """
        self._put("abortslew")

    def FindHome(self) -> None:
        """Start moving the mount to the "home" position.

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the homing operation has *successfully* been started, or
        :attr:`Slewing` = False which means the mount is already at its
        home position (and of course :attr:`AtHome` will already be True).
        See Notes, and :ref:`async_faq`

        Raises:
            NotImplementedException: If this feature is not implemented (:attr:`CanFindHome` = False)
            InvalidOperationException: If the mount is parked (:attr:`AtPark` = True)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking): Use the :attr:`AtHome` property
              to monitor the operation. When the mount has
              *successfully* reached its home position, :attr:`Slewing`
              becomes False and :attr:`AtHome`
              becomes True. See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |FindHome|

                .. |FindHome| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.FindHome" target="_blank">
                    Telescope.FindHome()</a> (external)

            .. only:: rinoh

                `Telescope.FindHome() <https://ascom-standards.org/newdocs/telescope.html#Telescope.FindHome>`_
        """
        self._put("findhome", 60)   # Extended timeout for bleeping sync method

    def MoveAxis(self, Axis: TelescopeAxes, Rate: float) -> None:
        """Move the mount about the given axis at the given angular rate.

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        after *successfully* starting the axis rotation operation. See Notes,
        and :ref:`async_faq`

        Args:
            Axis: :py:class:`TelecopeAxes`, the axis about which rotation is desired
            Rate: The rate or rotation desired (deg/sec)

        Raises:
            NotImplementedException: If this feature is not implemented (:attr:`CanMoveAxis` = False)
            InvalidOperationException: If the mount is parked (:attr:`AtPark` = True)
            InvalidValueException: If the axis or rate value is not valid.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking): Use the :attr:`Slewing` property
              to determine if the mount is moving, however you must explicitly
              call MoveAxis() with a zero rate to stop motion about the given axis.
            * This is a complex feature, see :ref:`moveaxis-faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |MoveAxis|

                .. |MoveAxis| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.MoveAxis" target="_blank">
                    Telescope.MoveAxis()</a> (external)

            .. only:: rinoh

                `Telescope.MoveAxis() <https://ascom-standards.org/newdocs/telescope.html#Telescope.MoveAxis>`_
        """
        self._put("moveaxis", Axis=Axis.value, Rate=Rate)

    def Park(self) -> None:
        """Start slewing the mount to its park position.

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the park operation has *successfully* been started, or
        :attr:`Slewing` = False which means the mount is already parked
        (and of course :attr:`AtPark` will already be True). See Notes,
        and :ref:`async_faq`

        Raises:
            NotImplementedException: If the mount does not support parking.
                In this case :attr:`CanPark` will be False.
            NotConnectedException: If the device is not connected
            ParkedException: If :attr:`AtPark` is True
            SlavedException: If :attr:`Slaved` is True
            DriverException:An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking): Use the :attr:`AtPark` property
              to monitor the operation. When the the park position has been
              *successfully* reached, :attr:`AtPark` becomes True, and
              :attr:`Slewing` becomes False.  See :ref:`async_faq`
            * An app should check :attr:`AtPark` before calling Park().

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Park|

                .. |Park| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Park" target="_blank">
                    Telescope.Park()</a> (external)

            .. only:: rinoh

                `Telescope.Park() <https://ascom-standards.org/newdocs/telescope.html#Telescope.Park>`_
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
                (:attr:`CanPulseGuide` property is False)
            NotConnectedException: If the device is not connected.
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous**: The method returns as soon the pulse-guiding operation
              has been *successfully* started, with :attr:`IsPulseGuiding` property True.
              However, you may find that :attr:`IsPulseGuiding` is False when you get
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

            .. only:: html

                |PulseGuide|

                .. |PulseGuide| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.PulseGuide" target="_blank">
                    Telescope.PulseGuide()</a> (external)

            .. only:: rinoh

                `Telescope.PulseGuide() <https://ascom-standards.org/newdocs/telescope.html#Telescope.PulseGuide>`_
        """
        self._put("pulseguide", Direction=Direction.value, Duration=Duration)

    def SetPark(self) -> None:
        """Set the telescope's park position to its current position.

        Raises:
            NotImplementedException: If the mount does not support the setting
                of the park position. In this case :attr:`CanSetPark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SetPark|

                .. |SetPark| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SetPark" target="_blank">
                    Telescope.SetPark()</a> (external)

            .. only:: rinoh

                `Telescope.SetPark() <https://ascom-standards.org/newdocs/telescope.html#Telescope.SetPark>`_
        """
        self._put("setpark")

    def SlewToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToAltAzAsync(self, Azimuth: float, Altitude: float) -> None:
        """Start a slew to the given local horizontal coordinates. See Notes.

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Args:
            Azimuth: Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude: Altitude coordinate (degrees, positive up).

        Raises:
            ParkedException: If :attr:`AtPark` is True
            InvalidValueException: If either of the coordinates are invalid
            NotImplementedException: If the mount does not support alt/az slewing.
                In this case :attr:`CanSlewAltAz` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking): Use the :attr:`Slewing` property
              to monitor the operation. When the the requested coordinates have been
              *successfully* reached, :attr:`Slewing` becomes False.
              If SlewToAltAzAsync() returns with :attr:`Slewing` = False then
              the mount was already at the  requested coordinates, which is also a
              success See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SlewToAltAzAsync|

                .. |SlewToAltAzAsync| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToAltAzAsync" target="_blank">
                    Telescope.SlewToAltAzAsync()</a> (external)

            .. only:: rinoh

                `Telescope.SlewToAltAzAsync() <https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToAltAzAsync>`_
        """
        self._put("slewtoaltazasync", Azimuth=Azimuth, Altitude=Altitude)

    def SlewToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToCoordinatesAsync(self, RightAscension: float, Declination: float):
        """Start a slew to the given equatorial coordinates. See Notes.

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Args:
            RightAscension: Right Ascension coordinate (hours).
            Declination: Declination coordinate (degrees).

        Raises:
            ParkedException: If :attr:`AtPark` is True
            NotImplementedException: If the mount does not support async slewing
                to equatorial coordinates. In this case :attr:`CanSlewAsync` will be False.
            InvalidValueException: If either of the coordinates are invalid
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking): Use the :attr:`Slewing` property
              to monitor the operation. When the the requested coordinates have been
              *successfully* reached, :attr:`Slewing` becomes False.
              If SlewToCoordinatesAsync() returns with :attr:`Slewing` = False then
              the mount was already at the requested coordinates, which is also a
              success See :ref:`async_faq`
            * The given coordinates must match the mount's :attr:`EquatorialSystem`.
            * The given coordinates are copied to the :attr:`TargetRightAscension` and
              :attr:`TargetDeclination` properties.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SlewToCoordinatesAsync|

                .. |SlewToCoordinatesAsync| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToCoordinatesAsync" target="_blank">
                    Telescope.SlewToCoordinatesAsync()</a> (external)

            .. only:: rinoh

                `Telescope.SlewToCoordinatesAsync() <https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToCoordinatesAsync>`_
        """
        self._put("slewtocoordinatesasync", RightAscension=RightAscension, Declination=Declination)

    def SlewToTarget(self) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToTargetAsync(self) -> None:
        """Start a slew to the coordinates in :attr:`TargetRightAscension` and
        :attr:`TargetDeclination`.. See Notes.

        **Non-blocking**: Returns immediately with :attr:`Slewing` = True
        if the slewing operation has *successfully* been started.
        See Notes, and :ref:`async_faq`

        Raises:
            ParkedException: If :attr:`AtPark` is True
            NotImplementedException: If the mount does not support async slewing
                to equatorial coordinates. In this case :attr:`CanSlewAsync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous** (non-blocking): Use the :attr:`Slewing` property
              to monitor the operation. When the the target coordinates have been
              *successfully* reached, :attr:`Slewing` becomes False.
              If SlewToCoordinatesAsync() returns with :attr:`Slewing` = False then
              the mount was already at the target coordinates, which is also a
              success See :ref:`async_faq`

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SlewToTargetAsync|

                .. |SlewToTargetAsync| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToTargetAsync" target="_blank">
                    Telescope.SlewToTargetAsync()</a> (external)

            .. only:: rinoh

                `Telescope.SlewToTargetAsync() <https://ascom-standards.org/newdocs/telescope.html#Telescope.SlewToTargetAsync>`_
        """
        self._put("slewtotargetasync")

    def SyncToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """Match the mount's alt/az coordinates with the given alt/az coordinates

        Args:
            Azimuth: Corrected Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude: Corrected Altitude coordinate (degrees, positive up).

        Raises:
            ParkedException: If :attr:`AtPark` is True
            InvalidValueException: If either of the coordinates are invalid
            NotImplementedException: If the mount does not support alt/az
                sync. In this case :attr:`CanSyncAltAz` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SyncToAltAz|

                .. |SyncToAltAz| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToAltAz" target="_blank">
                    Telescope.SyncToAltAz()</a> (external)

            .. only:: rinoh

                `Telescope.SyncToAltAz() <https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToAltAz>`_
        """
        self._put("synctoaltaz", Azimuth=Azimuth, Altitude=Altitude)

    def SyncToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """Match the mount's equatorial coordinates with the given equatorial coordinates

        Args:
            RightAscension: Corrected Right Ascension coordinate (hours).
            Declination: Corrected Declination coordinate (degrees).

        Raises:
            ParkedException: [REVIEW] If :attr:`AtPark` is True
            NotImplementedException: If the mount does not support equatorial
                coordinate synchronization. In this case
                :attr:`CanSync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SyncToCoordinates|

                .. |SyncToCoordinates| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToCoordinates" target="_blank">
                    Telescope.SyncToCoordinates()</a> (external)

            .. only:: rinoh

                `Telescope.SyncToCoordinates() <https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToCoordinates>`_
        """
        self._put(
            "synctocoordinates", RightAscension=RightAscension, Declination=Declination
        )

    def SyncToTarget(self) -> None:
        """Match the mount's equatorial coordinates with :attr:TargetRightAscension and
        :attr:`TargetDeclination`.

        Raises:
            ParkedException: If :attr:`AtPark` is True
            NotImplementedException: If the mount does not support equatorial
                coordinate synchronization. In this case
                :attr:`CanSync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SyncToTarget|

                .. |SyncToTarget| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToTarget" target="_blank">
                    Telescope.SyncToTarget()</a> (external)

            .. only:: rinoh

                `Telescope.SyncToTarget() <https://ascom-standards.org/newdocs/telescope.html#Telescope.SyncToTarget>`_
        """
        self._put("synctotarget")

    def Unpark(self) -> None:
        """Takes the mount out of parked state

        Raises:
            NotImplementedException: If this method is not implemented. In this case
                :attr:`CanUnpark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Unparking a mount that is not parked is harmless and will always be
              successful.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Unpark|

                .. |Unpark| raw:: html

                    <a href="https://ascom-standards.org/newdocs/telescope.html#Telescope.Unpark" target="_blank">
                    Telescope.Unpark()</a> (external)

            .. only:: rinoh

                `Telescope.Unpark() <https://ascom-standards.org/newdocs/telescope.html#Telescope.Unpark>`_
        """
        self._put("unpark")
