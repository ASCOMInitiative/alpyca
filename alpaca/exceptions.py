class ActionNotImplementedException(Exception):
    """Numeric value: 0x040C (1036)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x40C
        super().__init__(message)

class AlpacaRequestException(Exception):
    """Raised by the device's Alpaca server for unknown or illegal requests. 
    
    The number is the HTTP response code (4xx or 5xx) and the message
    is a concatenation of the server's response text and the URL.
    
    """
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class DriverException(Exception):
    """Numeric value: 0x500 - 0xFFF
    
    The number is assigned by the driver and will be a number from 0x500 - 0xFFF
    
    """
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class InvalidOperationException(Exception):
    """Numeric value: 0x40B (1035)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x40B
        super().__init__(message)

class InvalidValueException(Exception):
    """Numeric value: 0x401 (1025)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x401
        super().__init__(message)

class NotConnectedException(Exception):
    """Numeric value: 0x407 (1031)

    This refers to the driver not being connected to the
    device. It is not for network outages or bad URLs.

    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x407
        super().__init__(message)

class NotImplementedException(Exception):
    """Numeric value: 0x400 (1024)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x400
        super().__init__(message)

class ParkedException(Exception):
    """Numeric value: 0x408 (1032)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x408
        super().__init__(message)

class SlavedException(Exception):
    """Numeric value: 0x409 (1033)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x409
        super().__init__(message)

class UnknownAscomException(Exception):
    """ Unknown Error Code in Alpaca response
    
    Raised by the  library if the driver returns an error code that is 
    not part of the Alpaca 2022 specification, that is, a code from 0x400
    through 0x4FF that is not listed here for one of the other defined 
    exceptions. The message will contain the number followed by the 
    message from the driver. 

    """
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(f'Unknown code {number}: {message}')

class ValueNotSetException(Exception):
    """Numeric value: 0x402 (1026)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x402
        super().__init__(message)

