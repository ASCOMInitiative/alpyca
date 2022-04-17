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
        
        Raises:
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        super().__init__(address, "covercalibrator", device_number, protocol)

    @property
    def Brightness(self) -> int:
        """The current calibrator brightness (0 - :py:attr:`MaxBrightness`)
        
        Raises:
            NotImplementedException: When :py:attr:`CalibratorState` is
                :py:class:`~CalibratorStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * This is a mandatory property if a calibrator device is present
              (:py:attr:`CalibratorState` is other than 
              :py:class:`~CalibratorStatus.NotPresent`), and must always 
              return a value within the integer range 1 to 2,147,483,647. TODO I added 
              wording here. Also need we explicitly mention 2,147,483,647???
            * Examples: A value of 1 indicates that the calibrator can only be 
              "off" or "on". A value of 10 indicates that the calibrator has 
              10 discrete illumination levels in addition to "off".

        """
        return self._get("maxbrightness")

    def CalibratorOff(self) -> None:
        """Turns the calibrator off if the device has calibration capability 
        
        Raises:
            NotImplementedException: When :py:attr:`CalibratorState` is
                :py:class:`~CalibratorStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * **Asynchronous** (non-blocking): If the calibrator requires time to safely stabilise 
              after use, :py:class:`CalibratorState` will return :py:class:`~CalibratorStatus.NotReady`. 
              When the calibrator is safely off, :py:class:`CalibratorState` will return 
              :py:class:`~CalibratorStatus.Off`.
            * During the shutdown process, reading :py:class:`CalibratorStatus` may result in a 
              :py:exc:`~alpaca.exceptions.DriverException`.

        """
        self._put("calibratoroff")

    def CalibratorOn(self, BrightnessVal: int) -> None:
        """Turns the calibrator on if the device has calibration capability
        
        Parameters:
            Brightness: The calibrator illumination brightness to be set

        Raises:
            NotImplementedException: When :py:attr:`CalibratorState` is
                :py:class:`~CalibratorStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * **Asynchronous** (non-blocking): If the calibrator requires time to safely 
              stabilise, :py:class:`CalibratorState` will return
              :py:class:`~CalibratorStatus.NotReady`. 
              When the calibrator is ready for use, :py:class:`CalibratorState` will return 
              :py:class:`~CalibratorStatus.Ready`.
            * If an error condition arises while turning on the calibrator, 
              :py:class:`CalibratorState` will be set to :py:class:`~CalibratorStatus.Error`
              rather than :py:class:`~CalibratorStatus.Unknown`.
            * During the shutdown process, reading :py:class:`CalibratorStatus` may result in a 
              :py:exc:`~alpaca.exceptions.DriverException`.
        
        Attention:
            For devices with both cover and calibrator capabilities, this method may 
            change the :py:class:`CoverState`, if required. This operation is also 
            **asynchronous** (non-blocking) so you may need to wait for :py:class:`CoverState`
            to reach :py:class:`~CoverStatus.Open` 

        """
        self._put("calibratoron", Brightness=BrightnessVal)

    def CloseCover(self) -> None:
        """Initiates cover closing if a cover is present 
        
        Raises:
            NotImplementedException: When :py:attr:`CoverState` is
                :py:class:`~CoverStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * **Asynchronous** (non-blocking): :py:attr:`CoverState` indicates the 
              status of the operation once CloseCover() returns. It will be 
              :py:class:`~CoverStatus.Moving` immediately after the return of 
              CloseCover(), and will remain as long as the operation is progressing 
              successfully.
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
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

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
        
        Raises:
            NotImplementedException: When :py:attr:`CoverState` is
                :py:class:`~CoverStatus.NotPresent`
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * **Asynchronous** (non-blocking): :py:attr:`CoverState` indicates the 
              status of the operation once OpenCover() returns. It will be 
              :py:class:`~CoverStatus.Moving` immediately after the return of 
              OpenCover(), and will remain as long as the operation is progressing 
              successfully.
            * :py:class:`~CoverStatus.Open` indicates *successful* completion. 
            * If an error condition arises while moving between states, 
              :py:attr:`CoverState` will be set to :py:class:`~CoverStatus.Error`
              rather than :py:class:`~CoverStatus.Unknown`
            
            
        """
        self._put("OpenCover")

