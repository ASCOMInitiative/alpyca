# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# exceptions - Implements ASCOM Alpaca Exception classes
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.9 or later
# Doc Environment: Sphinx v5.0.2 with autodoc, autosummary, napoleon, and autoenum
# GitHub: https://github.com/ASCOMInitiative/alpyca
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022-2024 Ethan Chappel and Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# Edit History:
# 02-May-22 (rbd) Initial Edit
# 13-May-22 (rbd) 2.0.0-dev1 Project now called "Alpyca" - no logic changes
# 05-Mar-24 (rbd) 3.0.0 For Platform 7 add OperationCancelledException.
# 24-Feb-25 (rbd) 3.1.0 Fix DriverException and AlpacaRequestException for
#                       specified error number. Add number as exception
#                       attribute, Make message and number as named exception
#                       properties. Add str(exception) support. Enhance
#                       documentation.
# 26-May-25 (rbd) 3.1.1 Add missing note to DriverException
# -----------------------------------------------------------------------------

class ActionNotImplementedException(Exception):
    """Exception thrown by a device when it receives an unknown command through
    the Action method.

    Properties:
        - number (int): Constant 0x040C (1036)
        - message (str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x40C
        self.message = message
        super().__init__(0x40C, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class AlpacaRequestException(Exception):
    """Raised by the device's Alpaca server for unknown or illegal requests.

    Properties:
        - number (int): The HTTP response code (4xx or 5xx)
        - message (str): The concatenation of the server's response text and the URL.
    """
    def __init__(
        self,
        number: int,
        message: str
    ):
        self.number = number
        self.message = message
        super().__init__(number, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'


class DriverException(Exception):
    """Generic driver exception. See note below.

    Properties:
        - number (int): Assigned by the device and will be a number from 0x500 - 0xFFF
        - message (str): Text of the error message

    Note:
        This is the generic driver exception. Drivers are permitted to directly
        throw these exceptions. This exception should only be thrown if there is
        no other more appropriate exception as listed here are already defined.
        These specific exceptions should be thrown where appropriate rather
        than using the more generic DriverException. Conform will not accept
        DriverExceptions where more appropriate exceptionsare already defined.

    """
    def __init__(
        self,
        number: int,
        message: str
    ):
        self.number = number
        self.message = message
        super().__init__(number, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class InvalidOperationException(Exception):
    """Thrown by the device to reject a command from the client.

    Properties:
        - number (int): Constant 0x40B (1035)
        - message (str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x40B
        self.message = message
        super().__init__(0x40B, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class InvalidValueException(Exception):
    """Exception to report an invalid value supplied to a device.

    Properties:
        - number (int): Constant 0x401 (1025)
        - message(str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x401
        self.message = message
        super().__init__(0x401, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class NotConnectedException(Exception):
    """An operation is attempted that requires communication with the device, but the device
    is disconnected.

    Properties:
        - number (int): Constant 0x407 (1031)
        - message(str): Text of the error message

    This refers to the driver not being connected to the
    device. It is not for network outages or bad URLs.
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x407
        self.message = message
        super().__init__(0x407, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class NotImplementedException(Exception):
    """Property or method is not implemented in the device

    Properties:
        - number (int): Constant 0x400 (1024)
        - message(str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x400
        self.message = message
        super().__init__(0x400, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class OperationCancelledException(Exception):
    """An (asynchronous) in-progress operation has been cancelled.

    Properties:
        - number (int): Constant 0x40E (1038)
        - message(str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x40E
        self.message = message
        super().__init__(0x40E, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class ParkedException(Exception):
    """Movement (or other invalid operation) was attempted while the
    device was in a parked state.

    Properties:
        - number (int): Constant 0x408 (1032)
        - message(str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x408
        self.message = message
        super().__init__(0x408, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

class SlavedException(Exception):
    """Movement (or other invalid operation) was attempted while the
    device was in slaved mode. This applies primarily to Dome drivers.

    Properties:
        - number (int): Constant 0x409 (1033)
        - message(str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x409
        self.message = message
        super().__init__(0x409, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

# Replaced with DriverException per agreement 30-Apr-2022
# class UnknownAscomException(Exception):
#     """ Unknown Error Code in Alpaca response

#     Raised by the  library if the driver returns an error code that is
#     not part of the Alpaca 2022 specification, that is, a code from 0x400
#     through 0x4FF that is not listed here for one of the other defined
#     exceptions. The message will contain the number followed by the
#     message from the driver.

#     """
#     def __init__(
#         self,
#         number: int,
#         message: str
#     ):
#         super().__init__(f'Unknown code {number}: {message}')

class ValueNotSetException(Exception):
    """No value has yet been set for this property.

    Properties:
        - number (int): Constant 0x402 (1026)
        - message(str): Text of the error message
    """
    def __init__(
        self,
        message: str
    ):
        self.number = 0x402
        self.message = message
        super().__init__(0x402, message)

    def __str__(self):
        return f'{self.message} (Error Code: 0x{self.number:x})'

