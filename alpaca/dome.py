from enum import IntEnum
from alpaca.device import Device
from typing import List, Any

class ShutterState(IntEnum):
    shutterOpen = 0
    shutterClosed = 1
    shutterOpening = 2
    shutterClosing = 3
    shutterError = 4

class Dome(Device):
    """ASCOM Standard IDomeV2 Interface"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize Dome object."""
        super().__init__(address, "dome", device_number, protocol)

    @property
    def Altitude(self) -> float:
        """Dome altitude.

        Returns:
            Dome altitude (degrees, horizon zero and increasing positive to 90 zenith).
        
        """
        return self._get("altitude")

    @property
    def AtHome(self) -> bool:
        """Indicate whether the dome is in the home position.

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
        """Indicate whether the telescope is at the park position.

        Notes:
            Set only following a park() operation and reset with any slew operation.

        Returns:
            True if the dome is in the programmed park position.

        """
        return self._get("atpark")

    @property
    def Azimuth(self) -> float:
        """Dome azimuth.

        Returns:
            Dome azimuth (degrees, North zero and increasing clockwise, i.e., 90 East,
            180 South, 270 West).

        """
        return self._get("azimuth")

    @property
    def CanFindHome(self) -> bool:
        """Indicate whether the dome can find the home position.

        Returns:
            True if the dome can move to the home position.
        
        """
        return self._get("canfindhome")

    @property
    def CanPark(self) -> bool:
        """Indicate whether the dome can be parked.

        Returns:
            True if the dome is capable of programmed parking (park() method).
        
        """
        return self._get("canpark")

    @property
    def CanSetAltitude(self) -> bool:
        """Indicate whether the dome altitude can be set.

        Returns:
            True if driver is capable of setting the dome altitude.
        
        """
        return self._get("cansetaltitude")

    @property
    def CanSetAzimuth(self) -> bool:
        """Indicate whether the dome azimuth can be set.

        Returns:
            True if driver is capable of setting the dome azimuth.
        
        """
        return self._get("cansetazimuth")

    @property
    def CanSetPark(self) -> bool:
        """Indicate whether the dome park position can be set.

        Returns:
            True if driver is capable of setting the dome park position.
        
        """
        return self._get("cansetpark")

    @property
    def CanSetShutter(self) -> bool:
        """Indicate whether the dome shutter can be opened.

        Returns:
            True if driver is capable of automatically operating shutter.

        """
        return self._get("cansetshutter")

    @property
    def CanSlave(self) -> bool:
        """Indicate whether the dome supports slaving to a telescope.

        Returns:
            True if driver is capable of slaving to a telescope.
        
        """
        return self._get("canslave")

    @property
    def CanSyncAzimuth(self) -> bool:
        """Indicate whether the dome azimuth position can be synched.

        Notes:
            True if driver is capable of synchronizing the dome azimuth position using
            the synctoazimuth(float) method.
        
        Returns:
            True or False value.
        
        """
        return self._get("cansyncazimuth")

    @property
    def ShutterStatus(self) -> ShutterState:
        """Status (enum ShutterState) of the dome shutter or roll-off roof.

        Notes:
            ShutterState is 0 = Open, 1 = Closed, 2 = Opening, 
            3 = Closing, 4 = Shutter status error.
        
        Returns:
            Status (enum ShutterState) of the dome shutter or roll-off roof.

        """
        return ShutterState(self._get("shutterstatus"))

    @property
    def Slaved(self) -> bool:
        """Set or indicate whether the dome is slaved to the telescope.
        
        Returns:
            True if the dome is slaved to the telescope in its hardware, 
            else False.
        
        """
        return self._get("slaved")
    @Slaved.setter
    def Slaved(self, SlavedState: bool):
        self._put("slaved", Slaved=SlavedState)

    @property
    def Slewing(self) -> bool:
        """Indicate whether the any part of the dome is moving.

        Returns:
            True if any part of the dome is currently moving, False if all dome
            components are stationary.
        
        """
        return self._get("slewing")

    def AbortSlew(self) -> None:
        """Immediately stops any and all movement.

        Notes:
            Calling this method will immediately disable hardware slewing (Slaved
            will become False).

        """
        self._put("abortslew")

    def CloseShutter(self) -> None:
        """Close the shutter or otherwise shield telescope from the sky."""
        self._put("closeshutter")

    def FindHome(self):
        """Start operation to search for the dome home position.

        Notes:
            Asynchronous: The method returns as soon as the homing operation has 
            been successfully started. After the home position is established, 
            Azimuth is synchronized to the appropriate value and the AtHome 
            property becomes True.
        
        """
        self._put("findhome")

    def OpenShutter(self) -> None:
        """Open shutter or otherwise expose telescope to the sky."""
        self._put("openshutter")

    def Park(self) -> None:
        """Start slewing the dome to its park position.

        Notes:
            Asynchronous: The method returns as soon as the parking operation has 
            been successfully started, with the Slewing property True. After the 
            park position is established and motion stops, Azimuth and (if 
            supported by the dome) Altitude are synchronized to the appropriate 
            value(s), the AtPark property becomes True, and the Slewing property 
            becomes False.
        
        """
        self._put("park")

    def SetPark(self) -> None:
        """Set current position of dome to be the park position."""
        self._put("setpark")

    def SlewToAltitude(self, Altitude: float) -> None:
        """Start slewing the dome to the given altitude position.
        
        Args:
            Azimuth (float): Target dome azimuth (degrees, North zero and increasing
                clockwise. i.e., 90 East, 180 South, 270 West).
        Notes:
            Asynchronous: The method returns as soon as the slewing operation has 
            been successfully started, with the Slewing property True. After the
            destination altitude is successfully reached and motion stops, the 
            Slewing property becomes False.
        
        
        """
        self._put("slewtoaltitude", Altitude=Altitude)

    def SlewToAzimuth(self, Azimuth: float) -> None:
        """Slew the dome to the given azimuth position.
        
        Args:
            Azimuth (float): Target dome azimuth (degrees, North zero and increasing
                clockwise. i.e., 90 East, 180 South, 270 West).

        Notes:
            Asynchronous: The method returns as soon as the slewing operation has 
            been successfully started, with the Slewing property True. After the
            destination azimuth is successfully reached and motion stops, the 
            Slewing property becomes False.

        """
        self._put("slewtoazimuth", Azimuth=Azimuth)

    def SyncToAzimuth(self, Azimuth: float) -> None:
        """Synchronize the current azimuth of the dome to the given azimuth.

        Args:
            Azimuth (float): Target dome azimuth (degrees, North zero and increasing
                clockwise. i.e., 90 East, 180 South, 270 West).
        
        """
        self._put("synctoazimuth", Azimuth=Azimuth)

