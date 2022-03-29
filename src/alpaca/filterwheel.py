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
        """Initialize FilterWheel object."""
        super().__init__(address, "filterwheel", device_number, protocol)

    @property
    def FocusOffsets(self) -> List[int]:
        """Filter focus offsets.

        Returns:
            An integer array of filter focus offsets.
        
        """
        return self._get("focusoffsets")

    @property
    def Names(self) -> List[str]:
        """Filter wheel filter names.

        Returns:
            Names of the filters.

        """
        return self._get("names")

    @property
    def Position(self) -> int:
        """Start a change to, or return the filter wheel position (int, 0-based).

        Args:
            Position (int): Number of the filter wheel position to select, from 
            0 to N-1 

        Returns:
            Returns the current filter wheel position or -1 when in motion.
        
        Notes:
            Asynchronous: Changing position returns as soon as the filter change 
            operation has been successfully started. Position will return -1 while
            the change is in progress. After the requested position is successfully 
            reached and motion stops, Position will return the new filter number. 

        """
        return self._get("position")
    @Position.setter
    def Position(self, Position: int):
        self._put("position", Position=Position)

