class ActionNotImplementedException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class AlpacaRequestException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class DriverException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class InvalidOperationException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class InvalidValueException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class NotConnectedException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class NotImplementedException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(number, message)

class ParkedException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class SlavedException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

class UnknownAscomException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(f'Unknown code {number}: {message}')

class ValueNotSetException(Exception):
    def __init__(
        self,
        number: int,
        message: str
    ):
        super().__init__(message)

