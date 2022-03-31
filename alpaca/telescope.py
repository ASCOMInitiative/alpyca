from enum import Enum
from datetime import datetime
from typing import List, Any
import dateutil.parser
from alpaca.device import Device

class AlignmentModes(Enum):
    algAltAz        = 0
    algPolar        = 1
    algGermanPolar  = 2

class DriveRates(Enum):
    driveSidereal   = 0
    drivelunar      = 1
    driveSolar      = 2
    driveKing       = 3

class EquatorialCoordinateType(Enum):
    equOther        = 0
    equTopocentric  = 1
    equJ2000        = 2
    equJ2050        = 3
    equLocalTopocentric = 1     # OBSOLETE, use Topocentric

class GuideDirections(Enum):    # Shared by Camera
    guideNorth      = 0
    guideSouth      = 1
    guideEast       = 2
    guideWest       = 3

class PierSide(Enum):
    pierEast        = 0
    pierWest        = 1
    pierUnknown     = -1

class TelescopeAxes(Enum):
    axisPrimary     = 0
    axisSecondary   = 1
    axisTertiary    = 2

class Rate(object):
    """Describes a range of rates supported by the MoveAxis()"""
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
        """Initialize Telescope object."""
        super().__init__(address, "telescope", device_number, protocol)

    @property
    def AlignmentMode(self) -> AlignmentModes:
        """Return the current mount alignment mode.

        Returns:
            Alignment mode of the mount (Alt/Az, Polar, German Polar).
        
        """
        return self._get("alignmentmode")

    @property
    def Altitude(self) -> float:
        """Return the mount's Altitude above the horizon.

        Returns:
            Altitude of the telescope's current position (degrees, positive up).

        """
        return self._get("altitude")

    @property
    def ApertureArea(self) -> float:
        """Return the telescope's aperture.

        Returns:
            Area of the telescope's aperture (square meters).

        """
        return self._get("aperturearea")

    @property
    def ApertureDiameter(self) -> float:
        """Return the telescope's effective aperture.

        Returns:
            Telescope's effective aperture diameter (meters).

        """
        return self._get("aperturediameter")

    @property
    def AtHome(self) -> bool:
        """Indicate whether the mount is at the home position.

        Returns:
            True if the mount is stopped in the Home position. Must be False if the
            telescope does not support homing.
        
        """
        return self._get("athome")

    @property
    def AtPark(self) -> bool:
        """Indicate whether the telescope is at the park position.

        Returns:
            True if the telescope has been put into the parked state by the seee park()
            method. Set False by calling the unpark() method.
        
        """
        return self._get("atpark")

    @property
    def Azimuth(self) -> float:
        """Return the telescope's aperture.
        
        Return:
            Azimuth of the telescope's current position (degrees, North-referenced,
            positive East/clockwise).

        """
        return self._get("azimuth")

    @property
    def CanFindHome(self) -> bool:
        """Indicate whether the mount can find the home position.
        
        Returns:
            True if this telescope is capable of programmed finding its home position.
        
        """
        return self._get("canfindhome")

    @property
    def CanPark(self) -> bool:
        """Indicate whether the telescope can be parked.

        Returns:
            True if this telescope is capable of programmed parking.
        
        """
        return self._get("canpark")

    @property
    def CanPulseGuide(self) -> bool:
        """Indicate whether the telescope can be pulse guided.

        Returns:
            True if this telescope is capable of software-pulsed guiding (via the
            pulseguide(int, int) method).
        
        """
        return self._get("canpulseguide")

    @property
    def CanSetDeclinationRate(self) -> bool:
        """Indicate whether the DeclinationRate property can be changed.

        Returns:
            True if the DeclinationRate property can be changed to provide offset
            tracking in the declination axis.

        """
        return self._get("cansetdeclinationrate")

    @property
    def CanSetGuideRates(self) -> bool:
        """Indicate whether the DeclinationRate property can be changed.

        Returns:
            True if the guide rate properties used for pulseguide(int, int) can ba
            adjusted.

        """
        return self._get("cansetguiderates")

    @property
    def CanSetPark(self) -> bool:
        """Indicate whether the telescope park position can be set.

        Returns:
            True if this telescope is capable of programmed setting of its park position
            (setpark() method).

        """
        return self._get("cansetpark")

    @property
    def CanSetPierSide(self) -> bool:
        """Indicate whether the telescope SideOfPier can be set.

        Returns:
            True if the SideOfPier property can be set, meaning that the mount can be
            forced to flip.
        
        """
        return self._get("cansetpierside")

    @property
    def CanSetRightAscension(self) -> bool:
        """Indicate whether the RightAscensionRate property can be changed.

        Returns:
            True if the RightAscensionRate property can be changed to provide offset
            tracking in the right ascension axis.
        
        """
        return self._get("cansetrightascensionrate")

    @property
    def CanSetTracking(self) -> bool:
        """Indicate whether the Tracking property can be changed.

        Returns:
            True if the Tracking property can be changed, turning telescope sidereal
            tracking on and off.
        
        """
        return self._get("cansettracking")

    @property
    def CanSlew(self) -> bool:
        """Indicate whether the telescope can slew to equatorial coordinates."""
        return self._get("canslew")

    @property
    def CanSlewAsync(self) -> bool:
        """Indicate whether the telescope can slew asynchronously."""
        return self._get("canslewasync")

    @property
    def CanSlewAltAz(self) -> bool:
        """Indicate whether the telescope can slew to AltAz coordinates."""
        return self._get("canslewaltaz")

    @property
    def CanSlewAltAzAsync(self) -> bool:
        """Indicate whether the telescope can slew asynchronusly to AltAz coordinates."""
        return self._get("canslewaltazasync")

    @property
    def CanSync(self) -> bool:
        """Indicate whether the telescope can sync to equatorial coordinates."""
        return self._get("cansync")

    @property
    def CanSyncAltAz(self) -> bool:
        """Indicate whether the telescope can sync to local horizontal coordinates."""
        return self._get("cansyncaltaz")

    @property
    def CanUnpark(self) -> bool:
        """Indicates whether the telescope can be unparked via UnPark()."""
        return self._get("canunpark")

    @property
    def Declination(self) -> float:
        """Return the telescope's declination (degrees, float).

        Notes:
            Reading the property will raise an error if the value is unavailable.

        Returns:
            The declination (degrees) of the telescope's current equatorial coordinates,
            in the coordinate system given by the EquatorialSystem property.
        
        """
        return self._get("declination")

    @property
    def DeclinationRate(self) -> float:
        """Set or return the telescope's declination tracking rate.

        Args:
            DeclinationRate (float, arcseconds per second).
        
        Returns:
            The declination tracking rate (arcseconds per second).
        
        """
        return self._get("declinationrate")
    @DeclinationRate.setter
    def DeclinationRate(self, DeclinationRate: float):
        self._put("declinationrate", DeclinationRate=DeclinationRate)

    @property
    def DoesRefraction(self) -> bool:
        """Indicate or determine if atmospheric refraction is applied to coordinates.

        Args:
            DoesRefraction (bool): Set True to make the telescope or driver apply
                atmospheric refraction to coordinates.
        
        Returns:   
            True if the telescope or driver applies atmospheric refraction to
            coordinates.

        """
        return self._get("doesrefraction")
    @DoesRefraction.setter
    def DoesRefraction(self, DoesRefraction: bool):
        self._put("doesrefraction", DoesRefraction=DoesRefraction)

    @property
    def EquatorialSystem(self) -> EquatorialCoordinateType:
        """Return the current equatorial coordinate system used by this telescope.

        Returns:
            Current equatorial coordinate system used by this telescope
            (Enum EquatorialCoordinateType)

        """
        return self._get("equatorialsystem")

    @property
    def FocalLength(self) -> float:
        """Return the telescope's focal length in meters.

        Returns:
            The telescope's focal length in meters.

        """
        return self._get("focallength")

    @property
    def GuideRateDeclination(self) -> float:
        """Set or return the current Declination rate offset for telescope guiding.

        Args:
            GuideRateDeclination (float): Declination movement rate offset
                (degrees/sec).

        """
        return self._get("guideratedeclination")
    @GuideRateDeclination.setter
    def GuideRateDeclination(self, GuideRateDeclination: float):
        self._put("guideratedeclination", GuideRateDeclination=GuideRateDeclination)

    @property
    def GuideRateRightAscension(self) -> float:
        """Set or return the current Right Ascension rate offset for telescope guiding.

        Args:
            GuideRateRightAscension (float): Right Ascension movement rate offset
                (degrees/sec).

        """
        return self._get("guideraterightascension")
    @GuideRateDeclination.setter
    def GuideRateRightAscension(self, GuideRateRightAscension: float):
        self._put("guideraterightascension", GuideRateRightAscension=GuideRateRightAscension)

    @property
    def IsPulseGuiding(self) -> bool:
        """Indicate whether the telescope is currently executing a PulseGuide command.

        Returns:
            True if a pulseguide(int, int) command is in progress, False otherwise.
        
        """
        return self._get("ispulseguiding")

    @property
    def RightAscension(self) -> float:
        """Return the telescope's right ascension coordinate.

        Returns:
            The right ascension (hours) of the telescope's current equatorial
            coordinates, in the coordinate system given by the EquatorialSystem
            property.

        """
        return self._get("rightascension")

    @property
    def RightAscensionRate(self) -> float:
        """Set or return the telescope's right ascension tracking rate.

        Args:
            RightAscensionRate (float): Right ascension tracking rate (arcseconds per
                second).

        """
        return self._get("rightascensionrate")
    @RightAscensionRate.setter
    def RightAscensionRate(self, RightAscensionRate: float):
        self._put("rightascensionrate", RightAscensionRate=RightAscensionRate)

    @property
    def SideOfPier(self)  -> PierSide:
        """Set or return the mount's pointing state.

        Args:
            SideOfPier (int): New pointing state. 0 = pierEast, 1 = pierWest
        
        Returns:
            Side of pier if not set.
        
            **TODO** Make sure enum is handled correctly
        """
        return self._get("sideofpier")
    @SideOfPier.setter
    def SideOfPier(self, SideOfPier: PierSide):
        self._put("sideofpier", SideOfPier=SideOfPier)

    @property
    def SiderealTime(self) -> float:
        """Return the local apparent sidereal time.

        Returns:
            The local apparent sidereal time from the telescope's internal clock 
            (hours, float).

        """
        return self._get("siderealtime")

    @property
    def SiteElevation(self) -> float:
        """Set or return the observing site's elevation above mean sea level.

        Args:
            SiteElevation (float): Elevation above mean sea level (metres).
        
        Returns:
            Elevation above mean sea level (metres) of the site at which the telescope
            is located if not set.

        """
        return self._get("siteelevation")
    @SiteElevation.setter
    def SiteElevation(self, SiteElevation: float):
        self._put("siteelevation", SiteElevation=SiteElevation)

    @property
    def SiteLatitude(self) -> float:
        """Set or return the observing site's latitude.

        Args:
            SiteLatitude (float): Site latitude (degrees).
        
        Returns:
            Geodetic(map) latitude (degrees, positive North, WGS84) of the site at which
            the telescope is located if not set.
        
        """
        return self._get("sitelatitude")
    @SiteLatitude.setter
    def SiteLatitude(self, SiteLatitude: float):
        self._put("sitelatitude", SiteLatitude=SiteLatitude)

    @property
    def SiteLongitude(self) -> float:
        """Set or return the observing site's longitude.

        Args:
            SiteLongitude (float): Site longitude (degrees, positive East, WGS84)
        
        Returns:
            Longitude (degrees, positive East, WGS84) of the site at which the telescope
            is located.
        
        """
        return self._get("sitelongitude")
    @SiteLongitude.setter
    def SiteLongitude(self, SiteLongitude: float):
        self._put("sitelongitude", SiteLongitude=SiteLongitude)

    @property
    def Slewing(self) -> bool:
        """Indicate whether the telescope is currently slewing.

        Returns:
            True if telescope is currently moving in response to one of the Slew methods
            or the moveaxis(int, float) method, False at all other times.

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
        return self._get("trackingrate")
    @TrackingRate.setter
    def TrackingRate(self, TrackingRate: DriveRates):
        self._put("trackingrate", TrackingRate=TrackingRate)

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

    def CanMoveAxis(self, Axis: int) -> bool:
        """Indicate whether the telescope can move the requested axis.

        Returns:
            True if this telescope can move the requested axis.

        """
        return self._get("canmoveaxis", Axis=Axis)

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
        self._put("findhome")

    def MoveAxis(self, Axis: TelescopeAxes, Rate: float) -> None:
        """Move a telescope axis at the given rate.

        Args:
            Axis (int): The axis about which rate information is desired
            (enum TelescopeAxes): 0 = axisPrimary, 1 = axisSecondary, 
            2 = axisTertiary.
            Rate (float): The rate of motion (deg/sec) about the specified axis

        """
        self._put("moveaxis", Axis=Axis, Rate=Rate)

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
        self._put("pulseguide", Direction=Direction, Duration=Duration)

    def SetPark(self) -> None:
        """Set the telescope's park position to its current position."""
        self._put("setpark")

    def SlewToAltAz(self, Azimuth: float, Altitude: float) -> None:
        """Slew synchronously to the given local horizontal coordinates.

        Args:
            Azimuth (float): Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude (float): Altitude coordinate (degrees, positive up).

        """
        self._put("slewtoaltaz", Azimuth=Azimuth, Altitude=Altitude)

    def SlewToAltAzAsync(self, Azimuth: float, Altitude: float) -> None:
        """Slew asynchronously to the given local horizontal coordinates.

        Args:
            Azimuth (float): Azimuth coordinate (degrees, North-referenced, positive
                East/clockwise).
            Altitude (float): Altitude coordinate (degrees, positive up).

        """
        self._put("slewtoaltazasync", Azimuth=Azimuth, Altitude=Altitude)

    def SlewToCoordinates(self, RightAscension: float, Declination: float) -> None:
        """Slew synchronously to the given equatorial coordinates.

        Args:
            RightAscension (float): Right Ascension coordinate (hours).
            Declination (float): Declination coordinate (degrees).

        """
        self._put(
            "slewtocoordinates", RightAscension=RightAscension, Declination=Declination
        )

    def SlewToCoordinatesAsync(self, RightAscension: float, Declination: float):
        """Slew asynchronously to the given equatorial coordinates.

        Args:
            RightAscension (float): Right Ascension coordinate (hours).
            Declination (float): Declination coordinate (degrees).
        
        """
        self._put("slewtocoordinatesasync", RightAscension=RightAscension, Declination=Declination)

    def SlewToTarget(self) -> None:
        """Slew synchronously to the TargetRightAscension and TargetDeclination coordinates."""
        self._put("slewtotarget")

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

    def UnPark(self) -> None:
        """Unpark the mount."""
        self._put("unpark")
