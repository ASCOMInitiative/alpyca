from alpaca.device import Device

class SafetyMonitor(Device):
    """ASCOM Standard ISafetyMonitor V1 Interface.
    
    Provides a single property that indicates whether it is safe to expose
    the observatory instruments to the outside environment, or not. The
    measurements of meterological conditions that your application (or a 
    separate weather monitoring system) uses to make this decision will
    most often come from sensors that are accessed through the 
    :py:class:`~alpaca.observingconditions.ObservingConditions` interface.
    
    """

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize the SafetyMonitor object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "safetymonitor", device_number, protocol)

    @property
    def IsSafe(self) -> bool:
        """The monitored state is safe for use.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        """
        return self._get("issafe")
