from alpaca.device import Device

class Switch(Device):
    """ASCOM Standard ISwitch V2 Interface"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize Switch object."""
        super().__init__(address, "switch", device_number, protocol)

    @property
    def MaxSwitch(self) -> int:
        """Count of switch devices managed by this driver.

        Returns:
            Number of switch devices managed by this driver. Devices are numbered from 0
            to MaxSwitch - 1.
        
        """
        return self._get("maxswitch")

    @property
    def CanWrite(self, Id: int) -> bool:
        """Indicate whether the specified switch device can be written to.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.

        Returns:
            Whether the specified switch device can be written to, default true. This is
            false if the device cannot be written to, for example a limit switch or a
            sensor.
        
        """
        return self._get("canwrite", ID=Id)

    def GetSwitch(self, Id: int) -> bool:
        """Return the state of switch device id as a boolean.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (protocol): The device number.
        
        Returns:
            On/Off State (bool) of specified switch device.
        
        """
        return self._get("getswitch", ID=Id)

    def GetSwitchDescription(self, Id: int) -> str:
        """Get the description of the specified switch device.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
        
        Returns:
            Description of specified switch device.
        
        """
        return self._get("getswitchdescription", ID=Id)

    def GetSwitchName(self, Id: int) -> str:
        """Get the name of the specified switch device.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
        
        Returns:
            Name of the specified switch device.
        
        """
        return self._get("getswitchname", ID=Id)
    
    def GetSwitchValue(self, Id: int) -> str:
        """Get the value of the specified switch device as a double.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
        
        Returns:
            Value of the specified switch device.
        
        """
        return self._get("getswitchvalue", ID=Id)

    def MinSwitchValue(self, Id: int) -> str:
        """Get the minimum value of the specified switch device as a double.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
        
        Returns:
            Minimum value of the specified switch device as a double.
        
        """
        return self._get("minswitchvalue", ID=Id)

    def SetSwitch(self, Id: int, State: bool) -> None:
        """Set a switch controller device to the specified state, True or False.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
            State (bool): The required control state (True or False).

        """
        self._put("setswitch", ID=Id, State=State)

    def SetSwitchName(self, Id: int, Name: str) -> None:
        """Set a switch device name to the specified value.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
            Name (str): The name of the device.

        """
        self._put("setswitchname", ID=Id, Name=Name)

    def SetSwitchValue(self, Id: int, Value: float) -> None:
        """Set a switch device value to the specified value.

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
            Value (float): Value to be set, between MinSwitchValue and MaxSwitchValue.

        """
        self._put("setswitchvalue", ID=Id, Value=Value)

    def SwitchStep(self, Id: int) -> str:
        """Return the step size that this device supports.

        Return the step size that this device supports (the difference between
        successive values of the device).

        Notes:
            Devices are numbered from 0 to MaxSwitch - 1.

        Args:
            Id (int): The device number.
        
        Returns:
            Maximum value of the specified switch device as a double.
        
        """
        return self._get("switchstep", ID=Id)
