from alpaca.device import Device

class Switch(Device):
    """ASCOM Standard ISwitch V2 Interface"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize the Switch object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "switch", device_number, protocol)

    @property
    def MaxSwitch(self) -> int:
        """Count of switch devices managed by this driver.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Number of switch devices managed by this driver. Devices are numbered from 0
              to MaxSwitch - 1.
        
        """
        return self._get("maxswitch")

    def CanWrite(self, Id: int) -> bool:
        """The specified switch device can be written to.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Switch devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * Examples of witches that cannot be written to include a
              limit switch or a sensor.
        
        """
        return self._get("canwrite", ID=Id)

    def GetSwitch(self, Id: int) -> bool:
        """The state of the specified switch device.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        return self._get("getswitch", ID=Id)

    def GetSwitchDescription(self, Id: int) -> str:
        """The textual description of the specified switch device.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("getswitchdescription", ID=Id)

    def GetSwitchName(self, Id: int) -> str:
        """The textual name of the specified switch device.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("getswitchname", ID=Id)
    
    def GetSwitchValue(self, Id: int) -> float:
        """The value of the specified switch device as a float.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("getswitchvalue", ID=Id)

    def MaxSwitchValue(self, Id: int) -> float:
        """The maximum value of the specified switch device as a double.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("maxswitchvalue", ID=Id)

    def MinSwitchValue(self, Id: int) -> float:
        """The minimum value of the specified switch device as a double.

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
        
        """
        return self._get("minswitchvalue", ID=Id)

    def SetSwitch(self, Id: int, State: bool) -> None:
        """Set a switch device to the specified state

        Args:
            Id: the specified switch number (see Notes)
            State: The required control state

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        self._put("setswitch", ID=Id, State=State)

    def SetSwitchName(self, Id: int, Name: str) -> None:
        """Set a switch device name to the specified value.

        Args:
            Id: the specified switch number (see Notes)
            Name: The desired (new) name for the switch

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        self._put("setswitchname", ID=Id, Name=Name)

    def SetSwitchValue(self, Id: int, Value: float) -> None:
        """Set a switch device value to the specified value.

        Args:
            Id: the specified switch number (see Notes)
            Value: Value to be set, between :py:attr:`MinSwitchValue` and 
                :py:attr:`MinSwitchValue`.

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`), or
                the Value is out of range, not between :py:attr:`MinSwitchValue` and 
                :py:attr:`MinSwitchValue`.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.
            * On is True, Off is False.

        """
        self._put("setswitchvalue", ID=Id, Value=Value)

    def SwitchStep(self, Id: int) -> float:
        """The step size of the specified switch device (see Notes).

        Args:
            Id: the specified switch number (see Notes)

        Raises:
            InvalidValueException: The Id is out of range (see :py:attr:`MaxSwitch`)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Step size is the difference between successive values of the device.
            * Devices are numbered from 0 to :py:attr:`MaxSwitch` - 1.

        """
        return self._get("switchstep", ID=Id)
