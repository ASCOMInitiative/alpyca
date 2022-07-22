# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# docenum - Implements subclass that allows doc strings on IntEnum
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

from enum import IntEnum
class DocIntEnum(IntEnum):
    """Used to provide textual documentation for Enum classes
    
    Example:
        ::

            class CameraStates(DocIntEnum):
                \"\"\"Current condition of the Camera\"\"\"
                cameraIdle      = 0, 'Inactive'
                cameraWaiting   = 1, 'Waiting for ??'
                cameraExposing  = 2, 'Acquiring photons'
                cameraReading   = 3, 'Reading from the sensor'
                cameraDownload  = 4, 'Downloading the image data'
                cameraError     = 5, 'An error condition exists'

    References
        https://stackoverflow.com/questions/50473951/how-can-i-attach-documentation-to-members-of-a-python-enum/50473952#50473952

    """
    def __new__(cls, value, doc=None):
        self = int.__new__(cls, value)  # calling super().__new__(value) here would fail
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self
