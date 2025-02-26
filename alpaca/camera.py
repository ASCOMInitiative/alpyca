# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# camera - Implements ASCOM Alpaca Camera device classes and enums
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#           Ethan Chappel <ethan.chappel@gmail.com>
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
# 21-Jul-22 (rbd) 2.0.1 Resolve TODO reviews
# 07-Mar-24 (rbd) 3.0.0 Add Master Interfaces refs to all members
# 08-Nov-24 (rbd) 3.0.1 For PDF rendering no change to logic
# -----------------------------------------------------------------------------

from alpaca.device import Device
from alpaca.telescope import GuideDirections
from alpaca.exceptions import *
from alpaca.docenum import DocIntEnum
from typing import List
import requests
import array

class CameraStates(DocIntEnum):
    """Current condition of the Camera"""
    cameraIdle      = 0, 'Inactive'
    cameraWaiting   = 1, 'Waiting for ??'
    cameraExposing  = 2, 'Acquiring photons'
    cameraReading   = 3, 'Reading from the sensor'
    cameraDownload  = 4, 'Downloading the image data'
    cameraError     = 5, 'An error condition exists'

class SensorType(DocIntEnum):
    """Type of sensor in the Camera. Names should be self-explanatory."""
    Monochrome      = 0
    Color           = 1
    RGGB            = 2
    CMYG            = 3
    CMYG2           = 4
    LRGB            = 5

class ImageArrayElementTypes(DocIntEnum):
    """The native data type of ImageArray pixels"""
    Unknown = 0
    Int16 = 1
    Int32 = 2
    Double = 3
    Single = 4, 'Unused in Alpaca 2022'
    UInt64 = 5, 'Unused in Alpaca 2022'
    Byte = 6, 'Unused in Alpaca 2022'
    Int64 = 7, 'Unused in Alpaca 2022'
    UInt16 = 8, 'Unused in Alpaca 2022'

class ImageMetadata:
    """Metadata describing the returned ImageArray data

        Note:
            * Constructed internally by the library during image retrieval.
            * See https://ascom-standards.org/Developer/AlpacaImageBytes.pdf

    """
    def __init__(
        self,
        metadata_version: int,
        image_element_type: ImageArrayElementTypes,
        transmission_element_type: ImageArrayElementTypes,
        rank: int,
        num_x: int,
        num_y: int,
        num_z: int
    ):
        self.metavers = metadata_version
        self.imgtype = image_element_type
        self.xmtype = transmission_element_type
        self.rank = rank
        self.x_size = num_x
        self.y_size = num_y
        self.z_size = num_z

    @property
    def MetadataVersion(self):
        """The version of metadata, currently 1"""
        return self.metavers

    @property
    def ImageElementType(self) -> ImageArrayElementTypes:
        """The data type of the pixels in originally acquired image

        Note:
            Within Python, the returned nested list(s) image pixels themselves
            will be either int or float.
        """
        return self.imgtype

    @property
    def TransmissionElementType(self) -> ImageArrayElementTypes:
        """The ddta type of the pixels in the transmitted image bytes stream

        Note:
            Within Python, the returned image pixels themselves will be either int or float.

            To save transmission time camera may choose to use a smaller data
            type than the original image if the pixel values would all be
            representative in that data type without a loss of precision.

        """
        return self.xmtype

    @property
    def Rank(self):
        """The matrix rank of the image data (either 2 or 3)"""
        return self.rank

    @property
    def Dimension1(self):
        """The first (X) dimension of the image array"""
        return self.x_size

    @property
    def Dimension2(self):
        """The second (Y) dimension of the image array"""
        return self.y_size

    @property
    def Dimension3(self):
        """The third (Z) dimension of the image array (None or 3)"""
        return self.z_size

class Camera(Device):
    """ASCOM Standard iCamera V4 Interface."""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http",
    ):
        """Initialize the Camera object

        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "camera", device_number, protocol)
        self.img_desc = None

    @property
    def BayerOffsetX(self) -> int:
        """The X offset of the Bayer matrix, as defined in property :attr:`SensorType`

        Raises:

            NotImplementedException: Monochrome cameras throw this exception,
                colour cameras do not.
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.
            InvalidValueException: If not valid.

        Note:
            * The value returned will be in the range 0 to M-1 where M is the width of
              the Bayer matrix. The offset is relative to the 0,0 pixel in the sensor
              array, and does not change to reflect subframe settings.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |BayerOffsetX|

                .. |BayerOffsetX| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.BayerOffsetX" target="_blank">
                    Camera.BayerOffsetX</a> (external)

            .. only:: rinoh

                `Camera.BayerOffsetX <https://ascom-standards.org/newdocs/camera.html#Camera.BayerOffsetX>`_
        """
        return self._get("bayeroffsetx")

    @property
    def BayerOffsetY(self) -> int:
        """The Y offset of the Bayer matrix, as defined in property :attr:`SensorType`

        Raises:

            NotImplementedException: Monochrome cameras throw this exception,
                colour cameras do not.
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.
            InvalidValueException: If not valid.

        Note:
            * The value returned will be in the range 0 to M-1 where M is the width of
              the Bayer matrix. The offset is relative to the 0,0 pixel in the sensor
              array, and does not change to reflect subframe settings.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |BayerOffsetY|

                .. |BayerOffsetY| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.BayerOffsetY" target="_blank">
                    Camera.BayerOffsetY</a> (external)

            .. only:: rinoh

                `Camera.BayerOffsetY <https://ascom-standards.org/newdocs/camera.html#Camera.BayerOffsetY>`_
        """
        return self._get("bayeroffsety")

    @property
    def BinX(self) -> int:
        """**(Read/Write)** Set or return the binning factor for the X axis.

        Raises:
            InvalidValueException: If the given binning value is invalid
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Will default to 1 when the camera connection is established.
            * If :attr:`CanAssymetricBin` is False, then the binning values must be
              the same. Setting this property will result in BinY being the same value.
            * Camera does not check for compatible subframe values when this property
              is set; rather they are checked upon :meth:`StartExposure()`.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |BinX|

                .. |BinX| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.BinX" target="_blank">
                    Camera.BinX</a> (external)

            .. only:: rinoh

                `Camera.BinX <https://ascom-standards.org/newdocs/camera.html#Camera.BinX>`_
        """
        return self._get("binx")
    @BinX.setter
    def BinX(self, BinVal: int):
        self._put("binx", BinX=BinVal)

    @property
    def BinY(self) -> int:
        """**(Read/Write)** Set or return the binning factor for the Y axis.

        Raises:
            InvalidValueException: If the given binning value is invalid
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Will default to 1 when the camera connection is established.
            * If :attr:`CanAssymetricBin` is False, then the binning values must be
              the same. Setting this property will result in BinY being the same value.
            * Camera does not check for compatible subframe values when this property
              is set; rather they are checked upon :meth:`StartExposure()`.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |BinY|

                .. |BinY| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.BinY" target="_blank">
                    Camera.BinY</a> (external)

            .. only:: rinoh

                `Camera.BinY <https://ascom-standards.org/newdocs/camera.html#Camera.BinY>`_
        """
        return self._get("biny")
    @BinY.setter
    def BinY(self, BinVal: int):
        self._put("biny", BinY=BinVal)

    @property
    def CameraState(self) -> CameraStates:
        """The camera's operational state (:py:class:`CameraStates`)

        Raises:
            NotConnectedException: If the camera status is unavailable
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CameraState|

                .. |CameraState| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CameraState" target="_blank">
                    Camera.CameraState</a> (external)

            .. only:: rinoh

                `Camera.CameraState <https://ascom-standards.org/newdocs/camera.html#Camera.CameraState>`_
        """
        return CameraStates(self._get("camerastate"))

    @property
    def CameraXSize(self) -> int:
        """The width of the camera sensor in unbinned pixels

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CameraXSize|

                .. |CameraXSize| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CameraXSize" target="_blank">
                    Camera.CameraXSize</a> (external)

            .. only:: rinoh

                `Camera.CameraXSize <https://ascom-standards.org/newdocs/camera.html#Camera.CameraXSize>`_
        """
        return self._get("cameraxsize")

    @property
    def CameraYSize(self) -> int:
        """The height of the camera sensor in unbinned pixels

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CameraYSize|

                .. |CameraYSize| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CameraYSize" target="_blank">
                    Camera.CameraYSize</a> (external)

            .. only:: rinoh

                `Camera.CameraYSize <https://ascom-standards.org/newdocs/camera.html#Camera.CameraYSize>`_
        """
        return self._get("cameraysize")

    @property
    def CanAbortExposure(self) -> bool:
        """The camera can abort exposures

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Some cameras support :meth:`AbortExposure()`, which allows the exposure to be
              terminated before the exposure timer completes, *with the image being discarded*.
              Returns True if :meth:`AbortExposure()` is available, False if not. See also
              :meth:`StopExposure()`
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanAbortExposure|

                .. |CanAbortExposure| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CanAbortExposure" target="_blank">
                    Camera.CanAbortExposure</a> (external)

            .. only:: rinoh

                `Camera.CanAbortExposure <https://ascom-standards.org/newdocs/camera.html#Camera.CanAbortExposure>`_
        """
        return self._get("canabortexposure")

    @property
    def CanAsymmetricBin(self) -> bool:
        """The camera supports asymmetric binning

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * If true, the camera can have different binning on the X and Y axes, as
              determined by BinX and BinY. If false, the binning must be equal on the X and Y axes.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanAsymmetricBin|

                .. |CanAsymmetricBin| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CanAsymmetricBin" target="_blank">
                    Camera.CanAsymmetricBin</a> (external)

            .. only:: rinoh

                `Camera.CanAsymmetricBin <https://ascom-standards.org/newdocs/camera.html#Camera.CanAsymmetricBin>`_
        """
        return self._get("canasymmetricbin")

    @property
    def CanFastReadout(self) -> bool:
        """The camera supports a fast readout mode

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanFastReadout|

                .. |CanFastReadout| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CanFastReadout" target="_blank">
                    Camera.CanFastReadout</a> (external)

            .. only:: rinoh

                `Camera.CanFastReadout <https://ascom-standards.org/newdocs/camera.html#Camera.CanFastReadout>`_
        """
        return self._get("canfastreadout")

    @property
    def CanGetCoolerPower(self) -> bool:
        """The camera's cooler power level is available via :attr:`CoolerPower`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanGetCoolerPower|

                .. |CanGetCoolerPower| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CanGetCoolerPower" target="_blank">
                    Camera.CanGetCoolerPower</a> (external)

            .. only:: rinoh

                `Camera.CanGetCoolerPower <https://ascom-standards.org/newdocs/camera.html#Camera.CanGetCoolerPower>`_
        """
        return self._get("cangetcoolerpower")

    @property
    def CanPulseGuide(self) -> bool:
        """The camera supports pulse guiding via :meth:`PulseGuide()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanPulseGuide|

                .. |CanPulseGuide| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CanPulseGuide" target="_blank">
                    Camera.CanPulseGuide</a> (external)

            .. only:: rinoh

                `Camera.CanPulseGuide <https://ascom-standards.org/newdocs/camera.html#Camera.CanPulseGuide>`_
        """
        return self._get("canpulseguide")

    @property
    def CanSetCCDTemperature(self) -> bool:
        """The camera cooler temperature can be controlled

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * If True, the camera's cooler setpoint can be adjusted. If False, the
              camera either uses open-loop cooling or does not have the ability to
              adjust temperature from software, and setting the :attr:`SetCCDTemperature`
              property has no effect.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanSetCCDTemperature|

                .. |CanSetCCDTemperature| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CanSetCCDTemperature" target="_blank">
                    Camera.CanSetCCDTemperature</a> (external)

            .. only:: rinoh

                `Camera.CanSetCCDTemperature <https://ascom-standards.org/newdocs/camera.html#Camera.CanSetCCDTemperature>`_
        """
        return self._get("cansetccdtemperature")

    @property
    def CanStopExposure(self) -> bool:
        """The camera can stop exposures

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Some cameras support :meth:`StopExposure()`, which allows the exposure to be
              terminated before the exposure timer completes, *but will still read out the image*.
              Returns True if :meth:`StopExposure()` is available, False if not. See also
              :meth:`AbortExposure()`.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CanStopExposure|

                .. |CanStopExposure| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CanStopExposure" target="_blank">
                    Camera.CanStopExposure</a> (external)

            .. only:: rinoh

                `Camera.CanStopExposure <https://ascom-standards.org/newdocs/camera.html#Camera.CanStopExposure>`_
        """
        return self._get("canstopexposure")

    @property
    def CCDTemperature(self) -> float:
        """The current CCD temperature in degrees Celsius.

        Raises:
            InvalidValueException: If data unavailable.
            NotImplementedException: If not supported (no cooler)
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CCDTemperature|

                .. |CCDTemperature| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CCDTemperature" target="_blank">
                    Camera.CCDTemperature</a> (external)

            .. only:: rinoh

                `Camera.CCDTemperature <https://ascom-standards.org/newdocs/camera.html#Camera.CCDTemperature>`_
        """
        return self._get("ccdtemperature")

    @property
    def CoolerOn(self) -> bool:
        """**(Read/Write)** Turn the camera cooler on and off or return the current cooler on/off state.

        Raises:
            NotConnectedException: If the device is not connected
            NotImplementedException: If not supported (no cooler)
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Warning:
            Turning the cooler off when the cooler is operating at high delta-T
            (typically >20C below ambient) may result in thermal shock. Repeated thermal
            shock may lead to damage to the sensor or cooler stack. Please consult the
            documentation supplied with the camera for further information.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CoolerOn|

                .. |CoolerOn| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CoolerOn" target="_blank">
                    Camera.CoolerOn</a> (external)

            .. only:: rinoh

                `Camera.CoolerOn <https://ascom-standards.org/newdocs/camera.html#Camera.CoolerOn>`_
        """
        return self._get("cooleron")
    @CoolerOn.setter
    def CoolerOn(self, CoolerState: bool):
        self._put("cooleron", CoolerOn=CoolerState)

    @property
    def CoolerPower(self) -> float:
        """The current cooler power level in percent.

        Raises:
            NotImplementedException: If not supported (no cooler)
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |CoolerPower|

                .. |CoolerPower| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.CoolerPower" target="_blank">
                    Camera.CoolerPower</a> (external)

            .. only:: rinoh

                `Camera.CoolerPower <https://ascom-standards.org/newdocs/camera.html#Camera.CoolerPower>`_
        """
        return self._get("coolerpower")

    @property
    def ElectronsPerADU(self) -> float:
        """The gain of the camera in photoelectrons per A/D unit.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Some cameras have multiple gain modes, resulting in this value changing.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ElectronsPerADU|

                .. |ElectronsPerADU| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ElectronsPerADU" target="_blank">
                    Camera.ElectronsPerADU</a> (external)

            .. only:: rinoh

                `Camera.ElectronsPerADU <https://ascom-standards.org/newdocs/camera.html#Camera.ElectronsPerADU>`_
        """
        return self._get("electronsperadu")

    @property
    def ExposureMax(self) -> float:
        """The maximum exposure time (sec) supported by :meth:`StartExposure()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ExposureMax|

                .. |ExposureMax| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ExposureMax" target="_blank">
                    Camera.ExposureMax</a> (external)

            .. only:: rinoh

                `Camera.ExposureMax <https://ascom-standards.org/newdocs/camera.html#Camera.ExposureMax>`_
        """
        return self._get("exposuremax")

    @property
    def ExposureMin(self) -> float:
        """The minimum exposure time (sec) supported by :meth:`StartExposure()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ExposureMin|

                .. |ExposureMin| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ExposureMin" target="_blank">
                    Camera.ExposureMin</a> (external)

            .. only:: rinoh

                `Camera.ExposureMin <https://ascom-standards.org/newdocs/camera.html#Camera.ExposureMin>`_
        """
        return self._get("exposuremin")

    @property
    def ExposureResolution(self) -> float:
        """The smallest increment in exposure time (sec) supported by :meth:`StartExposure()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This can be used, for example, to specify the resolution of a user interface
              "spin control" used to dial in the exposure time.
            * The duration provided to :meth:`StartExposure()` does not have to be an
              exact multiple of this number; the driver will choose the closest available
              value. Also in some cases the resolution may not be constant over the full
              range of exposure times; in this case the smallest increment will be chosen
              by the driver. A value of 0.0 indicates that there is no minimum resolution
              except that imposed by the resolution of the float data type.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ExposureResolution|

                .. |ExposureResolution| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ExposureResolution" target="_blank">
                    Camera.ExposureResolution</a> (external)

            .. only:: rinoh

                `Camera.ExposureResolution <https://ascom-standards.org/newdocs/camera.html#Camera.ExposureResolution>`_
        """

        return self._get("exposureresolution")

    @property
    def FastReadout(self) -> bool:
        """(Read/Write) Gets or sets Fast Readout Mode.

        Raises:
            NotImplementedException: If FastReadout is not supported
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * This function may in some cases interact with :attr:`ReadoutModes`; for
              example, there may be modes where the Fast/Normal switch is meaningless.
              In this case, it may be preferable to use the :attr:`ReadoutModes`
              feature to control fast/normal switching.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |FastReadout|

                .. |FastReadout| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.FastReadout" target="_blank">
                    Camera.FastReadout</a> (external)

            .. only:: rinoh

                `Camera.FastReadout <https://ascom-standards.org/newdocs/camera.html#Camera.FastReadout>`_
        """
        return self._get("fastreadout")
    @FastReadout.setter
    def FastReadout(self, FastReadout: bool):
        self._put("fastreadout", FastReadout=FastReadout)

    @property
    def FullWellCapacity(self) -> float:
        """The full well capacity of the camera (see Notes).

        Raises:
            NotConnectedException: If the device is not connected.
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Reports the full well capacity of the camera in electrons, at the current
              camera settings (binning, SetupDialog settings, etc.).
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |FullWellCapacity|

                .. |FullWellCapacity| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.FullWellCapacity" target="_blank">
                    Camera.FullWellCapacity</a> (external)

            .. only:: rinoh

                `Camera.FullWellCapacity <https://ascom-standards.org/newdocs/camera.html#Camera.FullWellCapacity>`_
        """

        return self._get("fullwellcapacity")

    @property
    def Gain(self) -> int:
        """(Read/Write) Gets or sets the current gain value or index (**see Notes**)

        Raises:
            InvalidValueException: If the supplied valus is not valid
            NotImplementedException: If neither **gains index** mode nor **gains value**
                mode are supported.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            The Gain property is used to adjust the gain setting of the camera and has
            two modes of operation:

            * **Gains-Index:** The Gain property is the selected gain's index within
              the :attr:`Gains` array of textual gain descriptions.

                * In this mode the Gains method returns a *0-based* array of strings, which
                  describe available gain settings e.g. "ISO 200", "ISO 1600"
                * :attr:`GainMin` and :attr:`GainMax` will throw a
                  :py:class:`NotImplementedException`.

            * **Gains-Value:** The Gain property is a direct numeric representation
              of the camera's gain.

                * In this mode the :attr:`GainMin` and :attr:`GainMax` properties must
                  return integers specifying the valid range for Gain.
                * The :attr:`Gains` array property will throw a
                  :py:class:`NotImplementedException`.

            A driver can support none, one or both gain modes depending on the camera's capabilities.
            However, only one mode can be active at any one moment because both modes share the
            Gain property to return the gain value. Your application can determine
            which mode is operational by reading the :attr:`GainMin`, :attr:`GainMax`
            property and this Gain property. If a property can be read then its associated mode
            is active, if it throws a :py:class:`NotImplementedException` then the mode is not active.

        Important:
            The :attr:`ReadoutMode` may in some cases affect the gain of the camera; if so,
            the driver must ensure that the two properties do not conflict if both are used.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Gain|

                .. |Gain| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.Gain" target="_blank">
                    Camera.Gain</a> (external)

            .. only:: rinoh

                `Camera.Gain <https://ascom-standards.org/newdocs/camera.html#Camera.Gain>`_
        """
        return self._get("gain")
    @Gain.setter
    def Gain(self, Gain: int):
        self._put("gain", Gain=Gain)

    @property
    def GainMax(self) -> int:
        """Maximum gain value that this camera supports (see notes and :attr:`Gain`)

        Raises:
            NotImplementedException: If the :attr:`Gain` property is not
                implemented or is operating in **gains-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            When :attr:`Gain` is operating in **gain-value** mode:

            * GainMax must return the camera's highest valid :attr:`Gain` setting
            * The :attr:`Gains` property will throw **NotImplementedException**

            GainMax and :attr:`GainMin` act together and that either both will
            return values, or both will throw **NotImplementedException**.

            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |GainMax|

                .. |GainMax| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.GainMax" target="_blank">
                    Camera.GainMax</a> (external)

            .. only:: rinoh

                `Camera.GainMax <https://ascom-standards.org/newdocs/camera.html#Camera.GainMax>`_
        """
        return self._get("gainmax")

    @property
    def GainMin(self) -> int:
        """Minimum gain value that this camera supports (see notes and :attr:`Gain`)

        Raises:
            NotImplementedException: If the :attr:`Gain` property is not
                implemented or is operating in **gains-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            When :attr:`Gain` is operating in **gain-value** mode:

            * GainMin must return the camera's highest valid :attr:`Gain` setting
            * The :attr:`Gains` property will throw **NotImplementedException**

            GainMin and :attr:`GainMax` act together and that either both will
            return values, or both will throw **NotImplementedException**.

            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |GainMin|

                .. |GainMin| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.GainMin" target="_blank">
                    Camera.GainMin</a> (external)

            .. only:: rinoh

                `Camera.GainMin <https://ascom-standards.org/newdocs/camera.html#Camera.GainMin>`_
         """
        return self._get("gainmin")

    @property
    def Gains(self) -> List[str]:
        """List of Gain *names* supported by the camera (see notes and :attr:`Gain`)

        Raises:
            NotImplementedException: If the :attr:`Gain` property is not
                implemented or is operating in **gains-value** mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            When :attr:`Gain` is operating in the **gains-index** mode:

            * The ``Gains`` property returns a list of available gain setting *names*.
            * The :attr:`GainMax` and :attr:`GainMin` properties will throw
              **NotImplementedException**.

            The returned gain names could, for example, be a list of ISO settings
            for a DSLR camera or a list of gain names for a CMOS camera. Typically
            the application software will display the returned gain names in a
            drop list, from which the astronomer can select the required value.
            The application can then configure the required gain by setting the
            camera's Gain property to the *array index* of the selected description.

            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Gains|

                .. |Gains| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.Gains" target="_blank">
                    Camera.Gains</a> (external)

            .. only:: rinoh

                `Camera.Gains <https://ascom-standards.org/newdocs/camera.html#Camera.Gains>`_
        """
        return self._get("gains")

    @property
    def HasShutter(self) -> bool:
        """Indicate whether the camera has a mechanical shutter.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            If HasShutter is False, the :meth:`StartExposure()` method will ignore the
            Light parameter.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |HasShutter|

                .. |HasShutter| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.HasShutter" target="_blank">
                    Camera.HasShutter</a> (external)

            .. only:: rinoh

                `Camera.HasShutter <https://ascom-standards.org/newdocs/camera.html#Camera.HasShutter>`_
        """
        return self._get("hasshutter")

    @property
    def HeatSinkTemperature(self) -> float:
        """The current heat sink (aka "ambient") temperature (deg C).

        Raises:
            NotConnectedException: If the device is not connected
            NotImplementedException: If :attr:`CanSetCCDTemperature` is False
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |HeatSinkTemperature|

                .. |HeatSinkTemperature| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.HeatSinkTemperature" target="_blank">
                    Camera.HeatSinkTemperature</a> (external)

            .. only:: rinoh

                `Camera.HeatSinkTemperature <https://ascom-standards.org/newdocs/camera.html#Camera.HeatSinkTemperature>`_
        """
        return self._get("heatsinktemperature")

    @property
    def ImageArray(self) -> List[int]:
        """Return a multidimensional list containing the exposure pixel values.

        Raises:
            InvalidOperationException: If no image data is available
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * The returned array is in row-major format, and typically must be transposed
              for use with *numpy* and *astropy* for creating FITS files. See the example
              below.
            * Automatically adapts to devices returning either JSON image data or the much
              faster ImageBytes format. In either case the returned nested list array
              contains standard Python int or float pixel values. See the
              |ImageBytes|.
              See :attr:`ImageArrayInfo` for metadata covering the returned image data.

            .. |ImageBytes| raw:: html

                <a href="https://github.com/ASCOMInitiative/ASCOMRemote/raw/main/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf" target="_blank">
                    Alpaca API Reference</a> (external)

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ImageArray|

                .. |ImageArray| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ImageArray" target="_blank">
                    Camera.ImageArray</a> (external)

            .. only:: rinoh

                `Camera.ImageArray <https://ascom-standards.org/newdocs/camera.html#Camera.ImageArray>`_
        """
        return self._get_imagedata("imagearray")

    @property
    def ImageArrayInfo(self) -> ImageMetadata:
        """Get image metadata sucn as dimensions, data type, rank.

        See Class :py:class:`ImageMetadata` for the properties available.

        Note:
            If no image has been retrieved via :attr:`ImageArray`,
            this returns None.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ImageArrayInfo|

                .. |ImageArrayInfo| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ImageArrayInfo" target="_blank">
                    Camera.ImageArrayInfo</a> (external)

            .. only:: rinoh

                `Camera.ImageArrayInfo <https://ascom-standards.org/newdocs/camera.html#Camera.ImageArrayInfo>`_
        """
        return self.img_desc

    @property
    def ImageReady(self) -> bool:
        """Indicates that an image is ready to be downloaded.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.The device cannot
                *successfully* complete the previous :meth:`Expose()` request
                (see Attention below).

        Note:
            * If ImageReady returns a valid False or True value, then the *non-blocking*
              process of acquiring an image is *proceeding normally* or has been *successful*.
            * ImageReady will be False immediately upon return from :meth:`StartExposure()`.
              It will remain False until the exposure has been *successfully* completed and
              an image is ready for download.

        Attention:
            * If the camera encounters a problem which prevents or prevented it from
              *successfully* completing the exposure, the driver will raise an
              exception when you attempt to read ImageReady.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ImageReady|

                .. |ImageReady| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ImageReady" target="_blank">
                    Camera.ImageReady</a> (external)

            .. only:: rinoh

                `Camera.ImageReady <https://ascom-standards.org/newdocs/camera.html#Camera.ImageReady>`_
        """
        return self._get("imageready")

    @property
    def IsPulseGuiding(self) -> bool:
        """Indicates that the camera is currently in a :meth:`PulseGuide()` operation.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions. See Attention
                below. The device did not *successfully* complete the request.
        Note:
            * If IsPulseGuiding returns a valid True or False value, then the process of
              pulse-guiding is *proceeding normally* or has completed *successfully*,
              respectively.
            * IsPulseGuiding will be True immediately upon return from :meth:`PulseGuide()`.
              It will remain True until the requested pulse-guide interval has elapsed, and
              the pulse-guiding operation has been *successfully* completed. If
              :meth:`PulseGuide()` returns with IsPulseGuiding = False, then you can
              assume that the operation *succeeded* with a very short pulse-guide interval.

        Attention:
            * If the camera encounters a problem which prevents it from *successfully*
              completing the the pulse-guiding operation, the driver will raise an exception
              when you attempt to read IsPulseGuiding.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |IsPulseGuiding|

                .. |IsPulseGuiding| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.IsPulseGuiding" target="_blank">
                    Camera.IsPulseGuiding</a> (external)

            .. only:: rinoh

                `Camera.IsPulseGuiding <https://ascom-standards.org/newdocs/camera.html#Camera.IsPulseGuiding>`_
        """
        return self._get("ispulseguiding")

    @property
    def LastExposureDuration(self) -> float:
        """Report the actual exposure duration in seconds (i.e. shutter open time).

        Raises:
            NotImplementedException: If the camera doesn't support this feature
            InvalidOperationException: If no image has yet been *successfully* acquired.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions. See Attention
                below. The device did not *successfully* complete the request.

        Note:
            * This may differ from the exposure time requested due to shutter latency,
              camera timing precision, etc.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |LastExposureDuration|

                .. |LastExposureDuration| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.LastExposureDuration" target="_blank">
                    Camera.LastExposureDuration</a> (external)

            .. only:: rinoh

                `Camera.LastExposureDuration <https://ascom-standards.org/newdocs/camera.html#Camera.LastExposureDuration>`_
        """
        return self._get("lastexposureduration")

    @property
    def LastExposureStartTime(self) -> str:
        """Start time of the last exposure in FITS standard format, UTC.

        Raises:
            NotImplementedException: If the camera doesn't support this feature
            InvalidOperationException: If no image has yet been *successfully* acquired.
            NotConnectedException: If the device is not connected
            DriverException:  An error occurred that is not described by
                one of the more specific ASCOM exceptions. See Attention
                below. The device did not *successfully* complete the request.

        Note:
            Reports the actual exposure UTC start date/time in the
            FITS-standard / ISO-8601 CCYY-MM-DDThh:mm:ss[.sss...] format.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |LastExposureStartTime|

                .. |LastExposureStartTime| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.LastExposureStartTime" target="_blank">
                    Camera.LastExposureStartTime</a> (external)

            .. only:: rinoh

                `Camera.LastExposureStartTime <https://ascom-standards.org/newdocs/camera.html#Camera.LastExposureStartTime>`_
        """
        return self._get("lastexposurestarttime")

    @property
    def MaxADU(self) -> int:
        """The maximum ADU value of the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |MaxADU|

                .. |MaxADU| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.MaxADU" target="_blank">
                    Camera.MaxADU</a> (external)

            .. only:: rinoh

                `Camera.MaxADU <https://ascom-standards.org/newdocs/camera.html#Camera.MaxADU>`_
        """
        return self._get("maxadu")

    @property
    def MaxBinX(self) -> int:
        """The maximum supported X binning value of the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |MaxBinX|

                .. |MaxBinX| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.MaxBinX" target="_blank">
                    Camera.MaxBinX</a> (external)

            .. only:: rinoh

                `Camera.MaxBinX <https://ascom-standards.org/newdocs/camera.html#Camera.MaxBinX>`_
        """
        return self._get("maxbinx")

    @property
    def MaxBinY(self) -> int:
        """The maximum supported Y binning value of the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |MaxBinY|

                .. |MaxBinY| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.MaxBinY" target="_blank">
                    Camera.MaxBinY</a> (external)

            .. only:: rinoh

                `Camera.MaxBinY <https://ascom-standards.org/newdocs/camera.html#Camera.MaxBinY>`_
        """
        return self._get("maxbiny")

    @property
    def NumX(self) -> int:
        """(Read/Write) Set or return the current subframe width.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * If binning is active, value is in binned pixels.
            * Defaults to :attr:`CameraXSize` with :attr:`StartX` = 0
              (full frame) on initial camera startup.

        Attention:
            * No error check is performed for incompatibilty with :attr:`BinX`,
              and :attr:`StartX`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to
              :meth:`StartExposure()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |NumX|

                .. |NumX| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.NumX" target="_blank">
                    Camera.NumX</a> (external)

            .. only:: rinoh

                `Camera.NumX <https://ascom-standards.org/newdocs/camera.html#Camera.NumX>`_
        """
        return self._get("numx")
    @NumX.setter
    def NumX(self, NumX: int):
        self._put("numx", NumX=NumX)

    @property
    def NumY(self) -> int:
        """(Read/Write) Set or return the current subframe height.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * If binning is active, value is in binned pixels.
            * Defaults to :attr:`CameraYSize` with :attr:`StartY` = 0
              (full frame) on initial camera startup.

        Attention:
            * No error check is performed for incompatibilty with :attr:`BinY`,
              and :attr:`StartY`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to
              :meth:`StartExposure()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |NumY|

                .. |NumY| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.NumY" target="_blank">
                    Camera.NumY</a> (external)

            .. only:: rinoh

                `Camera.NumY <https://ascom-standards.org/newdocs/camera.html#Camera.NumY>`_
        """
        return self._get("numy")
    @NumY.setter
    def NumY(self, NumY: int):
        self._put("numy", NumY=NumY)

    @property
    def Offset(self) -> int:
        """(Read/Write) Gets or sets the current offset value or index (**see Notes**)

        Raises:
            InvalidValueException: If the supplied value is not valid
            NotImplementedException: If neither **offsets index** mode nor **offsets value**
                mode are supported.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            The Offset property is used to adjust the offset setting of the camera and has
            two modes of operation:

            * **Offsets-Index:** The Offset property is the selected offset's index within
              the :attr:`Offsets` array of textual offset descriptions.

                * In this mode the :attr:`Offsets` method returns a *0-based* array of
                  strings, which describe available offset settings.
                * :attr:`OffsetMin` and :attr:`OffsetMax` will throw a
                  :py:class:`NotImplementedException`.

            * **Offsets-Value:** The Offset property is a direct numeric representation
              of the camera's offset.

                * In this mode the :attr:`OffsetMin` and :attr:`OffsetMax` properties must
                  return integers specifying the valid range for Offset.
                * The :attr:`Offsets` array property will throw a
                  :py:class:`NotImplementedException`.

            A driver can support none, one or both offset modes depending on the camera's capabilities.
            However, only one mode can be active at any one moment because both modes share the
            Offset property to return the offset value. Your application can determine
            which mode is operational by reading the :attr:`OffsetMin`, :attr:`OffsetMax`
            property and this Offset property. If a property can be read then its associated mode
            is active, if it throws a :py:class:`NotImplementedException` then the mode is not active.

        Important:
            The :attr:`ReadoutMode` may in some cases affect the offset of the camera; if so,
            the driver must ensure that the two properties do not conflict if both are used.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Offset|

                .. |Offset| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.Offset" target="_blank">
                    Camera.Offset</a> (external)

            .. only:: rinoh

                `Camera.Offset <https://ascom-standards.org/newdocs/camera.html#Camera.Offset>`_
        """
        return self._get("offset")
    @Offset.setter
    def Offset(self, Offset: int):
        self._put("offset", Offset=Offset)

    @property
    def OffsetMax(self) -> int:
        """Maximum offset value that this camera supports (see notes and :attr:`Offset`)

        Raises:
            NotImplementedException: If the :attr:`Offset` property is not
                implemented or is operating in **offsets-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            When :attr:`Offset` is operating in **offsets-value** mode:

            * ``OffsetMax`` must return the camera's highest valid :attr:`Offset` setting
            * The :attr:`Offsets` property will throw **NotImplementedException**

            OffsetMax and :attr:`OffsetMin` act together and that either both will
            return values, or both will throw **NotImplementedException**.

            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |OffsetMax|

                .. |OffsetMax| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.OffsetMax" target="_blank">
                    Camera.OffsetMax</a> (external)

            .. only:: rinoh

                `Camera.OffsetMax <https://ascom-standards.org/newdocs/camera.html#Camera.OffsetMax>`_
        """
        return self._get("offsetmax")

    @property
    def OffsetMin(self) -> int:
        """Minimum offset value that this camera supports (see notes and :attr:`Offset`)

        Raises:
            NotImplementedException: If the :attr:`Offset` property is not
                implemented or is operating in **offsets-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            When :attr:`Offset` is operating in **offsets-value** mode:

            * OffsetMin must return the camera's highest valid :attr:`Offset` setting
            * The :attr:`Offsets` property will throw :py:class:`NotImplementedException`.

            OffsetMin and :attr:`OffsetMax` act together and that either both will
            return values, or both will throw :py:class:`NotImplementedException`.

            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |OffsetMin|

                .. |OffsetMin| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.OffsetMin" target="_blank">
                    Camera.OffsetMin</a> (external)

            .. only:: rinoh

                `Camera.OffsetMin <https://ascom-standards.org/newdocs/camera.html#Camera.OffsetMin>`_
         """
        return self._get("offsetmin")

    @property
    def Offsets(self) -> List[str]:
        """List of Offset *names* supported by the camera (see notes and :attr:`Offset`)

        Raises:
            NotImplementedException: If the :attr:`Offset` property is not
                implemented or is operating in **offsets-value** mode.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            When :attr:`Offset` is operating in the **offsets-index** mode:

            * The ``Offsets`` property returns a list of available offset setting *names*.
            * The :attr:`OffsetMax` and :attr:`OffsetMin` properties will throw
              :py:class:`NotImplementedException`.

            The returned offset names could, for example, be a list of ISO settings
            for a DSLR camera or a list of offset names for a CMOS camera. Typically
            the application software will display the returned offset names in a
            drop list, from which the astronomer can select the required value.
            The application can then configure the required offset by setting the
            camera's Offset property to the *array index* of the selected description.

            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |Offsets|

                .. |Offsets| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.Offsets" target="_blank">
                    Camera.Offsets</a> (external)

            .. only:: rinoh

                `Camera.Offsets <https://ascom-standards.org/newdocs/camera.html#Camera.Offsets>`_
        """
        return self._get("offsets")

    @property
    def PercentCompleted(self) -> int:
        """The percentage completeness of this operation

        Raises:
            InvalidOperationException: When it is inappropriate to ask for a
                completion percentage.
            NotImplementedException: If this optional property is not implemented.
            NotConnectedException: If the device is not connected.
            DriverException:  An error occurred that is not described by
                one of the more specific ASCOM exceptions. See Attention
                below. The device did not *successfully* complete the request.

        Note:
            * If valid, returns an integer between 0 and 100, where 0 indicates 0% progress
              (function just started) and 100 indicates 100% progress (i.e. completion).
            * At the discretion of the device, PercentCompleted may optionally be valid
              when :attr:`CameraState` is in any or all of the following states:

                * ``cameraExposing``
                * ``cameraWaiting``
                * ``cameraReading``
                * ``cameraDownloading``

            In all other states an :py:class:`InvalidOperationException` will be raised.

        Attention:
            * If the camera encounters a problem which prevents or prevented it from
              *successfully* completing the operation, the driver will raise an
              exception when you attempt to read PercentComplete.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |PercentCompleted|

                .. |PercentCompleted| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.PercentCompleted" target="_blank">
                    Camera.PercentCompleted</a> (external)

            .. only:: rinoh

                `Camera.PercentCompleted <https://ascom-standards.org/newdocs/camera.html#Camera.PercentCompleted>`_
        """
        return self._get("percentcompleted")

    @property
    def PixelSizeX(self) -> float:
        """The width (microns) of the camera sensor elements.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |PixelSizeX|

                .. |PixelSizeX| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.PixelSizeX" target="_blank">
                    Camera.PixelSizeX</a> (external)

            .. only:: rinoh

                `Camera.PixelSizeX <https://ascom-standards.org/newdocs/camera.html#Camera.PixelSizeX>`_
        """
        return self._get("pixelsizex")

    @property
    def PixelSizeY(self) -> float:
        """The height (microns) of the camera sensor elements.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |PixelSizeY|

                .. |PixelSizeY| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.PixelSizeY" target="_blank">
                    Camera.PixelSizeY</a> (external)

            .. only:: rinoh

                `Camera.PixelSizeY <https://ascom-standards.org/newdocs/camera.html#Camera.PixelSizeY>`_
        """
        return self._get("pixelsizey")

    @property
    def ReadoutMode(self) -> int:
        """(Read/Write) Gets or sets the current camera readout mode (**see Notes**)

        Raises:
            InvalidValueException: If the supplied value is not valid (index out of range)
            NotImplementedException: If :attr:`CanFastReadout` is True.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * ReadoutMode is an index into the array :attr:`ReadoutModes`, and
              selects the desired readout mode for the camera. Defaults to 0 if not set.
            * It is strongly recommended, but not required, that cameras make the 0-index
              mode suitable for standard imaging operations, since it is the default.

        Important:
            The :attr:`ReadoutMode` may in some cases affect the :attr:`Gain`
            and/or :attr:`Offset` of the camera; if so, the camera must ensure
            that the two properties do not conflict if both are used.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ReadoutMode|

                .. |ReadoutMode| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ReadoutMode" target="_blank">
                    Camera.ReadoutMode</a> (external)

            .. only:: rinoh

                `Camera.ReadoutMode <https://ascom-standards.org/newdocs/camera.html#Camera.ReadoutMode>`_
        """
        return self._get("readoutmode")
    @ReadoutMode.setter
    def ReadoutMode(self, ReadoutMode: int):
        self._put("readoutmode", ReadoutMode=ReadoutMode)

    @property
    def ReadoutModes(self) -> List[str]:
        """List of ReadoutMode *names* supported by the camera (see notes and :attr:`ReadoutMode`)

        Raises:
            NotImplementedException: If the :attr:`ReadoutMode` property is not
                implemented.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Readout modes may be available from the camera, and if so then
              :attr:`CanFastReadout` will be False. The two camera mode selection
              schemes are mutually exclusive.
            * This property provides an array of strings, each of which describes an
              available readout mode of the camera. At least one string will be present
              in the list. Your application may use this list to present to the user a
              drop-list of modes. The choice of available modes made available is
              entirely at the discretion of the camera. Please note that if the camera
              has many different modes of operation, then the most commonly adjusted
              settings will probably be in ReadoutModes; additional settings may be
              provided using :meth:`SetupDialog()`.
            * To select a mode, set ReadoutMode to the index of the desired mode.
              The index is zero-based.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |ReadoutModes|

                .. |ReadoutModes| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.ReadoutModes" target="_blank">
                    Camera.ReadoutModes</a> (external)

            .. only:: rinoh

                `Camera.ReadoutModes <https://ascom-standards.org/newdocs/camera.html#Camera.ReadoutModes>`_
        """
        return self._get("readoutmodes")

    @property
    def SensorName(self) -> str:
        """The name of the sensor used within the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Returns the name (data sheet part number) of the sensor, e.g. ICX285AL.
              The format is to be exactly as shown on manufacturer data sheet,
              subject to the following rules:

                * All letters will be upper-case.
                * Spaces will not be included.
                * Any extra suffixes that define region codes, package types, temperature range,
                  coatings, grading, colour/monochrome, etc. will not be included.
                * For colour sensors, if a suffix differentiates different Bayer matrix encodings,
                  it will be included.
                * The property will return an empty string if the sensor name is not known
            * Examples:
                * ICX285AL-F shall be reported as ICX285
                * KAF-8300-AXC-CD-AA shall be reported as KAF-8300
            * The most common usage of this property is to select approximate colour balance
              parameters to be applied to the Bayer matrix of one-shot colour sensors.
              Application authors should assume that an appropriate IR cut-off filter is
              in place for colour sensors.
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SensorName|

                .. |SensorName| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.SensorName" target="_blank">
                    Camera.SensorName</a> (external)

            .. only:: rinoh

                `Camera.SensorName <https://ascom-standards.org/newdocs/camera.html#Camera.SensorName>`_
        """
        return self._get("sensorname")

    @property
    def SensorType(self) -> SensorType:
        """The type of sensor within the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * It is recommended that this property be retrieved only after a connection is
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SensorType|

                .. |SensorType| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.SensorType" target="_blank">
                    Camera.SensorType</a> (external)

            .. only:: rinoh

                `Camera.SensorType <https://ascom-standards.org/newdocs/camera.html#Camera.SensorType>`_
        """
        return SensorType(self._get("sensortype"))

    @property
    def SetCCDTemperature(self) -> float:
        """(Read/Write) Get or set the camera's cooler setpoint (degrees Celsius).

        Raises:
            InvalidValueException: If set to a value outside the camera's valid
                temperature setpoint range.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SetCCDTemperature|

                .. |SetCCDTemperature| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.SetCCDTemperature" target="_blank">
                    Camera.SetCCDTemperature</a> (external)

            .. only:: rinoh

                `Camera.SetCCDTemperature <https://ascom-standards.org/newdocs/camera.html#Camera.SetCCDTemperature>`_
        """
        return self._get("setccdtemperature")
    @SetCCDTemperature.setter
    def SetCCDTemperature(self, SetCCDTemperature: float):
        self._put("setccdtemperature", SetCCDTemperature=SetCCDTemperature)

    @property
    def StartX(self) -> int:
        """(Read/Write) Set or return the current X-axis subframe start position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * If binning is active, value is in binned pixels.
            * Defaults to 0 with :attr:`NumX` = :attr:`CameraXSize`
              (full frame) on initial camera startup.

        Attention:
            * No error check is performed for incompatibilty with :attr:`BinX`,
              and :attr:`NumX`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to
              :meth:`StartExposure()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |StartX|

                .. |StartX| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.StartX" target="_blank">
                    Camera.StartX</a> (external)

            .. only:: rinoh

                `Camera.StartX <https://ascom-standards.org/newdocs/camera.html#Camera.StartX>`_
        """
        return self._get("startx")
    @StartX.setter
    def StartX(self, StartX: int):
        self._put("startx", StartX=StartX)

    @property
    def StartY(self) -> int:
        """(Read/Write) Set or return the current Y-axis subframe start position.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * If binning is active, value is in binned pixels.
            * Defaults to 0 with :attr:`NumY` = :attr:`CameraYSize`
              (full frame) on initial camera startup.

        Attention:
            * No error check is performed for incompatibilty with :attr:`BinY`,
              and :attr:`NumY`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to
              :meth:`StartExposure()`.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |StartY|

                .. |StartY| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.StartY" target="_blank">
                    Camera.StartY</a> (external)

            .. only:: rinoh

                `Camera.StartY <https://ascom-standards.org/newdocs/camera.html#Camera.StartY>`_
        """
        return self._get("starty")
    @StartY.setter
    def StartY(self, StartY):
        self._put("starty", StartY=StartY)

    @property
    def SubExposureDuration(self) -> float:
        """(Read/Write) Set or return the camera's sub-exposure interval (sec)

        Raises:
            NotImplementedException: The camera does not support
                on-board stacking with user-supplied sub-exposure interval.
            NotConnectedException: If the device is not connected.
            InvalidValueException: The supplied duration is not valid.
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |SubExposureDuration|

                .. |SubExposureDuration| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.SubExposureDuration" target="_blank">
                    Camera.SubExposureDuration</a> (external)

            .. only:: rinoh

                `Camera.SubExposureDuration <https://ascom-standards.org/newdocs/camera.html#Camera.SubExposureDuration>`_
        """
        return self._get("subexposureduration")
    @SubExposureDuration.setter
    def SubExposureDuration(self, SubexposureDuration: float):
        self._put("subexposureduration", SubexposureDuration=SubexposureDuration)

    def AbortExposure(self) -> None:
        """Abort the current exposure, if any, and returns the camera to Idle state.

        Raises:
            NotConnectedException: If the device is not connected.
            InvalidOperationException: If not currently possible (e.g. during image download)
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Unlike :meth:`StopExposure()` this method simply discards any
              partially-acquired image data and returns the camera to idle.
            * Will not raise an exception if the camera is already idle.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |AbortExposure|

                .. |AbortExposure| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.AbortExposure" target="_blank">
                    Camera.AbortExposure()</a> (external)

            .. only:: rinoh

                `Camera.AbortExposure() <https://ascom-standards.org/newdocs/camera.html#Camera.AbortExposure>`_
        """
        self._put("abortexposure")

    def PulseGuide(self, Direction: GuideDirections, Duration: int) -> None:
        """Pulse guide in the specified direction for the specified time (ms).

        **Non-blocking**: See Notes, and :ref:`async_faq`

        Args:
            Direction: :py:class:`~alpaca.telescope.GuideDirections`
            Interval: duration of the guide move, milliseconds

        Raises:
            NotImplementedException: If the camera does not support pulse guiding
                (:attr:`CanPulseGuide` property is False)
            NotConnectedException: If the device is not connected.
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * **Asynchronous**: The method returns as soon pulse-guiding operation
              has been *successfully* started with :attr:`IsPulseGuiding` property True.
              However, you may find that :attr:`IsPulseGuiding` is False when you get
              around to checking it if the 'pulse' is short. This is still a success if you
              get False back and not an exception. See :ref:`async_faq`
            * Some cameras have implemented this as a Synchronous (blocking) operation.
            * :py:class:`~alpaca.telescope.GuideDirections` for North and South
              have varying interpretations
              by German Equatorial mounts. Some GEM mounts interpret North to be
              the same rotation direction of the declination axis regardless of
              their pointing state ("side of the pier"). Others truly implement
              North and South by reversing the dec-axis rotation depending on
              their pointing state. **Apps must be prepared for either behavior**.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |PulseGuide|

                .. |PulseGuide| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.PulseGuide" target="_blank">
                    Camera.PulseGuide()</a> (external)

            .. only:: rinoh

                `Camera.PulseGuide() <https://ascom-standards.org/newdocs/camera.html#Camera.PulseGuide>`_
        """
        self._put("pulseguide", Direction=Direction, Duration=Duration)

    def StartExposure(self, Duration: float, Light: bool) -> None:
        """Start an exposure.

        **Non-blocking**: Returns with :attr:`ImageReady` = False
        if exposure has *successfully* been started. See :ref:`async_faq`

        Args:
            Duration: Duration of exposure in seconds.
            Light: True for light frame, False for dark frame.

        Raises:
            InvalidValueException: If Duration is invalid, or if :attr:`BinX`,
                :attr:`BinY`, :attr:`NumX`, :attr:`NumY`, :attr:`StartX`,
                and :attr:`StartY` form an illegal combination.
            InvalidOperationException: If :attr:`CanAsymmetricBin` is False, yet
                :attr:`BinX` is not equal to :attr:`BinY`.
            NotConnectedException: If the device is not connected.
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions. You may get this
                when reading IMageReady. The device did not *successfully*
                complete the request.

        Note:
            * **Asynchronous** (non-blocking): Use :attr:`ImageReady`
              to determine if the exposure has been *successfully*
              completed. See :ref:`async_faq`
            * Refer to :attr:`ImageReady` for additional info.
            * See the :ref:`Example` below.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |StartExposure|

                .. |StartExposure| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.StartExposure" target="_blank">
                    Camera.StartExposure()</a> (external)

            .. only:: rinoh

                `Camera.StartExposure() <https://ascom-standards.org/newdocs/camera.html#Camera.StartExposure>`_
        """
        self._put("startexposure", Duration=Duration, Light=Light)

    def StopExposure(self) -> None:
        """Stop the current exposure, if any, and download the image data already acquired.

        Raises:
            NotImplementedException: If the camera cannot stop an in-progress exposure
                and save the already-acquired image data (:attr:`CanStopExposure` is False)
            NotConnectedException: If the device is not connected.
            InvalidOperationException: If not currently possible (e.g. during image download)
            DriverException: An error occurred that is not described by one of the more specific ASCOM exceptions. The device did not *successfully* complete the request.

        Note:
            * Unlike :meth:`AbortExposure()` this method cuts an exposure short
              while preserving the image data acquired so far, making it available
              to the app.
            * If an exposure is in progress, the readout process is initiated.
              Ignored if readout is already in process.
            * Will not raise an exception if the camera is already idle.

        .. admonition:: Master Interfaces Reference
            :class: green

            .. only:: html

                |StopExposure|

                .. |StopExposure| raw:: html

                    <a href="https://ascom-standards.org/newdocs/camera.html#Camera.StopExposure" target="_blank">
                    Camera.StopExposure()</a> (external)

            .. only:: rinoh

                `Camera.StopExposure() <https://ascom-standards.org/newdocs/camera.html#Camera.StopExposure>`_
        """
        self._put("stopexposure")

# === LOW LEVEL ROUTINES TO GET IMAGE DATA WITH OPTIONAL IMAGEBYTES ===
#     https://www.w3resource.com/python/python-bytes.php#byte-string

    def _get_imagedata(self, attribute: str, **data) -> str:
        """TBD

        Args:
            attribute (str): Attribute to get from server.
            **data: Data to send with request.

        """
        url = f"{self.base_url}/{attribute}"
        hdrs = {'accept' : 'application/imagebytes'}
        # Make Host: header safe for IPv6
        if(self.address.startswith('[') and not self.address.startswith('[::1]')):
            hdrs['Host'] = f'{self.address.split("%")[0]}]'
        pdata = {
                "ClientTransactionID": f"{Device._client_trans_id}",
                "ClientID": f"{Device._client_id}"
                }
        pdata.update(data)
        try:
            Device._ctid_lock.acquire()
            response = requests.get("%s/%s" % (self.base_url, attribute), params=pdata, headers=hdrs)
            Device._client_trans_id += 1
        finally:
            Device._ctid_lock.release()

        if response.status_code not in range(200, 204):                 # HTTP level errors
            raise AlpacaRequestException(response.status_code,
                    f"{response.reason}: {response.text} (URL {response.url})")

        ct = response.headers.get('content-type')   # case insensitive
        m = 'little'
        #
        # IMAGEBYTES
        #
        if ct == 'application/imagebytes':
            b = response.content
            n = int.from_bytes(b[4:8], m)
            if n != 0:
                m = response.text[44:].decode(encoding='UTF-8')
                raise_alpaca_if(n, m)               # Will raise here
            self.img_desc = ImageMetadata(
                int.from_bytes(b[0:4], m),          # Meta version
                int.from_bytes(b[20:24], m),        # Image element type
                int.from_bytes(b[24:28], m),        # Xmsn element type
                int.from_bytes(b[28:32], m),        # Rank
                int.from_bytes(b[32:36], m),        # Dimension 1
                int.from_bytes(b[36:40], m),        # Dimension 2
                int.from_bytes(b[40:44], m)         # Dimension 3
                )
            #
            # Bless you Kelly Bundy and Mark Ransom
            # https://stackoverflow.com/questions/71774719/native-array-frombytes-not-numpy-mysterious-behavior/71776522#71776522
            #
            if self.img_desc.TransmissionElementType == ImageArrayElementTypes.Int16.value:
                tcode = 'h'
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.UInt16.value:
                tcode = 'H'
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.Int32.value:
                tcode = 'l'
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.Double.value:
                tcode = 'd'
            # Extension types for future. 64-bit pixels are unlikely to be seen on the wire
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.Byte.value:
                tcode = 'B'     # Unsigned
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.UInt32.value:
                tcode = 'L'
            else:
               raise InvalidValueException("Unknown or as-yet unsupported ImageBytes Transmission Array Element Type")
            #
            # Assemble byte stream back into indexable machine data types
            #
            a = array.array(tcode)
            data_start = int.from_bytes(b[16:20],m)
            a.frombytes(b[data_start:])     # 'h', 'H', 16-bit ints 2 bytes get turned into Python 32-bit ints
            #
            # Convert to common Python nested list "array".
            #
            l = []
            rows = self.img_desc.Dimension1
            cols = self.img_desc.Dimension2
            if self.img_desc.Rank == 3:
                for i in range(rows):
                    rowidx = i * cols * 3
                    r = []
                    for j in range(cols):
                        colidx = j * 3
                        r.append(a[colidx:colidx+3])
                    l.append(r)
            else:
                for i in range(rows):
                    rowidx = i * cols
                    l.append(a[rowidx:rowidx+cols])

            return l                                # Nested lists
        #
        # JSON IMAGE DATA -> List of Lists (row major)
        #
        else:
            j = response.json()
            n = j["ErrorNumber"]
            m = j["ErrorMessage"]
            raise_alpaca_if(n, m)                   # Raise Alpaca Exception if non-zero Alpaca error
            l = j["Value"]                          # Nested lists
            if type(l[0][0]) == list:               # Test & pick up color plane
                r = 3
                d3 = len(l[0][0])
            else:
                r = 2
                d3 = 0
            self.img_desc = ImageMetadata(
                1,                                  # Meta version
                ImageArrayElementTypes.Int32,       # Image element type
                ImageArrayElementTypes.Int32,       # Xmsn element type
                r,                                  # Rank
                len(l),                             # Dimension 1
                len(l[0]),                          # Dimension 2
                d3                                  # Dimension 3
            )
            return l

def raise_alpaca_if(n, m):
    """If non-zero Alpaca error, raise the appropriate Alpaca exception

    Parameters:
        n: Error number from JSON response
        m: Message text for exception

    Returns:
        Nothing if n==0, raises if n != 0

    Note:
        * If an unassigned error code in the range 0x400 <= code <= 0x4FF
          is received, a DriverException will also be raised.

    """
    if n == 0x0400:
        raise NotImplementedException(m)
    elif n == 0x0401:
        raise InvalidValueException(m)
    elif n == 0x0402:
        raise ValueNotSetException(m)
    elif n == 0x0407:
        raise NotConnectedException(m)
    elif n == 0x0408:
        raise ParkedException(m)
    elif n == 0x0409:
        raise SlavedException(m)
    elif n == 0x040B:
        raise InvalidOperationException(m)
    elif n == 0x040c:
        raise ActionNotImplementedException(m)
    elif n >= 0x500 and n <= 0xFFF:
        raise DriverException(n, m)
    else:
        # Per request Apr-2022 include otherwise unassigned numbers in DriverExeception
        raise DriverException(n, m)
