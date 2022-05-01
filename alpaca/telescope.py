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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        super().__init__(address, "telescope", device_number, protocol)

    @property
    def AlignmentMode(self) -> AlignmentModes:
        """The current mount alignment mode.

        Raises:
            NotImplementedException: If the mount cannot report its alignment mode.
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
              this property (if implemented) will raise 
              :py:class:`~alpaca.exceptions.DriverException` when read.
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

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
        """The mount is in motion resulting from a slew or a move-axis. See :ref:`async_faq`

        Raises:
            NotImplementedException: If the property is not implemented (none of the CanSlew
                properties are True, this is a manual mount)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * This is the correct property to use to determine *successful* completion of 
              a (non-blocking) :py:meth:`SlewToCoordinatesAsync()`, :py:meth:`SlewToTargetAsync()`,
              :py:meth:`SlewToCoordinatesAsync()`, or by writing to :py:attr:`SideOfPier`
              to force a flip. 
            * See :ref:`async_faq`
            * Slewing will be True immediately upon 
              returning from any of these calls, and will remain True until *successful* 
              completion, at which time Slewing will become False.
            * You might see Slewing = False on returning from a slew or move-axis
              if the operation takes a very short time. If you see False (and not an exception)
              in this state, you can be certain that the operation completed *successfully*.
            * Slewing will not be True during pulse-guiding or application of tracking 
              offsets.

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.


        """
        return self._get("slewsettletime")
    @SlewSettleTime.setter
    def SlewSettleTime(self, SlewSettleTime: int):
        self._put("slewsettletime", SlewSettleTime=SlewSettleTime)

    @property
    def TargetDeclination(self) -> float:
        """(Read/Write) Set or return the target declination. See Notes.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range -90 through
                90 degrees.
            InvalidOperationException: If the application must set the TargetDeclination
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * This is a pre-set target coordinate for :py:meth:`SlewToTargetAsync()`
              and :py:meth:`SyncToTarget()`
            * Target coordinates are for the current :py:attr:`EquatorialSystem`.
       
        """
        return self._get("targetdeclination")
    @TargetDeclination.setter
    def TargetDeclination(self, TargetDeclination: float):
        self._put("targetdeclination", TargetDeclination=TargetDeclination)

    @property
    def TargetRightAscension(self) -> float:
        """(Read/Write) Set or return the target declination. See Notes.

        Raises:
            NotImplementedException: If the property is not implemented
            InvalidValueException: If the given value is outside the range -180 through
                180 degrees.
            InvalidOperationException: If the application must set the TargetRightAscension
                before reading it, but has not. See Notes.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * This is a pre-set target coordinate for :py:meth:`SlewToTargetAsync()`
              and :py:meth:`SyncToTarget()`
            * Target coordinates are for the current :py:attr:`EquatorialSystem`.
        
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * When on, the mount will use the last selected :py:attr:`TrackingRate`.
            * Even if the mount doesn't support changing this, it will report the
              current state. 

        """
        return self._get("tracking")
    @Tracking.setter
    def Tracking(self, Tracking: bool):
        self._put("tracking", Tracking=Tracking)

    @property
    def TrackingRate(self) -> DriveRates:
        """(Read/Write) The current (sidereal) tracking rate of the mount. See Notes.

        Raises:
            InvalidValueException: If value being written is not one of the 
                :py:class:`DriveRates`, or if the requested rate is not 
                supported by the mount (not all are). 
            NotImplementedException: If the mount doesn't support writing this 
                property to change the tracking rate.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Even if the mount doesn't support changing this, it will report the
              current state. 

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * At a minimum, this list will contain an item for 
              :py:class:`~DriveRates.driveSidereal`
        """
        return self._get("trackingrates")

    @property
    def UTCDate(self) -> datetime:
        """(Read/Write) The UTC date/time of the mount's internal clock. See Notes.

        You may write either a Python datetime (tz=UTC) or an ISO 8601 string
        for example:: 
        
            2022-04-22T20:21:01.123+00:00

        Raises:
            InvalidValueException: if an illegal ISO 8601 string or a bad Python 
                datetime value is written to change the time. See Notes.
            NotImplementedException: If the mount doesn't support writing this 
                property to change the UTC time
            InvalidOperationException: When UTCDate is read and the 
                mount cannot provide this property itslef and a value has 
                not yet be established by writing to the property.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Changing time by writing to this property can be done with either a
              Python datetime value or an ISO 8601 string, for example
              '2022-04-22T20:21:01.123+00:00'.
            * Even if the mount doesn't support changing this, it will report the
              current UTC date/time. The value may be derived from the system clock
              by the driver if the mount doesn't provide it. 
            * If the UTC date/time is being derived from the system clock, you will 
              not be able to write this  (you'll get 
              :py:class:`~exceptions.NotImplementedException`).


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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * See :py:meth:`MoveAxis()` for details.
            * An empty list will be returned if :py:meth:`MoveAxis()` is not supported.
            * Returned rates will always be positive, it is up to you to choose the 
              positive or negative rate for your call to :py:meth:`MoveAxis()`.

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        """
        return self._get("canmoveaxis", Axis=Axis.value)

    def DestinationSideOfPier(self, RightAscension: float, Declination: float) -> PierSide:
        """Predicts the pointing state (PierSide) after a GEM slews to given coordinates at this instant. 

        Provided so apps can manage GEM flipping during an image sequence. See 
        :py:attr:`SideOfPier`, :ref:`dsop-faq`, and :ref:`ptgstate-faq`

        Raises:
            InvalidValueException: An invalid axis value is specified.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        """
        return self._get("destinationsideofpier", RightAscension=RightAscension, Declination=Declination)

    def AbortSlew(self) -> None:
        """Immediatley stops an asynchronous slew in progress.

        Raises:
            NotImplementedException: If this feature is not implemented. TODO with the 
                deprecation of sync methods, this should be required.
            InvalidOperationException: TODO [Review New] If the mount is parked (:py:attr:`AtPark` = True)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes: 
            * Effective only after an asynchronous slew/move call to 
              :py:meth:`SlewToTargetAsync()`, :py:meth:`SlewToCoordinatesAsync()`, 
              :py:meth:`SlewToAltAzAsync()`, or :py:meth:`MoveAxis()`. 
            * Does nothing if no slew/motion is in progress.
            * Tracking is returned to its pre-slew state. 

        
        """
        self._put("abortslew")

    def FindHome(self) -> None:
        """Move the mount to the "home" position.

        **BLOCKING** This will not return until completed. TODO This should be 
        deprecated and we need a FindHomeAsync(). The docs and the simulator both
        implement sync behavior. 
        
        Raises:
            NotImplementedException: If this feature is not implemented (:py:attr:`CanFindHome` = False)
            InvalidOperationException: If the mount is parked (:py:attr:`AtPark` = True)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
       
        Notes:
            * Returns only after the home position has been found. At this point the AtHome 
              property will be True. TODO [needs change!]

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to determine if the mount is moving, however you must explicitly 
              call MoveAxis() with a zero rate to stop motion about the given axis.
            * This is a complex feature, see :ref:`moveaxis-faq`
        """
        self._put("moveaxis", Axis=Axis.value, Rate=Rate)

    def Park(self) -> None:
        """Start slewing the mount to its park position.

        **Non-blocking**: Returns immediately with :py:attr:`Slewing` = True 
        if the park operation has *successfully* been started, or 
        :py:attr:`Slewing` = False which means the mount is already parked 
        (and of course :py:attr:`AtPark` will already be True). See Notes, 
        and :ref:`async_faq`  TODO [Review] I believe most mounts already 
        implement this async. Should we just go with it?

        Raises:
            NotImplementedException: If the mount does not support parking. 
                In this case :py:attr:`CanPark` will be False.
            NotConnectedException: If the device is not connected
            ParkedException: TODO [REVIEW] If :py:attr:`AtPark` is True
            SlavedException: TODO [REVIEW] If :py:attr:`Slaved` is True
            DriverException:If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`AtPark` property
              to monitor the operation. When the the park position has been 
              *successfully* reached, :py:attr:`AtPark` becomes True, and 
              :py:attr:`Slewing` becomes False.  See :ref:`async_faq`
            * An app should check :py:attr:`AtPark` before calling Park().

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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * **Asynchronous**: The method returns as soon the pulse-guiding operation
              has been *successfully* started, with :py:attr:`IsPulseGuiding` property True. 
              However, you may find that :py:attr:`IsPulseGuiding' is False when you get 
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
        """
        self._put("pulseguide", Direction=Direction.value, Duration=Duration)

    def SetPark(self) -> None:
        """Set the telescope's park position to its current position.
        
        Raises:
            NotImplementedException: If the mount does not support the setting
                of the park position. In this case :py:attr:`CanSetPark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
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
            ParkedException: TODO [REVIEW] If :py:attr:`AtPark` is True
            InvalidValueException: If either of the coordinates are invalid 
            NotImplementedException: If the mount does not support alt/az slewing. 
                In this case :py:attr:`CanSlewAltAz` will be False.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to monitor the operation. When the the requested coordinates have been 
              *successfully* reached, :py:attr:`Slewing` becomes False. 
              If SlewToAltAzAsync() returns with :py:attr:`Slewing` = False then 
              the mount was already at the  requested coordinates, which is also a 
              success See :ref:`async_faq`

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
            ParkedException: TODO [REVIEW] If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support async slewing
                to equatorial coordinates. In this case :py:attr:`CanSlewAsync` will be False.
            InvalidValueException: If either of the coordinates are invalid 
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
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
            ParkedException: TODO [REVIEW] If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support async slewing
                to equatorial coordinates. In this case :py:attr:`CanSlewAsync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * **Asynchronous** (non-blocking): Use the :py:attr:`Slewing` property
              to monitor the operation. When the the target coordinates have been 
              *successfully* reached, :py:attr:`Slewing` becomes False. 
              If SlewToCoordinatesAsync() returns with :py:attr:`Slewing` = False then 
              the mount was already at the target coordinates, which is also a 
              success See :ref:`async_faq`

        """
        self._put("slewtotargetasync")

    def SyncToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """Match the mount's alt/az coordinates with the given alt/az coordinates

        Args:
            Azimuth: Corrected Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude: Corrected Altitude coordinate (degrees, positive up).

        Raises:
            ParkedException: TODO [REVIEW] If :py:attr:`AtPark` is True
            InvalidValueException: If either of the coordinates are invalid 
            NotImplementedException: If the mount does not support alt/az
                sync. In this case :py:attr:`CanSyncAltAz` will be False.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        """
        self._put("synctoaltaz", Azimuth=Azimuth, Altitude=Altitude)

    def SyncToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """Match the mount's equatorial coordinates with the given equatorial coordinates

        Args:
            RightAscension: Corrected Right Ascension coordinate (hours).
            Declination: Corrected Declination coordinate (degrees).

        Raises:
            ParkedException: TODO [REVIEW] If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support equatorial
                coordinate synchronization. In this case 
                :py:attr:`CanSync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        self._put(
            "synctocoordinates", RightAscension=RightAscension, Declination=Declination
        )

    def SyncToTarget(self) -> None:
        """Match the mount's equatorial coordinates with :py:attr:TargetRightAscension and
        :py:attr:`TargetDeclination`. 

        Raises:
            ParkedException: TODO [REVIEW] If :py:attr:`AtPark` is True
            NotImplementedException: If the mount does not support equatorial
                coordinate synchronization. In this case 
                :py:attr:`CanSync` will be False.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        self._put("synctotarget")

    def Unpark(self) -> None:
        """Takes the mount out of parked state
        
        Raises:
            NotImplementedException: If this method is not implemented. In this case 
                :py:attr:`CanUnpark` will be False.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Unparking a mount that is not parked is harmless and will always be
              successful.
              
        """
        self._put("unpark")
