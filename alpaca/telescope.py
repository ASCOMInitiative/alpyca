from datetime import datetime
from typing import List, Any
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
    drivelunar      = 1, 'Lunar tracking rate (14.685 arcseconds per second).'
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
    pierWest        = 1, 'Unknown or indeterminate.' 
    pierUnknown     = -1, 'Through the pole pointing state - Mount on the West side of pier (looking East)'

class TelescopeAxes(DocIntEnum):
    axisPrimary     = 0, 'Primary axis (e.g., Right Ascension or Azimuth).'
    axisSecondary   = 1, 'Secondary axis (e.g., Declination or Altitude).'
    axisTertiary    = 2, 'Tertiary axis (e.g. imager rotator/de-rotator).'

class Rate(object):
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        super().__init__(address, "telescope", device_number, protocol)

    @property
    def AlignmentMode(self) -> AlignmentModes:
        """The current mount alignment mode.

        Raises:
            NotImplementedException: TODO [REALLY? Should this be required?]
                If the mount cannot report its alignment mode.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return AlignmentModes(self._get("alignmentmode"))

    @property
    def Altitude(self) -> float:
        """The mount's current Altitude (degrees) above the horizon.

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("altitude")

    @property
    def ApertureArea(self) -> float:
        """The telescope's aperture area (square meters).

        Raises:
            NotImplementedException:Not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes: 
            * The area takes into account any obstructions; it is the actual
              light-gathering area.

        """
        return self._get("aperturearea")

    @property
    def ApertureDiameter(self) -> float:
        """Return the telescope's effective aperture (meters).

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("aperturediameter")

    @property
    def AtHome(self) -> bool:
        """The mount is at the home position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * True if the telescope is stopped in the Home position. Can be True
              only following a FindHome() operation.
            * Will become False immediately upon any slewing operation
            * Will always be False if the telescope does not support homing. Use
              :py:attr:`CanFindHome` to determine if the mount supports homing.
            * TODO [REVIEW] This should be the completion property for async
              FindHomeAsync().

        """
        return self._get("athome")

    @property
    def AtPark(self) -> bool:
        """The telescope is at the park position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * True if the telescope is stopped in the Park position. Can be True
              only following successful completion of a :py:meth:`Park()` operation.
            * When parked, the telescope will be stationary or restricted to a small 
              safe range of movement. :py:attr:`Tracking` will be False.
            * You must take the telescope out of park by calling :py:meth:`Unpark()`;
              attempts to slew enabling tracking while parked will raise an exception.
            * Will always be False if the telescope does not support parking. Use
              :py:attr:`CanPark` to determine if the mount supports parking.
            * TODO [REVIEW] This should be the completion property for async
              ParkAsync(). I  think we have established that Park is already
              asynch? If so I will document that.

        """
        return self._get("atpark")

    @property
    def Azimuth(self) -> float:
        """The azimuth (degrees) at which the telescope is currently pointing.

        Raises:
            NotImplementedException: Alt-Az not implemented by the device
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Azimuth is per the usual alt/az coordinate convention: degrees
              North-referenced, positive East/clockwise.
              
        """
        return self._get("azimuth")

    @property
    def CanFindHome(self) -> bool:
        """The mount can find its home position.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
 
        Notes:
            * See :py:meth:`FindHome()`
               
        """
        return self._get("canfindhome")

    @property
    def CanPark(self) -> bool:
        """The mount can be parked.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * See :py:meth:`Park()`
        
        """
        return self._get("canpark")

    @property
    def CanPulseGuide(self) -> bool:
        """The mount can be pulse guided.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:attr:`PulseGuide`

        """
        return self._get("canpulseguide")

    @property
    def CanSetDeclinationRate(self) -> bool:
        """The Declination tracking rate may be offset.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:attr:`DeclinationRate`

        """
        return self._get("cansetdeclinationrate")

    @property
    def CanSetGuideRates(self) -> bool:
        """The guiding rates for :py:meth:'PulseGuide()` can be adjusted

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:attr:`PulseGuide()`.

        """
        return self._get("cansetguiderates")

    @property
    def CanSetPark(self) -> bool:
        """The mount's park position can be set.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:attr:`SetPark()`

        """
        return self._get("cansetpark")

    @property
    def CanSetPierSide(self) -> bool:
        """The mount can be force-flipped via setting :py:attr:`SideOfPier`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:attr:`SideOfPier`.
            * Will always be False for non-German mounts

        """
        return self._get("cansetpierside")

    @property
    def CanSetRightAscensionRate(self) -> bool:
        """The Right Ascension tracking rate may be offset

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:attr:`RightAscensionRate`.

        """
        return self._get("cansetrightascensionrate")

    @property
    def CanSetTracking(self) -> bool:
        """The mount's sidereal tracking may be turned on and off

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:attr:`Tracking`.

        """
        return self._get("cansettracking")

    @property
    def CanSlew(self) -> bool:
        """The mount can slew to equatorial coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:meth:`SlewToCoordinates()`, :py:meth:`SlewToCoordinatesAsync()`
              :py:meth:`SlewToTarget()`, and :py:meth:`SlewToTargetAsync()`.

        Attention:
            Do not use synchronous methods unless the mount cannot do asynchronous
            slewing (:py:attr:`CanSlewAsync` = False). Synchronous methods will be
            deprecated in the next version of ITelescope.
       
        """
        return self._get("canslew")

    @property
    def CanSlewAsync(self) -> bool:
        """The mount can slew to equatorial coordinates synchronously.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * :py:attr:`CanSlew` will be True if CanSlewAsync is True.
            * See :py:meth:`SlewToCoordinatesAsync()`
              and :py:meth:`SlewToTargetAsync()`.

        Attention:
            Always use asynchronous slewing if at all possible (CanSlewAsync = True).
            Synchronous methods will be deprecated in the next version of ITelescope.

        """
        return self._get("canslewasync")

    @property
    def CanSlewAltAz(self) -> bool:
        """The mount can slew to alt/az coordinates.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:meth:`SlewToAltAz()` and :py:meth:`SlewToAltAzAsync()`.

        Attention:
            Do not use synchronous methods unless the mount cannot do asynchronous
            slewing (:py:attr:`CanSlewAltAzAsync` = False). Synchronous methods will be
            deprecated in the next version of ITelescope.
       
        """
        return self._get("canslewaltaz")

    @property
    def CanSlewAltAzAsync(self) -> bool:
        """The mount can slew to alt/az coordinates asynchronously.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * :py:attr:`CanSlewAltAz` will be True if CanSlewAltAzAsync is True.
            * See :py:meth:`SlewToAltAzAsync()`.

        Attention:
            Always use asynchronous slewing if at all possible (CanSlewAltAzAsync = True).
            Synchronous methods will be deprecated in the next version of ITelescope.

        """
        return self._get("canslewaltazasync")

    @property
    def CanSync(self) -> bool:
        """The mount can be synchronized to equatorial coordinates.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:meth:`SyncToCoordinates()`.

        """
        return self._get("cansync")

    @property
    def CanSyncAltAz(self) -> bool:
        """The mount can be synchronized to alt/az coordinates.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:meth:`SyncToAltAz()`.

        """
        return self._get("cansyncaltaz")

    @property
    def CanUnpark(self) -> bool:
        """The mount can be unparked
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:meth:`Unpark()` and :py:meth:`Park()`.

        """
        return self._get("canunpark")

    @property
    def Declination(self) -> float:
        """The mount's current Declination (degrees, see Notes)

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Declination will be in the equinox given by the current value of 
              :py:attr:`EquatorialSystem`.

        """
        return self._get("declination")

    @property
    def DeclinationRate(self) -> float:
        """(Read/Write) The mount's declination tracking rate (see Notes).

        Raises:
            NotImplementedException: If :py:attr:`CanSetDeclinationRate` is False,
            yet an attempt is made to write to this property.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * If the driver does not know whether the attached telescope does its 
              own refraction, and if the driver does not itself calculate refraction, 
              this property (if implemented) will raise an error when read.
              TODO [What error? Clarify this]
            * If the mount indicates that it can apply refraction, yet you wish to 
              calculate your own (more accurate) correction, try setting this to 
              False then, if successful, supply your own refracted coordinates.
            * If you set this to True, and the mount (already) does refraction, or
              if you set this to Fales, and the mount (already) does not do 
              refraction, no exception will be raised. 

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * See :py:class:`EquatorialCoordinateType`. 
            * Most mounts use topocentric coordinates. Some high-end research 
              mounts use J2000 coordinates. 

        """
        return EquatorialCoordinateType(self._get("equatorialsystem"))

    @property
    def FocalLength(self) -> float:
        """Return the telescope's focal length in meters.

        Raises:
            NotImplementedException: Focal length is not available from the mount
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("focallength")

    @property
    def GuideRateDeclination(self) -> float:
        """(Read/Write) The current Declination rate offset (deg/sec) for guiding.

        Raises:
            InvalidValueException: If an invalid guide rate is set
            NotImplementedException: Rate cannot be set, :py:attr:`CanSetGuideRates` = False
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * This is the rate for both hardware/relay guiding and for 
              :py:meth:`PulseGuide()`.
            * The mount may not support separate right ascension and declination
              guide rates. If so, setting either rate will set the other to the
              same value.
            * This value will be set to a default upon startup. 

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * This is the rate for both hardware/relay guiding and for 
              :py:meth:`PulseGuide()`.
            * The mount may not support separate right ascension and declination
              guide rates. If so, setting either rate will set the other to the
              same value.
            * This value will be set to a default upon startup. 

        """
        return self._get("guideraterightascension")
    @GuideRateDeclination.setter
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
          * A pulse guide command may be so short that you won't see this equal to True. 
            If you can read False after calling :py:meth:`PulseGuide()`, then you know it 
            completed *successfully*. See :ref:`async_faq`
        
        """
        return self._get("ispulseguiding")

    @property
    def RightAscension(self) -> float:
        """The mount's current right ascension (hours) in the current :py:attr:`EquatorialSystem`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("rightascension")

    @property
    def RightAscensionRate(self) -> float:
        """(Read/Write) The mount's right ascension tracking rate (see Notes).

        Raises:
            NotImplementedException: If :py:attr:`CanSetRightAscensionRate` is False,
            yet an attempt is made to write to this property.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * RightAscensionRate is an offset from the currently selected :py:attr:TrackingRate`
              given in (sidereal) seconds of RA per *sidereal* second.
            * To convert a given rate in units of sidereal seconds per UTC (clock) second, 
              multiply the value by 0.9972695677 (the number of UTC seconds in a sidereal 
              second) then set the RightAscensionRate property.
            * The supported range for this property is mount-specific. 
            * Offset tracking is most commonly used to track a solar system object such 
              as a minor planet or comet.
            * Offset tracking may also be used (less commonly) as a method for reducing 
              dynamic mount errors.
            * If offset tracking is in effect (non-zero), and a slew is initiated, the
              mount will continue to update the slew destination coordinates at the 
              given offset rate.
            * Use the :py:attr:`Tracking` property to stop and start tracking. 
        """
        return self._get("rightascensionrate")
    @RightAscensionRate.setter
    def RightAscensionRate(self, RightAscensionRate: float):
        self._put("rightascensionrate", RightAscensionRate=RightAscensionRate)

    @property
    def SideOfPier(self)  -> PierSide:
        """(Read/Write) Set or return the mount's pointing state. See :ref:`ptgstate-faq`

        Raises:
            NotImplementedException: If the mount does not report its pointing state,
                or if it doesn't support force-flipping by writing to SideOfPier
                (:py:attr:`CanSetPierSide` = False).
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * May optionally be written-to to force a flip on a German mount
            * See :ref:`ptgstate-faq`
        
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is required for a driver to calculate this from the system clock if 
              the mount has no accessible source of sidereal time.
            * Local Apparent Sidereal Time is the sidereal time used for pointing 
              telescopes, and thus must be calculated from the Greenwich Mean 
              Sidereal time, longitude, nutation in longitude and true ecliptic 
              obliquity. 
            * Local Apparent Sidereal Time is the topocentric Right Ascension 
              of the meridian at the current instant. TODO [REVIEW is this right?]

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Some mounts supply this via input to their control systems, in 
              other scenarios the application will set this on initialization.
            * If a change is made via SiteElevation, most mounts will save the value
              persistently across power off/on.
            * If the value hasn't been set by any means, an InvalidOperationException
              will be raised.

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * This is geodetic (map) latitude, degrees, WGS84, positive North.
            * Some mounts supply this via input to their control systems, in 
              other scenarios the application will set this on initialization.
            * If a change is made via SiteLatitude, most mounts will save the value
              persistently across power off/on.
            * If the value hasn't been set by any means, an InvalidOperationException
              will be raised.
        
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

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
        
        """
        return self._get("sitelongitude")
    @SiteLongitude.setter
    def SiteLongitude(self, SiteLongitude: float):
        self._put("sitelongitude", SiteLongitude=SiteLongitude)

    @property
    def Slewing(self) -> bool:
        """The mount is in motion resulting from a slew or a MoveAxis. See :ref:`async_faq`

        Notes:
            * This is the correct property to use to determine *successful* completion of 
              a (non-blocking) :py:meth:`SlewToCoordinatesAsync()`, :py:meth:`SlewToTargetAsync()`,
              :py:meth:`SlewToCoordinatesAsync()`, or by writing to :py:attr:`SideOfPier`
              to force a flip. 
            * See :ref:`async_faq`
            * Slewing will be True immediately upon 
              returning from any of these calls, and will remain True until *successful* 
              completion, at which time Slewing will become False.
            * Slewing will not be True during pulse-guiding or application of tracking 
              offsets.

        """
        return self._get("slewing")

    @property
    def SlewSettleTime(self) -> int:
        """Set or return the post-slew settling time.

        Args:
            SlewSettleTime (int): Settling time (integer sec.).

        Returns:
            Returns the post-slew settling time (sec.) if not set.

        """
        return self._get("slewsettletime")
    @SlewSettleTime.setter
    def SlewSettleTime(self, SlewSettleTime: int):
        self._put("slewsettletime", SlewSettleTime=SlewSettleTime)

    @property
    def TargetDeclination(self) -> float:
        """Set or return the target declination of a slew or sync.

        Args:
            TargetDeclination (float): Target declination(degrees)
        
        Returns:
            Declination (degrees, positive North) for the target of an equatorial slew
            or sync operation.
        
        """
        return self._get("targetdeclination")
    @TargetDeclination.setter
    def TargetDeclination(self, TargetDeclination: float):
        self._put("targetdeclination", TargetDeclination=TargetDeclination)

    @property
    def TargetRightAscension(self) -> float:
        """Set or return the current target right ascension.

        Args:
            TargetRightAscension (float): Target right ascension (hours).
        
        Returns:
            Right ascension (hours) for the target of an equatorial slew or sync
            operation.

        """
        return self._get("targetrightascension")
    @TargetRightAscension.setter
    def TargetRightAscension(self, TargetRightAscension: float):
        self._put("targetrightascension", TargetRightAscension=TargetRightAscension)

    @property
    def Tracking(self) -> bool:
        """Enable, disable, or indicate whether the telescope is tracking.

        Args:
            Tracking (bool): Tracking enabled / disabled.
        
        Returns:
            State of the telescope's sidereal tracking drive.
        
        """
        return self._get("tracking")
    @Tracking.setter
    def Tracking(self, Tracking: bool):
        self._put("tracking", Tracking=Tracking)

    @property
    def TrackingRate(self) -> DriveRates:
        """Set or return the current tracking rate (enum DriveRates).

        Args:
            Enum DriveRates: 
                0 = driveSidereal, 1 = driveLunar, 2 = driveSolar, 3 = driveKing.
        
        Returns:
            Current tracking rate of the telescope's sidereal drive if not set.
        **TODO** Verify enum usage both ways

        """
        return DriveRates(self._get("trackingrate"))
    @TrackingRate.setter
    def TrackingRate(self, TrackingRate: DriveRates):
        self._put("trackingrate", TrackingRate=TrackingRate.value)

    @property
    def TrackingRates(self) -> List[DriveRates]:
        """Return a list of supported enum DriveRates values.

        Returns:
            List of supported enum DriveRates values that describe the permissible values of
            the TrackingRate property for this telescope type.

        """
        return self._get("trackingrates")

    @property
    def UTCDate(self) -> datetime:
        """Set or return the UTC date/time of the telescope's internal clock.

        Args:
            UTCDate: UTC date/time as an str or datetime.
        
        Returns:
            datetime of the UTC date/time if not set.
        **TODO** Check setting with both formats

        """
        return dateutil.parser.parse(self._get("utcdate"))
    @UTCDate.setter
    def UTCDate(self, UTCDate: datetime):
        if type(UTCDate) is str:
            data = UTCDate
        elif type(UTCDate) is datetime:
            data = UTCDate.isoformat()  # Convert to ISO string
        else:
            raise TypeError("Must be an ISO 8601 string or a Python datetime value")
        self._put("utcdate", UTCDate=data)

    def AxisRates(self, Axis: TelescopeAxes) -> List[Rate]:
        """Return rates at which the telescope may be moved about the specified axis.

        Returns:
            The rates at which the telescope may be moved about the specified axis 
            (enum TelescopeAxes) by the MoveAxis(int, float) method.
        
        """
        l = []
        jList = self._get("axisrates", Axis=Axis.value)
        for j in jList:
            l.append(Rate(j["Maximum"], j["Minimum"]))
        return l

    def CanMoveAxis(self, Axis: TelescopeAxes) -> bool:
        """Indicate whether the telescope can move about the requested axis.

        Returns:
            True if this telescope can move about the requested axis.

        """
        return self._get("canmoveaxis", Axis=Axis.value)

    def DestinationSideOfPier(self, RightAscension: float, Declination: float) -> PierSide:
        """Predict the pointing state (PierSide) after a German equatorial mount slews to given coordinates.

        Args:
            RightAscension (float): Right Ascension coordinate (0.0 to 23.99999999
                hours).
            Declination (float): Declination coordinate (-90.0 to +90.0 degrees).

        Returns:
            Pointing state (enum PierSide)that a German equatorial mount will be in 
            if it slews to the given coordinates. 

        """
        return self._get("destinationsideofpier", RightAscension=RightAscension, Declination=Declination)

    def AbortSlew(self) -> None:
        """Immediatley stops a slew in progress."""
        self._put("abortslew")

    def FindHome(self) -> None:
        """Move the mount to the "home" position."""
        # **TODO** This is synchronous now, etc.
        self._put("findhome", 30)   # Extended timeout for bleeping sync method

    def MoveAxis(self, Axis: TelescopeAxes, Rate: float) -> None:
        """Move a telescope axis at the given rate.

        Args:
            Axis (int): The axis about which rate information is desired
            (enum TelescopeAxes): 0 = axisPrimary, 1 = axisSecondary, 
            2 = axisTertiary.
            Rate (float): The rate of motion (deg/sec) about the specified axis

        """
        self._put("moveaxis", Axis=Axis.value, Rate=Rate)

    def Park(self) -> None:
        """Park the mount."""
        # **TODO** This is synchronous, etc.
        self._put("park")

    def PulseGuide(self, Direction: GuideDirections, Duration: int) -> None:
        """Move the scope in the given direction for the given time.

        Args:
            Direction (enum GuideDirections): Direction in which the guide-rate 
            motion is to be made.
            Duration (int): Duration of the guide-rate motion (milliseconds).
        
        """
        self._put("pulseguide", Direction=Direction.value, Duration=Duration)

    def SetPark(self) -> None:
        """Set the telescope's park position to its current position."""
        self._put("setpark")

    def SlewToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToAltAzAsync(self, Azimuth: float, Altitude: float) -> None:
        """Slew asynchronously to the given local horizontal coordinates.

        Args:
            Azimuth (float): Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude (float): Altitude coordinate (degrees, positive up).

        """
        self._put("slewtoaltazasync", Azimuth=Azimuth, Altitude=Altitude)

    def SlewToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToCoordinatesAsync(self, RightAscension: float, Declination: float):
        """Slew asynchronously to the given equatorial coordinates.

        Args:
            RightAscension (float): Right Ascension coordinate (hours).
            Declination (float): Declination coordinate (degrees).
        
        """
        self._put("slewtocoordinatesasync", RightAscension=RightAscension, Declination=Declination)

    def SlewToTarget(self) -> None:
        """DEPRECATED - Do not use this via Alpaca"""
        raise NotImplementedException("Synchronous methods are deprecated, not available via Alpaca.")

    def SlewToTargetAsync(self) -> None:
        """Asynchronously slew to the TargetRightAscension and TargetDeclination coordinates."""
        self._put("slewtotargetasync")

    def SyncToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """Sync to the given local horizontal coordinates.

        Args:
            Azimuth (float): Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude (float): Altitude coordinate (degrees, positive up).

        """
        self._put("synctoaltaz", Azimuth=Azimuth, Altitude=Altitude)

    def SyncToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """Sync to the given equatorial coordinates.

        Args:
            RightAscension (float): Right Ascension coordinate (hours).
            Declination (float): Declination coordinate (degrees).

        """
        self._put(
            "synctocoordinates", RightAscension=RightAscension, Declination=Declination
        )

    def SyncToTarget(self) -> None:
        """Sync to the TargetRightAscension and TargetDeclination coordinates."""
        self._put("synctotarget")

    def Unpark(self) -> None:
        """Unpark the mount."""
        self._put("unpark")
