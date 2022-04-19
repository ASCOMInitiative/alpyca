from alpaca.device import Device

class Rotator(Device):
    """ASCOM Standard IRotatorV3 interface."""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize the Rotator object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".
        
        Raises:
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        super().__init__(address, "rotator", device_number, protocol)

    @property
    def CanReverse(self) -> bool:
        """The rotator supports the Reverse method

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        """
        return self._get("canreverse")

    @property
    def IsMoving(self) -> bool:
        """The rotator is currently moving to a new position
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * This is the correct property to use to determine *successful* completion of 
              a (non-blocking) :py:meth:`Move()` request. IsMoving will be True 
              immediately upon returning from a :py:meth:`Move()` call, and will 
              remain True until *successful* completion, at which time IsMoving will 
              become False.
        
        """
        return self._get("ismoving")

    @property
    def MechanicalPosition(self) -> bool:
        """The raw mechanical position (deg) of the rotator
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            Value is in degrees counterclockwise from the rotator's mechanical index.
        
        """
        return self._get("mechanicalposition")

    @property
    def Position(self) -> bool:
        """This returns the position (deg) of the rotator allowing for sync offset  

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Position is in degrees counterclockwise
            * The :py:meth:`Sync()` method may used to make Position indicate 
              equatorial position angle. This can account for not only an offset
              in the rotator's mechanical position, but also the angle at which 
              an attached imager is mounted.
            * If :py:meth:`Sync()` has never been called, Position will be 
              equal to :py:attr:`MechanicalPosition`. Once called, however, 
              the offset will remain across driver starts and device reboots.
            
        """
        return self._get("position")

    @property
    def Reverse(self) -> bool:
        """(Read/Write) Set or indicate rotation direction reversal.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            Rotation is normally in degrees counterclockwise as viewed
            from behind the rotator, looking toward the sky. This corresponds
            to the direction of equatorial position angle. Set this property True 
            to cause rotation opposite to equatorial PositionAngle, i.e. clockwise.
            
        """
        return self._get("reverse")
    @Reverse.setter
    def Reverse(self, ReverseState: bool):
        self._put("reverse", Reverse=ReverseState)

    @property
    def StepSize(self) -> float:
        """The minimum rotation step size (deg)
        
        Raises:
            NotImplementedException: If this property is not available from the device
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("stepsize")

    @property
    def TargetPosition(self) -> float:
        """The destination angle for :py:meth:`Move()` and MoveAbsolute(). 
        
        Notes:
            This will contain the new Position, including any :py:meth:`Sync()` 
            offset, immediately upon return from a call to :py:meth:`Move()` or 
            :py:meth:`MoveAbsolute()`.
            
        """
        return self._get("targetposition")

    def Halt(self) -> None:
        """Immediately stop any rotator motion due to a previous movement call.
        
        Raises:
            NotImplementedException: The rotator cannot be programmatically halted.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * You should try to call this method aftr initialization to see if halting is
              supported by your device. You can use this info to possibly disable a Halt
              button in your user interface.

        """
        self._put("halt")

    def Move(self, Position: float) -> None:
        """Starts rotation relative to the current position (degrees)

        **Non-blocking**: Returns immediately with :py:attr:`IsMoving` = True if 
        the operation has *successfully* been started, or if it returns with 
        :py:attr:`IsMoving` = False, it will already be at the requested position,
        also a success. See Notes, and :ref:`async_faq`
        
        **Also See Notes for details on absolute versus relative movement**.

        Arguments:
            Position: The angular amount (degrees) to move relative to the
                current position.
            
        Raises:
            InvalidValueException: TODO [REVIEW] The given position change results in a position
                outside 0 <= position < 360. [or does it just apply modulo 360 for negative
                or positive offsets? Then what is an "invalid" value?]
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Calling Move causes the TargetPosition property to change to the sum of the 
              current angular position and the value of the Position parameter (modulo 
              360 degrees), then starts rotation to TargetPosition. Position includes the
              effect of any previous Sync() operation.
            * **Asynchronous**: The method returns as soon as the rotation operation has
              been successfully started, with the :py:attr:`IsMoving' property True. 
              After the requested angle is successfully reached and motion stops, 
              the :py:attr:`IsMoving` property becomes False.  See :ref:`async_faq`
        
        """
        self._put("move", Position=Position)

    def MoveAbsolute(self, Position: float) -> None:
        """Starts rotation to the new position (degrees)

        **Non-blocking**: Returns immediately with :py:attr:`IsMoving` = True if 
        the operation has *successfully* been started, or if it returns with 
        :py:attr:`IsMoving` = False, it will already be at the requested position,
        also a success. See Notes, and :ref:`async_faq`
        
        Arguments:
            Position: The requested angle, degrees.
            
        Raises:
            InvalidValueException: TODO [REVIEW] The given position is
                0 <= position < 360. [or does it just apply modulo 360? 
                Then what is an "invalid" value?]
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Calling Move causes the TargetPosition property to change to  the
              value of the Position parameter (modulo 
              360 degrees [TODO REVIEW]), then starts rotation to TargetPosition. 
              Position includes the effect of any previous Sync() operation.
            * **Asynchronous**: The method returns as soon as the rotation operation has
              been successfully started, with the :py:attr:`IsMoving' property True. 
              After the requested angle is successfully reached and motion stops, 
              the :py:attr:`IsMoving` property becomes False.  See :ref:`async_faq`
        
        """
        self._put("moveabsolute", Position=Position)

    def MoveMechanical(self, Position: float) -> None:
        """Starts rotation to the given mechanical position (degrees)

        **Non-blocking**: Returns immediately with :py:attr:`IsMoving` = True if 
        the operation has *successfully* been started, or if it returns with 
        :py:attr:`IsMoving` = False, it will already be at the requested position,
        also a success. See Notes, and :ref:`async_faq`

        Arguments:
            Position: The requested angle, degrees.

        Raises:
            InvalidValueException: TODO [REVIEW] The given position is
                0 <= position < 360. [or does it just apply modulo 360? 
                Then what is an "invalid" value?]
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Calling MoveMechanical causes the TargetPosition property to change to 
              the value of the Position parameter then starts rotation to TargetPosition. 
              This moves without regard to the SyncOffset, that is, to the 
              mechanical rotator angle.
            * This method is to address requirements that need a physical rotation 
              angle such as taking sky flats.
            * **Asynchronous**: The method returns as soon as the rotation operation has
              been successfully started, with the :py:attr:`IsMoving' property True. 
              After the requested angle is successfully reached and motion stops, 
              the :py:attr:`IsMoving` property becomes False. See :ref:`async_faq`
        
        """
        self._put("movemechanical", Position=Position)

    def Sync(self, Position: float) -> None:
        """Syncs the rotator to the specified position angle (degrees) without moving it. 

        Arguments:
            Position: The requested angle, degrees.

        Raises:
            InvalidValueException: TODO [REVIEW] The given position is
                0 <= position < 360. [or does it just apply modulo 360? 
                Then what is an "invalid" value?]
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Once this method has been called and the sync offset determined, both 
              the :py:meth:`MoveAbsolute()' method and the :py:attr:`Position`
              property will function in synced coordinates rather than mechanical 
              coordinates. The sync offset will persist across driver starts and 
              device reboots. 

        """
        self._put("sync", Position=Position)