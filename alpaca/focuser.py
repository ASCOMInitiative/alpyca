from alpaca.device import Device
from typing import List, Any

class Focuser(Device):
    """ASCOM Standard IFocuserV3 Interface (obsolete Link not included)"""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize Dome object."""
        super().__init__(address, "focuser", device_number, protocol)

    
    @property
    def Absolute(self) -> bool:
        """Indicate if the focuser does absolute positioning
            
        Returns:
            True if the focuser is capable of absolute position; that is, being 
            commanded to a specific step location. False if relative.

        """
        return self._get("absolute")

    @property
    def IsMoving(self) -> bool:
        """Indicate (True) if the focuser is currently moving to a new position"""
        return self._get("ismoving")

    @property
    def MaxIncrement(self) -> int:
        """Maximum number of steps allowed in one Move() operation. 

        Notes:
            For most focusers this is the same as the MaxStep property. This is
            normally used to limit the Increment display in the host software. 

        """
        return self._get("maxincrement")

    @property
    def MaxStep(self) -> int:
        """Maximum step position permitted. 

        Notes:
            The focuser can step between 0 and MaxStep. If an attempt is made to 
            move the focuser beyond these limits, it will automatically stop at 
            the limit. 

        """
        return self._get("maxstep")

    @property
    def Position(self) -> int:
        """Current focuser position, in steps."""
        return self._get("position")

    @property
    def StepSize(self) -> int:
        """Step size (microns) for the focuser."""
        return self._get("stepsize")

    @property
    def TempComp(self) -> bool:
        """Set or indicate the state of the focuser's temp compensation.

        Notes:
            If the TempCompAvailable property is True, then setting TempComp to 
            True puts the focuser into temperature tracking mode; setting it to 
            False will turn off temperature tracking. If temperature compensation 
            is not available, this property will always return False. REFER TO
            THE INTERFACE DOC FOR BEHAVIOUR DIFFERENCES IN EARLIER VERSIONS.
        
        Returns:
            The state of temperature compensation mode (if available), 
            else always False.
        
        """
        return self._get("tempcomp")
    @TempComp.setter
    def TempComp(self, TempCompState: bool):
        self._put("tempcomp", TempComp=TempCompState)

    @property
    def TempCompAvailable(self) -> bool:
        """Indicate (True) if focuser has temperature compensation available. """
        return self._get("tempcompavailable")

    @property
    def Temperature(self) -> float:
        """Current focuser position, in steps."""
        return self._get("temperature")

    def Halt(self) -> None:
        """Immediately stop any focuser motion due to a previous Move() call."""
        self._put("halt")

    def Move(self, Position: int) -> None:
        """Starts moving the focuser to a new position
        
        Arguments:
            Position: 
                Step distance or absolute position, depending on the value of the 
                Absolute property.
            
        Notes:
            Asynchronous: The method returns as soon as the focus change operation 
            has been successfully started, with the IsMoving property True. After the
            requested position is successfully reached and motion stops, the 
            IsMoving property becomes False.

            See the IFocuserV3 interface doc for details on behavior differences
            between relative and absolute focusers.

        """
        self._put("move", Position=Position)
