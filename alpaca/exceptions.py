# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# exceptions - Implements ASCOM Alpaca Exception classes
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# Doc Environment: Sphinx v5.0.2 with autodoc, autosummary, napoleon, and autoenum
# GitHub: https://github.com/ASCOMInitiative/alpyca
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 Ethan Chappel and Bob Denny
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
# -----------------------------------------------------------------------------

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
    """Numeric value: 0x402 (1026)"""
    def __init__(
        self,
        message: str
    ):
        self.number = 0x402
        super().__init__(message)

