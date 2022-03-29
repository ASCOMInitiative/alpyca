from alpaca.device import Device

class Rotator(Device):
    """ASCOM Standard IRotatorV3 interface."""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize FilterWheel object."""
        super().__init__(address, "rotator", device_number, protocol)

    @property
    def CanReverse(self) -> bool:
        """Indicates whether the rotator supports the Reverse method"""
        self._get("canreverse")

    @property
    def IsMoving(self) -> bool:
        """Indicates whether the rotator is currently moving"""
        self._get("ismoving")

    @property
    def MechanicalPosition(self) -> bool:
        """This returns the raw mechanical position (deg) of the rotator
        
        Notes:
            Position is in degrees counterclockwise
        
        """
        self._get("mechanicalposition")

    @property
    def Position(self) -> bool:
        """This returns the position (deg) of the rotator allowing for sync offset        
        Notes:
            Position is in degrees counterclockwise
            The Sync() method may used to make Position indicate equatorial PositionAngle.
            If Sync() has not been called since initialization, Position will be equal to
            MechanicalPosition.
            
        """
        self._get("position")

    @property
    def Reverse(self) -> bool:
        """Set or indicate rotation direction reversal. Reverse is clockwise.
        
        Notes:
            Position is normally in degrees counterclockwise. Set this property True 
            to cause rotation opposite to equatorial PositionAngle, i.e. clockwise.
            
        """
        self._get("reverse")
    @Reverse.setter
    def Reverse(self, ReverseState: bool):
        self._put("reverse", Reverse=ReverseState)

    @property
    def StepSize(self) -> float:
        """The minimum StepSize, in degrees
        
        Notes:
            If this is not available, may throw a NotImplemented exception
            
        """
        self._get("stepsize")

    @property
    def TargetPosition(self) -> float:
        """The destination Position for Move() and MoveAbsolute(). 
        
        Notes:
            This will contain the new Position, including any Sync() offset, upon 
            return from a call to Move() or MoveAbsolute().
            
        """
        self._get("targetposition")

    def Halt(self) -> None:
        """Immediately stop any Rotator motion"""
        self._put("halt")

    def Move(self, Position: float) -> None:
        """Starts rotation relative to the current position (degrees)

        Notes:
            Calling Move causes the TargetPosition property to change to the sum of the 
            current angular position and the value of the Position parameter (modulo 
            360 degrees), then starts rotation to TargetPosition. Position includes the
            effect of any previous Sync() operation.

            Asynchronous: The method returns as soon as the rotation operation has
            been successfully started, with the IsMoving property True. After the
            requested angle is successfully reached and motion stops, the IsMoving 
            property becomes False.
        
        """
        self._put("move", Position=Position)

    def MoveAbsolute(self, Position: float) -> None:
        """Starts rotation to the given position (degrees)

        Notes:
            Calling Move causes the TargetPosition property to change to the value of 
            the Position parameter then starts rotation to TargetPosition. Position 
            includes the effect of any previous Sync() operation.

            Asynchronous: The method returns as soon as the rotation operation has
            been successfully started, with the IsMoving property True. After the
            requested angle is successfully reached and motion stops, the IsMoving 
            property becomes False.
        
        """
        self._put("move", Position=Position)