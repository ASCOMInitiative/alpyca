from enum import IntEnum
from alpaca.device import Device

class CalibratorStatus(IntEnum):
    NotPresent = 0
    Off = 1
    NotReady = 2
    Ready = 3
    Unknown = 4
    Error = 5

class CoverStatus(IntEnum):
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
        """Initialize Camera object."""
        super().__init__(address, "covercalibrator", device_number, protocol)

    @property
    def Brightness(self) -> int:
        """The current calibrator brightness (0 - MaxBrightness)"""
        return self._get("brightness")

    @property
    def CalibratorState(self) -> CalibratorStatus:
        """The state of the calibration device (enum CalibratorStatus)"""
        return CalibratorStatus(self._get("calibratorstate"))

    @property
    def CoverState(self) -> CoverStatus:
        """The state of the device cover (enum CoverStatus)"""
        return CoverStatus(self._get("coverstate"))

    @property
    def MaxBrightness(self) -> int:
        """The state of the device cover (enum CoverStatus)"""
        return self._get("maxbrightness")

    def CalibratorOff(self) -> None:
        """Turns the calibrator off if the device has calibration capability 
        
        Notes:
            Asynchronous: If the calibrator requires time to safely stabilise 
            after use, CalibratorState will return NotReady. When the calibrator
            is safely off, CalibratorState will return Off.

        """
        self._put("calibratoroff")

    def CalibratorOn(self, BrightnessVal: int) -> None:
        """Turns the calibrator on if the device has calibration capability
        
        Parameters:
            Brightness: The calibrator illumination brightness to be set
            
        """
        self._put("calibratoron", Brightness=BrightnessVal)

    def CloseCover(self) -> None:
        """Initiates cover closing if a cover is present 
        
        Notes:
            Asynchronous: CoverState indicates the status of the operation once
            CloseCover() returns. CoverState = Closed indicates success. If an 
            error condition arises while moving between states, CoverState 
            must be set to Error rather than Unknown.
            
        """
        self._put("closecover")

    def HaltCover(self) -> None:
        """Immediately stops an in-progress OpenCover() or CloseCover
        
        Notes:
            This will  stop any cover movement as soon as possible and 
            set a CoverState of Open, Closed or Unknown as appropriate.
            If cover movement cannot be interrupted, a 
            MethodNotImplementedException will be thrown.

            
        """
        self._put("haltcover")

    def OpenCover(self) -> None:
        """Initiates cover opening if a cover is present 
        
        Notes:
            Asynchronous: CoverState indictes the status of the operation once
            OpenCover() returns. CoverState = Open indicates success. If an error 
            condition arises while moving between states, CoverState must be set 
            to Error rather than Unknown
            
        """
        self._put("OpenCover")

