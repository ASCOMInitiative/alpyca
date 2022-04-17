from alpaca.device import Device
from typing import List, Any

class FilterWheel(Device):
    """ASCOM Standard IFilterWheelV2 interface."""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize FilterWheel object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".
        
        """
        super().__init__(address, "filterwheel", device_number, protocol)

    @property
    def FocusOffsets(self) -> List[int]:
        """List of filter focus offsets for each filter in the wheel
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes: 
            * The offset values in this list are in the same order as the filters in the wheel
            * The number of available filters can be determined from the length of the list. 
            * If focuser offsets are not available, then the list will contain zeroes. 

        """
        return self._get("focusoffsets")

    @property
    def Names(self) -> List[str]:
        """List of filter names for each filter in the wheel
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes: 
            * The names in this lisat are in the same order as the filters in the wheel
            * The number of available filters can be determined from the length of the list. 
            * If focuser offsets are not available, then the lost will contain generic names
              of 'Filter 1', 'Filter 2', etc.

        """
        return self._get("names")

    @property
    def Position(self) -> int:
        """(Read/Write) Start a change to, or return the filter wheel position (zero-based)

        **Non-blocking**: Returns immediately upon writing to change the filter 
        with Position = -1 if the operation has been *successfully* started.

        Raises:
            InvalidValueException: If an invalid filter number is written to Position.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            **Asynchronous** (non-blocking): Writing to Position returns as soon as the 
            filter change operation has been *successfully* started. Position
            will return -1 while the change is in progress. After the requested position 
            has been *successfully* reached and motion stops, Position will
            return the requested new filter number. 

        """
        return self._get("position")
    @Position.setter
    def Position(self, Position: int):
        self._put("position", Position=Position)

